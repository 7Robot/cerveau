#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <arpa/inet.h>

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "server.h"

#define MAX_CONNECTION 64
#define BUF_SIZE 1024
#define ENV_SERVICE "TCPHUB_SERVICE"

int hub(const char * port);
int dispatches(int sockclientc, int * sockclient, int socksource, int r, char * buffer);
int nonblock(int fd);
void help(char * cmd);

int main(int argc, char ** argv)
{
	char * service = NULL;
	char * env;

	env = getenv(ENV_SERVICE);
	if ((env != NULL) && (strlen(env) != 0)) {
		service = malloc(strlen(env) + 1);
		if (service == NULL) {
			perror("malloc");
			return 1;
		}
		strcpy(service, env);
	}
	if (service == NULL) {
		if (argc != 2) {
			help(argv[0]);
			return 1;
		}
		service = argv[1];
	} else {
		if (argc != 1) {
			help(argv[0]);
			return 1;
		}
	}

	printf("tcphub running on port %s\n", service);
	fflush(stdout);
	if (hub(service) < 0) {
		return 1;
	}
}

int hub(const char * service)
{
	int sockserver;
	
	struct sockaddr_in address;
	socklen_t length = sizeof(struct sockaddr_in);

	if ((sockserver = create_tcp_server(NULL, service)) < 0) {
		return -1;
	}
	
	if (nonblock(sockserver) < 0) {
		return -1;
	}

	char buffer[BUF_SIZE];
	int sockclient[MAX_CONNECTION];
	int sockclientc = 0;

	int i, j, r, sock, run, dataread;

	fd_set listenfdset;

	run = 1;
	while (run) {
		FD_ZERO(&listenfdset);
		FD_SET(sockserver, &listenfdset);
		for (i = 0 ; i < sockclientc ; i++) {
			FD_SET(sockclient[i], &listenfdset);
		}

		if (select(FD_SETSIZE, &listenfdset, NULL, NULL, NULL) < 0) {
			if (errno != EINTR) {
				perror("select");
				return -1;
			} else {
				continue;
			}
		}

		if (FD_ISSET(sockserver, &listenfdset)) {
			if ((sock = accept(sockserver, (struct sockaddr*)(&address), &length)) < 0) {
				perror("accept");
				return -1;
			}
			if (nonblock(sock) < 0) {
				return -1;
			}
			if (sockclientc == MAX_CONNECTION) {
				char * toomanyco = "Sorry, no slot available, retry later\n";
				if (write(sock, toomanyco, strlen(toomanyco)) < -1) {
					perror("write");
				}
				close(sock);
			} else {
				sockclient[sockclientc++] = sock;
				fprintf(stdout, "%i connections [+1]\n", sockclientc);
				fflush(stdout);
			}
		}

		for (i = 0 ; i < sockclientc ; i++) {
			if (FD_ISSET(sockclient[i], &listenfdset)) {
				r = read(sockclient[i], buffer, BUF_SIZE);
				if (r <= 0) {
					close(sockclient[i]);
                    sockclient[i] = sockclient[--sockclientc];
					fprintf(stdout, "%i connections [-1]\n", sockclientc);
					fflush(stdout);
					if (r < 0 && errno != ECONNRESET) {
						perror("read");
						//return -1;
					}
				} else {
					if (dispatches(sockclientc, sockclient, i, r, buffer) < 0) {
						return -1;
					}
				}
			}
		}
	}
}

int dispatches(int sockclientc, int * sockclient, int socksource, int r, char * buffer)
{
	static fd_set writefdset;
	static int pending[MAX_CONNECTION];
	static char buffers[MAX_CONNECTION][BUF_SIZE];
	static int i, w, setsize;

	for (i = 0 ; i < sockclientc ; i++) {
		if (i != socksource) {
			memcpy(buffers[i], buffer, r);
			pending[i] = r;
		} else {
			pending[i] = 0;
		}
	}

	while (1) {
		setsize = 0;
		FD_ZERO(&writefdset);
		for (i = 0 ; i < sockclientc ; i++) {
			if (pending[i] > 0) {
				setsize++;
				FD_SET(sockclient[i], &writefdset);
			}
		}
		if (!setsize) {
			return 0;
		}

		if (select(FD_SETSIZE, NULL, &writefdset, NULL, NULL) < 0) {
			if (errno != EINTR) {
				perror("select");
				return -1;
			} else {
				continue;
			}
		}

		for (i = 0 ; i < sockclientc ; i++) {
			if (FD_ISSET(sockclient[i], &writefdset)) {
				if ((w = write(sockclient[i], buffers[i], pending[i])) < 0) {
					perror("write");
					close(sockclient[i]);
					if (i != --sockclientc) {
						sockclient[i] = sockclient[sockclientc];
						memmove(buffers[i], buffers[sockclientc], pending[sockclientc]);
						pending[i] = pending[sockclientc];
					}
					fprintf(stdout, "%i connections [-1]\n", sockclientc);
					fflush(stdout);
				} else {
					memmove(buffers[i], &(buffers[i][w]), pending[i] - w);
					pending[i] -= w;
				}
			}
		}
	}
}

int nonblock(int fd)
{
	int opts;
	if ((opts = fcntl(fd, F_GETFL)) < 0) {
		perror("fcntl");
		return -1;
	}
	if (fcntl(fd, F_SETFL, opts | O_NONBLOCK) < 0) {
		perror("fcntl");
		return -1;
	}
}

void help(char * cmd)
{
	printf("Usage: %s <port>\n", cmd);
}
