#include "libcan.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define CTX_MAX 8

extern int getsockfd(const char * host, const char * port);
void recv(unsigned int, can_t packet);
int parse(char * s);
void help(char * cmd);

typedef struct {
	unsigned int id;
	can_ctx * ctx;
} stream;


can_ctx * ctx[CTX_MAX];
int ctxno = 0;

int main(int argc, char ** argv)
{
	printf("Can bridge - version 2.0\n");
	int i;
	for(i = 1 ; i < argc && i < CTX_MAX ; i++) {
		if (parse(argv[i]) < 0) {
			fprintf(stderr, "error with argument: \"%s\"\n", argv[i]);
			help(argv[0]);
			return EXIT_FAILURE;
		}
	}

	if (i == CTX_MAX) {
		fprintf(stderr, "Warning: too many arguments, some was ignored\n");
	} else if (i == 1) {
		help(argv[0]);
		return EXIT_SUCCESS;
	}

	printf("Working …\n");

	pause();
}

int parse(char * s)
{
	int n;
	char format[32];
	char server[128];
	char port[16];

	n = sscanf(s, "%32[^@]@%128[^:]:%16s", format, server, port);
	if (n != 3) {
		fprintf(stderr, "unable to split \"%s\"\n", s);
		return -1;
	}

	int fd;
	if ((fd = getsockfd(server, port)) < 0) {
		fprintf(stderr, "getsockfd failed\n");
		return -1;
	}

	if (can_init(&(ctx[ctxno++]), fd, format, recv) < 0) {
		fprintf(stderr, "can_init failed\n");
		return -1;
	}
}

void help(char * cmd)
{
	printf("Usage: %s [STREAM]\nwhere STREAM := FORMAT@SERVER:PORT\n", cmd);
}

void recv(unsigned int id, can_t packet)
{
	int i;
	for (i = 0 ; i < ctxno ; i++) {
		if (can_id(ctx[i]) != id) {
			can_send(ctx[i], packet);
		}
	}
}
