#include "libcan.h"

#include <sys/types.h>
#include <regex.h>

#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <assert.h>
#include <math.h>

enum varName {
	DISTANCE_RATIO,
	ROTATE_RATIO
};

struct var {
	enum varName name;
	double value;
};

#include "ini.h"

#define MATCH(s, n) strcasecmp(section, s) == 0 && strcasecmp(name, n) == 0

static int parse(
		void * user,
		const char * section,
		const char * name,
		const char * value)
{
	struct var * v = user;
	switch (v->name) {
		case DISTANCE_RATIO:
			if (MATCH("asserv", "forward")) {
				sscanf(value, "%lf", &(v->value));
				return 1;
			}
			break;
		case ROTATE_RATIO:
			if (MATCH("asserv", "rotate")) {
				sscanf(value, "%lf", &(v->value));
				return 1;
			}
			break;
	}
    //atoi(value);
    //strdup(value);
    return 1;
}

double getValue(enum varName name)
{
	static char * filename = NULL;
	if (filename == NULL) {
		char * env = getenv("ROBOT_CONFIG_FILE");
		if (env != NULL && strlen(env) != 0) {
			if ((filename = malloc(strlen(env)+1)) == NULL) {
				perror("malloc");
				filename = "conf.ini";
			} else {
				strcpy(filename, env);
			}
		} else {
			filename = "conf.ini";
		}
	}

	struct var v;
	v.name = name;

	int errno;
	if ((errno = ini_parse(filename, parse, &v)) != 0) {
		if (errno == -1) {
			fprintf(stderr, "ini_parse: failed to open config file '%s'\n", filename);
			fprintf(stderr, "please check value of ROBOT_CONFIG_FILE environment variable\n");
		} else {
			fprintf(stderr, "ini_parse: failed to parse config file '%s': error line %d\n", filename, errno);
		}
		return -1;
	}

	return v.value;
}

