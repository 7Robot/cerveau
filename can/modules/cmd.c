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

#include "ini.h"

#define PMATCH_MAX 32
#define BUF_LENGTH 256
#define LINE_LENGTH 256

struct var {
	const char * section;
    const char * name;
	double value;
};

#define MATCH(s, n) strcasecmp(section, s) == 0 && strcasecmp(name, n) == 0
#define MAX(x, y) (x<y)?y:x

static int parse(void * user,
		const char * section,
		const char * name,
		const char * value);
double getValue(const char * section, const char * name);
int strword(char * dest, char * src, int * spos);

int can_write(int fd, can_t packet)
{	
    char output[256];

	int carte = packet.id >> 7;
	int id = packet.id & 127;

	int send = 1;

	if (((carte & 2) == 2) || (carte == 1 && ((id & 7) == 7))) { // CAPTEURS -----------------------------
        if ((id & 64) == 64) { // rangefinder
            if ((id & 32) == 32) { // value
                sprintf(output, "RANGEFINDER %d VALUE %hu %s %s\n",
                        (id & 7) + 1, ((uint16_t*)packet.b)[0],
                        ((id & 16) == 16)?"UNDER":"OVER",
                        ((id & 8) == 8)?"EDGE":"");
            } else if ((id & 16) == 16) { // broadcast
                sprintf(output, "RANGEFINDER %d %s\n", (id & 7) + 1,
                        ((id & 8) == 8)?"UNMUTE":"MUTE");
            } else if ((id & 8) == 8) { // threshold
                sprintf(output, "RANGEFINDER %d THRESHOLD %hu\n", (id & 7) + 1,
                        ((uint16_t*)packet.b)[0]);
            } else { // request
                sprintf(output, "RANGEFINDER %d REQUEST\n", (id & 7) + 1);
            }
        } else if ((id & 112) == 16) { //bump
            int bumpid = (id & 3) + 1;
            char bumpname[64];
            if (bumpid == 1) {
                strcpy(bumpname, "BACK");
            } else if (bumpid == 2) {
                strcpy(bumpname, "FRONT");
            } else if (bumpid == 3) {
                strcpy(bumpname, "ALIM");
            } else if (bumpid == 4) {
                strcpy(bumpname, "LEASH");
            } else {
                sprintf(bumpname, "%d", bumpid);
            }
            sprintf(output, "BUMP %s %s\n",
                    bumpname,
                    (id&8)==8?"CLOSE":"OPEN");
        } else {
            send = 0;
        }
    } else if (carte == 0) { // ARM & SUIVEUR ---------------------------------
		if (id == 127) { // reset
			sprintf(output, "RESET\n");
		} else {
			send = 0;
		}
	} else if (carte == 1) { // ALIM (tourelle) ----------------------
        if ((id & 124) == 64) {
            if (id == 65) {
                sprintf(output, "BATTERY REQUEST\n");
            } else if (id = 66) {
                sprintf(output, "BATTERY ANSWER %.2lf\n", ((uint16_t*)packet.b)[0] / getValue("alim", "battery"));
            } else {
                send = 0;
            }
        } else if ((id & 96) == 96) {
            if ((id & 12) == 0) {
                sprintf(output, "AX %d %s REQUEST\n",
                        (id & 3) + 1,
                        ((id & 16) == 16)?"ANGLE":"TORQUE");
            } else if ((id & 8) == 8) {
                sprintf(output, "AX %d %s %s %hu\n",
                        (id & 3) + 1,
                        ((id & 16) == 16)?"ANGLE":"TORQUE", 
                        ((id & 4) == 4)?"SET":"ANSWER",
                        ((uint16_t*)packet.b)[0]);
            } else {
                send = 0;
            }
        } else if ((id & 112) == 0){
            if ((id & 15) == 4) {
                sprintf(output, "TURRET REQUEST\n");
            } else if ((id & 15) == 5) {
                sprintf(output, "TURRET ANSWER"); 
                int i;
                for (i = 0 ; i < 4 ; i++) {
                    if (packet.length > 1) {
                        sprintf(output+strlen(output), "\t%hhu %hhu", packet.b[2*i], packet.b[2*i+1]);
                        packet.length -= 2;
                    }
                }
                sprintf(output+strlen(output), "\n");
            } else if ((id & 14) == 6) {
                sprintf(output, "TURRET %s\n", (id&1)==1?"UNMUTE":"MUTE");
            } else if ((id & 14) == 8) {
                sprintf(output, "TURRET %s\n", (id&1)==1?"ON":"OFF");
            } else {
                send = 0;
            }
        } else {
            send = 0;
        }
	} else if (carte == 4) { // ODOMÉTRIE ----------------------------
        if (id == 1) {
			sprintf(output, "ODO REQUEST\n");
        } else if ((id & 126) == 2) {
			sprintf(output, "ODO %s\n", (id&1)==1?"UNMUTE":"MUTE");
        } else if ((id & 126) == 4) {
			sprintf(output, "ODO %s %+hd %+hd %hu\n", (id&1)==1?"SET":"POS",
                    ((int16_t*)packet.b)[0],
                    ((int16_t*)packet.b)[1],
                    ((uint16_t*)packet.b)[2]);
		} else {
			send = 0;
		}
	} else if (carte == 8) { // ASSERV ------------------------------
		if (id == 1) {
            int distance;
            if (((int16_t*)packet.b)[0] > 0) {
    			distance = ((int16_t*)packet.b)[0] / getValue("asserv", "fwd-pos");
            } else {
    			distance = ((int16_t*)packet.b)[0] / getValue("asserv", "fwd-neg");
            }
			sprintf(output, "ASSERV DIST %+d\n", distance);
		} else if (id == 2) {
			int angle;
            if (((int16_t*)packet.b)[0] < 0) {
                angle = ((int16_t*)packet.b)[0] / getValue("asserv", "rot-pos");
            } else {
                angle = ((int16_t*)packet.b)[0] / getValue("asserv", "rot-neg");
            }
			sprintf(output, "ASSERV ROT %+d°\n", angle);
		} else if ((id & 126) == 8) {
			sprintf(output, "ASSERV SPEED %+hhd %+hhd %s\n",
                    packet.b[0], packet.b[1],
                    (id&1==1)?"":"CURT");
		} else if ((id & 126) == 4) {
			sprintf(output, "ASSERV %s\n", (id&1==1)?"ON":"OFF");
		} else if (id  == 16) {
			sprintf(output, "ASSERV DONE\n");
		} else if (id == 17) {
            int distance;
            if (((int16_t*)packet.b)[0] > 0) {
    			distance = ((int16_t*)packet.b)[0] / getValue("asserv", "fwd-pos");
            } else {
    			distance = ((int16_t*)packet.b)[0] / getValue("asserv", "fwd-neg");
            }
			sprintf(output, "ASSERV INT DIST %hd\n", distance);
		} else if (id == 18) {
			int angle;
            if (((int16_t*)packet.b)[0] < 0) {
                angle = ((int16_t*)packet.b)[0] / getValue("asserv", "rot-pos");
            } else {
                angle = ((int16_t*)packet.b)[0] / getValue("asserv", "rot-neg");
            }
			sprintf(output, "ASSERV INT ROT %hd\n", angle);
        } else if (id == 19) {
            sprintf(output, "ASSERV TICKS RESET\n");
        } else if (id == 20) {
            sprintf(output, "ASSERV TICKS REQUEST\n");
        } else if (id == 21) {
            int distance;
            if (((int32_t*)packet.b)[0] > 0) {
    			distance = ((int32_t*)packet.b)[0] / getValue("asserv", "fwd-pos");
            } else {
    			distance = ((int32_t*)packet.b)[0] / getValue("asserv", "fwd-neg");
            }
            sprintf(output, "ASSERV TICKS ANSWER %d\n", distance);
        } else if (id == 127) {
            sprintf(output, "ASSERV STOP\n");
		} else {
			send = 0;
		}
	} else {
		send = 0;
	}
   
	if (send) {
		write(fd, output, strlen(output));
    	fsync(fd);
	}

    return 0;
}

