#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>

#include <sys/wait.h>

#include "functions.h"

/* Default parameters */
#define DEFAULT_DEVICE "/dev/ttyUSB0"
#define DEFAULT_SPEED 19200

#define DEFAULT_HOST "r2d2"
#define DEFAULT_PORT "7771"

void show_help(char * cmd);

int main(int argc, char * argv[])
{
	char * env;
	int option, device_fd, socket_fd;

	static char * device = DEFAULT_DEVICE;
	char * opt_device = NULL;

	int speed = DEFAULT_SPEED;

	static char * host = DEFAULT_HOST;
	char * opt_host = NULL;

	static char * port = DEFAULT_PORT;
	char * opt_port = NULL;

	/* ENV */
	env = getenv("CANGATEWAY_DEVICE");
	if ((env != NULL) && (strlen(env) != 0)) {
		opt_device = malloc(strlen(env) + 1);
		if (opt_device == NULL) {
			perror("malloc");
			exit(1);
		}
		strcpy(opt_device, env);
		device = opt_device;
	}
	env = getenv("CANGATEWAY_SPEED");
	if ((env != NULL) && (strlen(env) != 0)) {
		sscanf(env, "%d", &speed);
	}
	env = getenv("CANGATEWAY_HOST");
	if ((env != NULL) && (strlen(env) != 0)) {
		opt_host = malloc(strlen(env) + 1);
		if (opt_host == NULL) {
			perror("malloc");
			exit(1);
		}
		strcpy(opt_host, env);
		host = opt_host;
	}
	env = getenv("CANGATEWAY_PORT");
	if ((env != NULL) && (strlen(env) != 0)) {
		opt_port = malloc(strlen(env) + 1);
		if (opt_port == NULL) {
			perror("malloc");
			exit(1);
		}
		strcpy(opt_port, env);
		port = opt_port;
	}

	/* OPT */
	opterr = 1;
	while (1) {
		option = getopt(argc, argv, "D:H:P:S:h");
		if (option == -1)
			break;
		switch (option) {
			case 'D':
				opt_device = malloc(strlen(optarg) + 1);
                if (opt_device == NULL) {
                    perror("malloc");
                    exit(1);
                }
                strcpy(opt_device, optarg);
                device = opt_device;
				break;
			case 'S':
				if (sscanf(optarg, "%d", &speed) != 1) {
					fprintf(stderr, "Bad argument for '-S' option\n");
					show_help(argv[0]);
					exit(1);
				}
				break;
			case 'H':
				opt_host = malloc(strlen(optarg) + 1);
                if (opt_host == NULL) {
                    perror("malloc");
                    exit(1);
                }
                strcpy(opt_host, optarg);
                host = opt_host;
				break;
			case 'P':
				opt_port = malloc(strlen(optarg) + 1);
                if (opt_port == NULL) {
                    perror("malloc");
                    exit(1);
                }
                strcpy(opt_port, optarg);
                port = opt_port;
				break;
			case 'h':
				show_help(argv[0]);
				exit(0);
			case '?':
				show_help(argv[0]);
				exit(1);
			default:
				break;
		}
	}

	printf("Gateway settings:\n");
	printf("\tSerial device : %s\n", device);
	printf("\tSpeed : %d\n", speed);
	printf("\tSocket  : %s:%s\n", host, port);

	if ((device_fd = getttyfd(device, speed)) < 0) {
		fprintf(stderr, "error: getttyfd(%s, %d) failed\n", device, speed);
		exit(1);
	}
	if ((socket_fd = getsockfd(host, port)) < 0) {
		fprintf(stderr, "error: getsockfd(%s, %s) failed\n", host, port);
		exit(1);
	}

	int fd[2][2] = {{ device_fd, socket_fd }, { socket_fd, device_fd }};
	if (multipipe(2, fd)) {
		fprintf(stderr, "error: an error occured during data transfer\n");
		exit(1);
	}

	return 0;
}

void show_help(char * cmd)
{
	printf("Usage: %s [-D <device>] [-H <host>] [-P <port>] [-h]\n", cmd);
	printf("\tD: set device to open\n");
	printf("\tS: set speed transmission\n");
	printf("\tH: set host to connect\n");
	printf("\tP: set port to connect\n");
	printf("\th: show this help\n");
}