int can_write(int fd, can_t packet)
{	
    char output[256];

	int carte = packet.id >> 7;
	int id = packet.id & 127;

	int send = 1;
	int verbose = 0;

	if (carte == 0) { // ARM & SUIVEUR ---------------------------------
		if (id == 127) { // reset
			sprintf(output, "RESET\n");
		} else if (verbose > 0) {
			sprintf(output, "??? (ARM&SUIVEUR:%d)\n", id);
		} else {
			send = 0;
		}
	} else if (carte == 1) { // ALIM (tourelle) ----------------------
		if (0) {
		} else if (verbose > 0) {
			sprintf(output, "??? (ALIM:%d)\n", id);
		} else {
			send = 0;
		}
	} else if (carte == 2) { // CAPTEURS -----------------------------
		if ((id & 64) == 64) { // sonar
			int no = (id >> 5)%2 + 1;
			id = id & 31;
			if ((id & 30) == 12) { // broadcast
				sprintf(output, "SONAR %d\tBROADCAST\t%s\n", no,
						(id&1)==1?"ON":"OFF");
			} else if ((id & 28) == 0) { // echo
				sprintf(output, "SONAR %d\t%s\t%hu\t%s\n", no,
						(id&1)==1?"UNDER":"upon",
						((uint16_t*)packet.b)[0],
						(id&2)==2?"EDGE":"");
			} else if (id == 4) { // ask value
				sprintf(output, "SONAR %d\tREQUEST\n", no);
			} else if (id == 8) { // seuil
				sprintf(output, "SONAR %d\tTHRESHOLD\t%hu\n", no,
						((uint16_t*)packet.b)[0]);
			} else if (verbose > 0) {
				sprintf(output, "??? (CAPTEURS:SONAR%d:%d)\n", no, id);
			} else {
				send = 0;
			}
		} else if ((id & 124) == 0) { // bump
			sprintf(output, "BUMP\t%s\t%s\n",
					(id&2)==2?"FRONT":"BACK",
					(id&1)==1?"ON":"OFF");
		} else if ((id & 96) == 32) { // sharp FIXME
			if ((id & 24) == 24) { // broadcast
				sprintf(output, "SHARP %d\tBROADCAST\t%s\n",
						((id&6)>>1)+1, (id&1)==1?"ON":"OFF");
			} else if ((id & 25) == 16) {
				sprintf(output, "SHARP %d\tREQUEST\n",
						((id&6)>>1)+1);
			} else if ((id & 25) == 0) {
				sprintf(output, "SHARP %d\tTHRESHOLD\t%hu\n",
						((id&6)>>1)+1, ((uint16_t*)packet.b)[0]);
			} else if (verbose > 0) {
				sprintf(output, "??? (CAPTEURS:SHARD%d:%d)\n", ((id&6)>>1)+1, id);
			} else {
				send = 0;
			}
		} else if (verbose > 0) {
			sprintf(output, "??? (CAPTEURS:%d)\n", id);
		} else {
			send = 0;
		}
	} else if (carte == 4) { // ODOMÉTRIE ----------------------------
		if (id == 1) {
			sprintf(output, "ODO\tREQUEST\n");
		} else if ((id & 126) == 2) {
			sprintf(output, "ODO\tBROADCAST\t%s\n", (id&1)==1?"ON":"OFF");
		} else if ((id & 126) == 4) {
			if (id == 4) {
				sprintf(output, "ODO\tPOSITION\t");
			} else if (id == 5) {
				sprintf(output, "ODO\tSET     \t");
			}
			sprintf(output+strlen(output), "x=%+d mm\ty=%+d mm\ttheta=%.2lf°\n",
					((int16_t*)packet.b)[0],
					((int16_t*)packet.b)[1],
					((uint16_t*)packet.b)[2]/100.0);
		} else if (verbose > 0) {
			sprintf(output, "??? (ODO:%d)\n", id);
		} else {
			send = 0;
		}
	} else if (carte == 8) { // ASSERV ------------------------------
		if (id == 1) {
			double distance = ((int16_t*)packet.b)[0] / getValue(DISTANCE_RATIO);
			sprintf(output, "DISTANCE\t%+.1lf mm\n", distance / 10);
		} else if (id == 2) {
			double angle = ((int16_t*)packet.b)[0] / getValue(ROTATE_RATIO);
			sprintf(output, "ROTATE\t%+.2lf°\n", angle);
		} else if (id == 5) {
			sprintf(output, "SPEED\tCURT\t%+hhd\t%+hhd\n", packet.b[0], packet.b[1]);
		} else if (id == 4) {
			sprintf(output, "ASSERV\tDONE\n", id);
		} else if (id == 127 || id == 27) { // FIXME
			sprintf(output, "STOP\n", id);
		} else if ((id & 126) == 6) {
			sprintf(output, "ASSERV\t%s\n", (id&1==1)?"OFF":"ON"); // FIXME
		} else if (id == 8) {
			sprintf(output, "SPEED\t\t%+hhd\t%+hhd\n", packet.b[0], packet.b[1]);
		} else if (verbose > 0) {
			sprintf(output, "??? (ASSERV:%d)\n", id);
		} else {
			send = 0;
		}
	} else if (verbose > 1) {
		sprintf(output, "??? (%d:%d)\n", carte, id);
	} else {
		send = 0;
	}
    
	if (send) {
		write(fd, output, strlen(output));
    	fsync(fd);
	}

    return 0;
}

#define PMATCH_MAX 32
#define BUF_LENGTH 256
#define LINE_LENGTH 256

int multiplier(char * buffer, int * send)
{
	if (strcasecmp(buffer, "mm") == 0) {
		return 10;
	} else if (strcasecmp(buffer, "cm") == 0) {
		return 100;
	} else if (strcasecmp(buffer, "m") == 0) {
		return 10000;
	} else if (strlen(buffer) == 0) { // par défaut, cm
		return 100;
	} else {
		return 0;
		*send = -1;
	}
}