void can_listen(FILE * stream, void(*receiv)(unsigned int, can_t))
{
    can_t packet;
    char line[LINE_LENGTH];
	char buffer[BUF_LENGTH];
	int send = 0;
    int pos;

    while (1) {

		packet.length = 0;
		fgets(line, LINE_LENGTH, stream);
        
        pos = 0; send = 1;
        strword(buffer, line, &pos);
        if (!strcasecmp(buffer, "reset")) {
            packet.id = 127;
        } else if (!strcasecmp(buffer, "odo")) {
            if (!strword(buffer, line, &pos)) {
                printf("Warning: « odo » needs at least one argument\n");
                send = 0;
            } else if (!strcasecmp(buffer, "request")) {
                packet.id = 513;
            } else if (!strcasecmp(buffer, "mute")) {
                packet.id = 514;
            } else if (!strcasecmp(buffer, "unmute")) {
                packet.id = 515;
            } else if (!strcasecmp(buffer, "pos")
                    || !strcasecmp(buffer, "set")) {
                if (!strcasecmp(buffer, "pos")) {
                    packet.id = 516;
                } else {
                    packet.id = 517;
                }
                int16_t coord[3];
                int i;
                for (i = 0 ; i < 3 ; i++) {
                    if (!strword(buffer, line, &pos)) {
                        printf("Warning: bag arguments for « odo pos/set »\n");
                        send = 0;
                        break;
                    }
                    coord[i] = atoi(buffer);
                }
                if (send) {
                    packet.length = 6;
                    packet.b[0] = ((char*)&coord[0])[0];
                    packet.b[1] = ((char*)&coord[0])[1];
                    packet.b[2] = ((char*)&coord[1])[0];
                    packet.b[3] = ((char*)&coord[1])[1];
                    packet.b[4] = ((char*)&coord[2])[0];
                    packet.b[5] = ((char*)&coord[2])[1];
                }
            } else {
                printf("Warning: « odo » can't be followed by « %s »\n", buffer);
                send = 0;
            }
        } else if (!strcasecmp(buffer, "asserv")) {
            if (!strword(buffer, line, &pos)) {
                printf("Warning: « asserv » needs at least one argument\n");
                send = 0;
            } else if (!strcasecmp(buffer, "on")) {
                packet.id = 1029;
            } else if (!strcasecmp(buffer, "off")) {
                packet.id = 1028;
            } else if (!strcasecmp(buffer, "stop")) {
                packet.id = 1151;
            } else if (!strcasecmp(buffer, "dist")) {
                int16_t dist;
                if (!strword(buffer, line, &pos)) {
                    printf("Warning: bag arguments for « asserv dist »\n");
                    send = 0;
                }
                int d = atoi(buffer);
                if (d > 0) {
                    d *= getValue("asserv", "fwd-pos");
                } else {
                    d *= getValue("asserv", "fwd-neg");
                }
                dist = d;
                packet.length = 2;
                packet.b[0] = ((char*)&dist)[0];
                packet.b[1] = ((char*)&dist)[1];
                packet.id = 1025;
            } else if (!strcasecmp(buffer, "done")) {
                packet.id = 1040;
            } else if (!strcasecmp(buffer, "rot")) {
                int16_t angle;
                if (!strword(buffer, line, &pos)) {
                    printf("Warning: bag arguments for « asserv rot »\n");
                    send = 0;
                }
                int a = atoi(buffer);
                if (a > 0) {
                    a *= getValue("asserv", "rot-pos");
                } else {
                    a *= getValue("asserv", "rot-neg");
                }
                angle = a;
                packet.length = 2;
                packet.b[0] = ((char*)&angle)[0];
                packet.b[1] = ((char*)&angle)[1];
                packet.id = 1026;
            } else if (!strcasecmp(buffer, "speed")) {
                int8_t vg, vd;
                if (!strword(buffer, line, &pos)) {
                    printf("Warning: bag arguments for « asserv speed »\n");
                    send = 0;
                }
                vg = atoi(buffer);
                packet.length = 2;
                if (!strword(buffer, line, &pos)) {
                    printf("Warning: bag arguments for « asserv speed »\n");
                    send = 0;
                }
                vd = atoi(buffer);
                packet.b[0] = vg;
                packet.b[1] = vd;
                if (strword(buffer, line, &pos) && strcasecmp(buffer, "curt") == 0) {
                    packet.id = 1032;
                } else {
                    packet.id = 1033;
                }
            } else if (!strcasecmp(buffer, "int")) {
                char * errmsg = "Warning: « asserv int » must be followed by « dist » or « rot », then by an integer\n";
                if (!strword(buffer, line, &pos)) {
                    printf("%s", errmsg);
                    send = 0;
                }
                if (!strcasecmp(buffer, "dist")) {
                    packet.id = 1041;
                } else if (!strcasecmp(buffer, "rot")) {
                    packet.id = 1042;
                } else {
                    printf("%s", errmsg);
                    send = 0;
                }
                if (send) {
                    if (!strword(buffer, line, &pos)) {
                        printf("%s", errmsg);
                        send = 0;
                    }
                    int v = atoi(buffer);
                    if (packet.id == 1041) {
                        if (v > 0) {
                            v *= getValue("asserv", "fwd-pos");
                        } else {
                            v *= getValue("asserv", "fwd-neg");
                        }
                    } else {
                        if (v > 0) {
                            v *= getValue("asserv", "rot-pos");
                        } else {
                            v *= getValue("asserv", "rot-neg");
                        }
                    }
                    int16_t value = v;
                    packet.length = 2;
                    packet.b[0] = ((uint8_t*)&value)[0];
                    packet.b[1] = ((uint8_t*)&value)[1];
                }
            } else if (!strcasecmp(buffer, "ticks")) {
                if (!strword(buffer, line, &pos)) {
                    printf("Warning: « asserv ticks » need argument\n");
                    send = 0;
                }
                if (!strcasecmp(buffer, "reset")) {
                    packet.id = 1043;
                } else if (!strcasecmp(buffer, "request")) {
                    packet.id = 1044;
                } else if (!strcasecmp(buffer, "answer")) {
                    if (!strword(buffer, line, &pos)) {
                        printf("Warning: « asserv ticks answer » need an integer argument\n");
                        send = 0;
                    }
                    int32_t answer = atoi(buffer);
                    if (answer > 0) {
                        answer *= getValue("asserv", "fwd-pos");
                    } else {
                        answer *= getValue("asserv", "fwd-neg");
                    }
                    int i;
                    for (i = 0; i < 4 ; i++) {
                        packet.b[i] = ((int8_t*)&answer)[i];
                    }
                    packet.length = 4;
                    packet.id = 1045;
                } else {
                    printf("Warning: bag arguments for « asserv ticks »\n");
                    send = 0;
                }
            } else {
                printf("Warning: « asserv » can't be followed by « %s »\n", buffer);
                send = 0;
            }
        } else if (!strcasecmp(buffer, "rangefinder")) {
            packet.id = 320;
            int rfid;
            char * errmsg = "Warning: « rangefinder » must be followed by an integer between 1 and 8, then « value », « request », « mute », « unmute » or « threshold »\n";
            if (!strword(buffer, line, &pos) || !(rfid = atoi(buffer)) || !strword(buffer, line, &pos)) {
                printf(errmsg);
                send = 0;
            } else {
                if (rfid > 0 && rfid < 8) {
                    packet.id += rfid - 1;
                } else if (rfid == 8) {
                    packet.id = 199;
                }
                if (!strcasecmp(buffer, "value")) {
                    packet.id += 32;
                    errmsg = "Warning: « rangefinder %d value » must be followed by a distance value, then « under » or « other », then optionally « edge »\n";
                    if (!strword(buffer, line, &pos)) {
                        printf(errmsg, rfid);
                        send = 0;
                    } else {
                        int16_t value = atoi(buffer);
                        packet.b[0] = ((int8_t*)&value)[0];
                        packet.b[1] = ((int8_t*)&value)[1];
                        packet.length = 2;
                        int under;
                        if (!strword(buffer, line, &pos)
                                || ((under = strcasecmp(buffer, "over")) && strcasecmp(buffer, "under"))) {
                            printf(errmsg, rfid);
                            send = 0;
                        } else {
                            if (under) packet.id += 16;
                            if (strword(buffer, line, &pos) && !strcasecmp(buffer, "edge"))
                                packet.id += 8;
                        }
                    }
                } else if (!strcasecmp(buffer, "threshold")) {
                    packet.id += 8;
                    if (!strword(buffer, line, &pos)) {
                        printf("Warning: « rangefinder %d threshold » must be followed by a distance value\n", rfid);
                        send = 0;
                    } else {
                        int16_t value = atoi(buffer);
                        packet.b[0] = ((int8_t*)&value)[0];
                        packet.b[1] = ((int8_t*)&value)[1];
                        packet.length = 2;
                    }
                } else if (!strcasecmp(buffer, "mute")) {
                    packet.id += 16;
                } else if (!strcasecmp(buffer, "unmute")) {
                    packet.id += 24;
                } else if (strcasecmp(buffer, "request")) {
                    printf(errmsg);
                    send = 0;
                }
            }
        } else if (!strcasecmp(buffer, "bump")) {
            int close, bid;
            if (!strword(buffer, line, &pos) || (bid = atoi(buffer)) < 1 || bid > 8
                    || !strword(buffer, line, &pos) || ((close = strcasecmp(buffer, "open")) && strcasecmp(buffer, "close"))) {
                printf("Warning: « bump » must be followed by i in [1;8], then, « open » or « close »\n");
                send = 0;
            }
            packet.id = 272;
            packet.id += bid - 1;
            if (close) packet.id += 4;
        } else if (!strcasecmp(buffer, "battery")) {
            if (!strword(buffer, line, &pos)) {
                printf("Warning: « battery » must be followed by « request » or « answer »\n");
                send = 0;
            } else {
                if (!strcasecmp(buffer, "request")) {
                    packet.id = 193;
                } else if (!strcasecmp(buffer, "answer")) {
                    if (!strword(buffer, line, &pos)) {
                        printf("Warning: « battery answer » must be followed by an integer\n");
                        send = 0;
                    } else {
                        packet.id = 194;
                        int value = atoi(buffer) * getValue("alim", "battery");
                        packet.length = 2;
                        packet.b[0] = ((uint8_t*)&value)[0];
                        packet.b[1] = ((uint8_t*)&value)[1];
                    }
                } else {
                    printf("Warning: « battery » must be followed by « request » or « answer »\n");
                    send = 0;
                }
            }
        } else if (!strcasecmp(buffer, "ax")) {
            if (!strword(buffer, line, &pos)) {
                printf("Warning: « ax » must be followed by an id in [1;8]\n");
                send = 0;
            } else {
                packet.id = 224 + atoi(buffer) - 1;
                if (packet.id > 231 || packet.id < 224) {
                    printf("Warning: the ax12 ip must be in range [1;8]\n");
                    send = 0;
                } else if (!strword(buffer, line, &pos)) {
                    printf("Warning: « ax <id> » must be followed by « angle » or « torque »\n");
                    send = 0;
                } else {
                    if (!strcasecmp(buffer, "angle")) {
                        packet.id += 16;
                    } else if (strcasecmp(buffer, "torque")) {
                        printf("Warning: « ax <id> » must be followed by « angle » or « torque »\n");
                        send = 0;
                    }
                }
                if (send) {
                    if (!strword(buffer, line, &pos)) {
                        printf("Warning: « ax <id> <angle/torque> » must be followed by « request », « answer » or « set »\n");
                        send = 0;
                    } else {
                        if (strcasecmp(buffer, "request")) {
                            if (!strcasecmp(buffer, "answer")) {
                                packet.id += 8;
                            } else if (!strcasecmp(buffer, "set")) {
                                packet.id += 12;
                            } else {
                                printf("Warning: invalid argument for « ax » command\n"); 
                                send = 0;
                            }
                            if (send && !strword(buffer, line, &pos)) {
                                printf("Warning: missing argument for « ax » command\n");
                                send = 0;
                            } else {
                                packet.length = 2;
                                int value = atoi(buffer);
                                packet.b[0] = ((uint8_t*)&value)[0];
                                packet.b[1] = ((uint8_t*)&value)[1];
                            }
                        }
                    }
                }
            }
        } else if (!strcasecmp(buffer, "turret")) {
            if (!strword(buffer, line, &pos)) {
                send = 0;
            } else {
                if (!strcasecmp(buffer, "request")) {
                    packet.id = 132;
                } else if (!strcasecmp(buffer, "answer")) {
                    packet.id = 133;
                    int i, dist, angle;
                    for (i = 0; i < 4 ; i++) {
                        if (!strword(buffer, line, &pos)) {
                            break;
                        }
                        dist = atoi(buffer);
                        if (!strword(buffer, line, &pos)) {
                            break;
                        }
                        angle = atoi(buffer);
                        packet.length += 2;
                        packet.b[i*2] = dist;
                        packet.b[i*2+1] = angle;
                    }
                } else if (!strcasecmp(buffer, "mute")) {
                    packet.id = 134;
                } else if (!strcasecmp(buffer, "unmute")) {
                    packet.id = 135;
                } else if (!strcasecmp(buffer, "off")) {
                    packet.id = 136;
                } else if (!strcasecmp(buffer, "on")) {
                    packet.id = 137;
                } else {
                    send = 0;
                }
            }
        } else {
            send = 0;
        }
        /*int len;
        while((len = strword(buffer, line, &pos))) {
            printf("\t«%s»\n", buffer);
        }*/

		if (send == 1) {
			receiv((unsigned int)pthread_self(), packet);
			send = 0;
		}
    }
}

int strword(char * dest, char * src, int * spos)
{
    char in;
    int dpos = 0;
    do {
        in = src[*spos];
        if (in == ' ' || in == '\t') {
            if (dpos != 0) {
                break;
            } else {
                (*spos)++;
            }
        } else if (in == '\n' || in == '\0') {
            break;
        } else {
            dest[dpos++] = in;
            (*spos)++;
        }
    } while (1);
    dest[dpos] = '\0';
    return dpos;
}


static int parse(void * user,
		const char * section,
		const char * name,
		const char * value)
{
	struct var * var = user;
    if (MATCH(var->section, var->name)) {
        sscanf(value, "%lf", &(var->value));
        return 1;
    }
    //atoi(value);
    //strdup(value);
    return 1;
}

double getValue(const char * section, const char * name)
{
	static char * filename = NULL;
    struct var v;
    v.section = section;
    v.name = name;

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