void can_listen(FILE * stream, void(*receiv)(unsigned int, can_t))
{
    can_t packet;
    char line[LINE_LENGTH];
	char buffer[BUF_LENGTH];
	int send = 0;
	int result, start, end;
	size_t size;
	regmatch_t pmatch[PMATCH_MAX];

	// ARM & SUIVEUR -------------------------------------------------

	regex_t reg_reset;
	assert(!regcomp(&reg_reset, "^reset[ \t]*\n$",
				REG_EXTENDED | REG_ICASE | REG_NOSUB));

	// ALIM ----------------------------------------------------------
			
	// CAPTEURS ------------------------------------------------------
	
	regex_t reg_sonar_echo;
	assert(!regcomp(&reg_sonar_echo, "^sonar[ \t]+(1|2)[ \t]+(under|upon)[ \t]+([0-9]+)([ \t]+(edge)+|)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_sonar_echo.re_nsub < PMATCH_MAX); // pmatch[0] = all

	regex_t reg_sonar_threshold;
	assert(!regcomp(&reg_sonar_threshold, "^sonar[ \t]+(1|2)[ \t]+threshold[ \t]+([0-9]+)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_sonar_threshold.re_nsub < PMATCH_MAX); // pmatch[0] = all
	
	regex_t reg_sonar_request;
	assert(!regcomp(&reg_sonar_request, "^sonar[ \t]+(1|2)[ \t]+request[ \t]*\n$",
				REG_EXTENDED |REG_NOSUB));
	assert(reg_sonar_request.re_nsub < PMATCH_MAX); // pmatch[0] = all

	regex_t reg_sonar_status;
	assert(!regcomp(&reg_sonar_status, "^sonar[ \t]+(broadcast[ \t]+|bc[ \t]+|)(1|2)[ \t]+(on|off|1|0)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_sonar_status.re_nsub < PMATCH_MAX); // pmatch[0] = all
	
	regex_t reg_bump;
	assert(!regcomp(&reg_bump, "^bump[ \t]+(front|back|2|1)[ \t]+(on|off|1|0)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_bump.re_nsub < PMATCH_MAX); // pmatch[0] = all

	// ODOMÉTRIE -----------------------------------------------------
	
	regex_t reg_odo_request;
	assert(!regcomp(&reg_odo_request, "^odo[ \t]+request[ \t]*\n$",
				REG_EXTENDED | REG_ICASE | REG_NOSUB));

	regex_t reg_odo_status;
	assert(!regcomp(&reg_odo_status, "^odo[ \t]+(broadcast[ \t]+|bc[ \t]+|)(on|off|1|0)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_odo_status.re_nsub < PMATCH_MAX); // pmatch[0] = all

	regex_t reg_odo_pos;
	assert(!regcomp(&reg_odo_pos, "^(odo[ \t]+(set)|(odo[ \t]+|)(position)|(odo[ \t]+|)(pos))[ \t]+(x[ ]?=[ ]?|)((\\+|-|)[0-9]+(|\\.[0-9]*))[ \t]*(mm|cm|m|)[ \t]+(y[ ]?=[ ]?|)((\\+|-|)[0-9]+(|\\.[0-9]*))[ \t]*(mm|cm|m|)[ \t]+((theta|t)[ ]?=[ ]?|)((\\+|-|)[0-9]+(|\\.[0-9]*))[ \t]*(°|)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_odo_pos.re_nsub < PMATCH_MAX); // pmatch[0] = all

	// ASSERV --------------------------------------------------------
	
	regex_t reg_asserv_distance;
	assert(!regcomp(&reg_asserv_distance, "^(asserv[ \t]+|)(distance|dist)[ \t]+((\\+|-|)[0-9]+(|\\.[0-9]*))[ \t]*(mm|cm|m|)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_asserv_distance.re_nsub < PMATCH_MAX); // pmatch[0] = all

	regex_t reg_asserv_rotate;
	assert(!regcomp(&reg_asserv_rotate, "^(asserv[ \t]+|)(rotate|rot)[ \t]+((\\+|-|)[0-9]+(|\\.[0-9]*))[ \t]*(°|)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_asserv_rotate.re_nsub < PMATCH_MAX); // pmatch[0] = all

	regex_t reg_asserv_speed;
	assert(!regcomp(&reg_asserv_speed, "^(asserv[ \t]+|)speed([ \t]+(curt)|)([ \t]+((\\+|-|)[0-9]+))([ \t]+((\\+|-|)[0-9]+))[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_asserv_speed.re_nsub < PMATCH_MAX); // pmatch[0] = all

	regex_t reg_asserv_stop;
	assert(!regcomp(&reg_asserv_stop, "^stop[ \t]*\n$",
				REG_EXTENDED | REG_ICASE | REG_NOSUB));

	regex_t reg_asserv_done;
	assert(!regcomp(&reg_asserv_done, "^(asserv[ \t]+|)done[ \t]*\n$",
				REG_EXTENDED | REG_ICASE | REG_NOSUB));
	
	regex_t reg_asserv_status;
	assert(!regcomp(&reg_asserv_status, "^asserv[ \t]+(broadcast[ \t]+|bc[ \t]+|)(on|off|1|0)[ \t]*\n$",
				REG_EXTENDED | REG_ICASE));
	assert(reg_asserv_status.re_nsub < PMATCH_MAX); // pmatch[0] = all

	// ---------------------------------------------------------------

    while (1) {

		packet.length = 0;
		fgets(line, LINE_LENGTH, stream);
		
		do {
			// ARM & SUIVEUR -------------------------------------------------

			result = regexec(&reg_reset, line, 0, 0, 0); // RESET
			if (!result) {
				packet.id = 127;
				send = 1; 
				break;
			}
			
			// ALIM ----------------------------------------------------------
			
			
			
			// CAPTEURS ------------------------------------------------------

			result = regexec(&reg_sonar_echo, line, reg_sonar_echo.re_nsub+1, pmatch, 0); // SONAR ECHO
			if (!result) {
				packet.id = 320;
				start = pmatch[1].rm_so; end = pmatch[1].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "2") == 0) {
					packet.id |= 32;
				}
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "under") == 0) {
					packet.id |= 1;
				}
				start = pmatch[5].rm_so; end = pmatch[5].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "edge") == 0) {
					packet.id |= 2;
				}
				start = pmatch[3].rm_so; end = pmatch[3].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				int echo;
				if (sscanf(buffer, "%u", &echo) == 1 && echo < 65536) {
					uint16_t e = echo;
					packet.b[0] = ((char*)&e)[0];
					packet.b[1] = ((char*)&e)[1];
					packet.length = 2;
					send = 1; 
				}
				break;
			}
			
			result = regexec(&reg_sonar_request, line, reg_sonar_request.re_nsub+1, pmatch, 0); // SONAR REQUEST
			if (!result) {
				packet.id = 324;
				start = pmatch[1].rm_so; end = pmatch[1].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcmp(buffer, "2") == 0) {
					packet.id |= 32;
				}
				send = 1; 
				break;
			}

			result = regexec(&reg_sonar_threshold, line, reg_sonar_threshold.re_nsub+1, pmatch, 0); // SONAR THRESHOLD
			if (!result) {
				packet.id = 328;
				start = pmatch[1].rm_so; end = pmatch[1].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "2") == 0) {
					packet.id |= 32;
				}
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				int threshold;
				if (sscanf(buffer, "%u", &threshold) == 1 && threshold < 65536) {
					uint16_t t = threshold;
					packet.b[0] = ((char*)&t)[0];
					packet.b[1] = ((char*)&t)[1];
					packet.length = 2;
					send = 1; 
				}
				break;
			}
			
			result = regexec(&reg_sonar_status, line, reg_sonar_status.re_nsub+1, pmatch, 0); // SONAR ON/OFF
			if (!result) {
				packet.id = 332;
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcmp(buffer, "2") == 0) {
					packet.id |= 32;
				}
				start = pmatch[3].rm_so; end = pmatch[3].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "on") == 0 || strcmp(buffer, "1") == 0) {
					packet.id |= 1;
				}
				send = 1; 
				break;
			}
			
			result = regexec(&reg_bump, line, reg_odo_status.re_nsub+1, pmatch, 0); // BUMP
			if (!result) {
				packet.id = 256;
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "on") == 0 || strcmp(buffer, "1") == 0) {
					packet.id |= 1;
				}
				start = pmatch[1].rm_so; end = pmatch[1].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "front") == 0 || strcmp(buffer, "2") == 0) {
					packet.id |= 2;
				}
				send = 1; 
				break;
			}

			// ODOMÉTRIE -----------------------------------------------------

			result = regexec(&reg_odo_request, line, 0, 0, 0); // ODO REQUEST
			if (!result) {
				packet.id = 513;
				send = 1; 
				break;
			}

			result = regexec(&reg_odo_status, line, reg_odo_status.re_nsub+1, pmatch, 0); // ODO ON/OFF
			if (!result) {
				packet.id = 514;
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "on") == 0 || strcmp(buffer, "1") == 0) {
					packet.id |= 1;
				}
				send = 1; 
				break;
			}
			
			result = regexec(&reg_odo_pos, line, reg_odo_pos.re_nsub+1, pmatch, 0); // ODO POS
			if (!result) {
				int set = 0;
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "set") == 0) {
					set = 1;
				}
				int x, y;
				double theta;
				// x
				start = pmatch[8].rm_so; end = pmatch[8].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (!sscanf(buffer, "%d", &x)) send = -1;
				start = pmatch[11].rm_so; end = pmatch[11].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				x = x * (multiplier(buffer, &send)/10);
				// y
				start = pmatch[13].rm_so; end = pmatch[13].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (!sscanf(buffer, "%d", &y)) send = -1;
				start = pmatch[16].rm_so; end = pmatch[16].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				y *= (multiplier(buffer, &send)/10);
				// theta
				start = pmatch[19].rm_so; end = pmatch[19].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (!sscanf(buffer, "%lf", &theta)) send = -1;
				theta *= 100.0; // convertion en centième de degré
				if (send == 0 && -32769 < x && x < 32768
						&& -32769 < y && y < 32768 && 0 <= theta && theta <= 65536) {
					int16_t _x = x;
					int16_t _y = y;
					uint16_t _theta = theta;
					packet.length = 6;
					packet.b[0] = ((char*)&_x)[0];
					packet.b[1] = ((char*)&_x)[1];
					packet.b[2] = ((char*)&_y)[0];
					packet.b[3] = ((char*)&_y)[1];
					packet.b[4] = ((char*)&_theta)[0];
					packet.b[5] = ((char*)&_theta)[1];
					if (set) {
						packet.id = 517;
					} else {
						packet.id = 516;
					}
					send = 1;
				}
				/*int i; char format[32];
				for (i = 0 ; i < reg_odo_pos.re_nsub+1 ; i++) {
					start = pmatch[i].rm_so; end = pmatch[i].rm_eo; size = end - start;
					//printf("size: %d\n", size);
					assert(size<BUF_LENGTH);
					strncpy(buffer, &line[start], size);
					buffer[size] = '\0';
					printf("i=%d, buffer: «%s»\n", i, buffer);
				}*/
				/*double angle;
				sscanf(buffer, "%lf", &angle);
				angle = round(angle * 100 * getValue(ROTATE_RATIO));
				if (angle < 32768 && angle >= -32768) {
					int16_t a = angle;
					packet.b[0] = ((uint8_t*)&a)[0];
					packet.b[1] = ((uint8_t*)&a)[1];
					packet.id = 1026;
					send = 1;
				}*/
				break;
			}

			// ASSERV --------------------------------------------------------
			
			// ASSERV DISTANCE
			result = regexec(&reg_asserv_distance, line, reg_asserv_distance.re_nsub+1, pmatch, 0);
			if (!result) {
				start = pmatch[3].rm_so; end = pmatch[3].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				double distance;
				sscanf(buffer, "%lf", &distance);
				start = pmatch[6].rm_so; end = pmatch[6].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				distance *= multiplier(buffer, &send);
				if (send == 0) {
					distance = round(distance * getValue(DISTANCE_RATIO));
					if (distance < 32768 && distance >= -32768) {
						packet.length = 2;
   						int16_t d = distance;
						packet.b[0] = ((uint8_t*)&d)[0];
						packet.b[1] = ((uint8_t*)&d)[1];
						packet.id = 1025;
						send = 1;
					}
				}
				break;
			}
			
			// ASSERV ROTATE
			result = regexec(&reg_asserv_rotate, line, reg_asserv_rotate.re_nsub+1, pmatch, 0);
			if (!result) {
				start = pmatch[3].rm_so; end = pmatch[3].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				double angle;
				if (!sscanf(buffer, "%lf", &angle)) send = -1;
				angle = round(angle * getValue(ROTATE_RATIO));
				printf("angle: %lf\n", angle);
				if (send == 0 && angle < 32768 && angle >= -32768) {
					packet.length = 2;
					int16_t a = angle;
					packet.b[0] = ((uint8_t*)&a)[0];
					packet.b[1] = ((uint8_t*)&a)[1];
					packet.id = 1026;
					send = 1;
				}
				break;
			}
			
			// ASSERV SPEED
			result = regexec(&reg_asserv_speed, line, reg_asserv_speed.re_nsub+1, pmatch, 0);
			if (!result) {
				int curt = 0;
				start = pmatch[3].rm_so; end = pmatch[3].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "curt") == 0) {
					curt = 1;
				}
				int vg, vd;
				start = pmatch[5].rm_so; end = pmatch[5].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (!sscanf(buffer, "%d", &vg)) send = -1;
				start = pmatch[8].rm_so; end = pmatch[8].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (!sscanf(buffer, "%d", &vd)) send = -1;
				if (send == 0 && -81 < vg && vg < 81 && -81 < vd && vd < 81) {
					packet.length = 2;
					packet.b[0] = vg;
					packet.b[1] = vd;
					if (curt) {
						packet.id = 1029;
					} else {
						packet.id = 1032;
					}
					send = 1;
				}
				/*int i; char format[32];
				for (i = 0 ; i < reg_asserv_speed.re_nsub ; i++) {
					start = pmatch[i].rm_so; end = pmatch[i].rm_eo; size = end - start;
					printf("size: %d\n", size);
					assert(size<BUF_LENGTH);
					strncpy(buffer, &line[start], size);
					buffer[size] = '\0';
					printf("i=%d, buffer: «%s»\n", i, buffer);
				}*/
				/*double angle;
				sscanf(buffer, "%lf", &angle);
				angle = round(angle * 100 * getValue(ROTATE_RATIO));
				if (angle < 32768 && angle >= -32768) {
					int16_t a = angle;
					packet.b[0] = ((uint8_t*)&a)[0];
					packet.b[1] = ((uint8_t*)&a)[1];
					packet.id = 1026;
					send = 1;
				}*/
				break;
			}

			result = regexec(&reg_asserv_stop, line, 0, 0, 0); // ASSERV STOP
			if (!result) {
				packet.id = 1051; // FIXME
				send = 1; 
				break;
			}

			result = regexec(&reg_asserv_done, line, 0, 0, 0); // ASSERV DONE
			if (!result) {
				packet.id = 1028;
				send = 1; 
				break;
			}

			result = regexec(&reg_asserv_status, line, reg_asserv_status.re_nsub+1, pmatch, 0); // ASSERV ON/OFF
			if (!result) {
				start = pmatch[2].rm_so; end = pmatch[2].rm_eo; size = end - start;
				assert(size<BUF_LENGTH);
				strncpy(buffer, &line[start], size);
				buffer[size] = '\0';
				if (strcasecmp(buffer, "on") == 0 || strcmp(buffer, "1") == 0) {
					packet.id = 1030;
				} else {
					packet.id = 1031;
				}
				send = 1; 
				break;
			}
			
			// ---------------------------------------------------------------

		} while (0);

		if (send == 1) {
			receiv((unsigned int)pthread_self(), packet);
			send = 0;
		}
        /*fgets(line, 256, stream);
        packet.length = sscanf(line, "%d%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu", &packet.id,
                packet.b, packet.b+1, packet.b+2, packet.b+3, packet.b+4, packet.b+5, packet.b+6, packet.b+7) - 1;
        if (packet.length >= 0 && packet.id < 2048) {
            receiv((unsigned int)pthread_self(), packet);
        }*/
    }
}
