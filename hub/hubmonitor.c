#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
//#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <arpa/inet.h>

#include "server.h"

#define BUF_SIZE 256
#define MAX_HUB 64
#define MAX_CLIENT 16
#define PORT "13756"

//pthread_mutex_t hub_mtx;
int hub_pin[MAX_HUB];
int hub_pout[MAX_HUB];
int hub_pid[MAX_HUB];
char * hub_port[MAX_HUB];
int hub_count;
void son_sig_handler(int signo);

int add_hub(char * service);
int rm_hub(char * service);
int logpipe(int fd);
int logline(char * line);
void * run_server(void * args);
int nonblock(int fd);
int process_connection(int sock);

int main(int argc, char ** argv)
{
	printf("TCP Hub server monitor\n");

	void * rvalue;
	char * port = PORT;

	struct sigaction action;
	struct sigaction oldsate;
	action.sa_handler = son_sig_handler;
	sigemptyset(&(action.sa_mask));
	action.sa_flags = SA_RESTART;
	if (sigaction(SIGCHLD, &action, NULL) != 0) {
		perror("sigaction");
		return 1;
	}

	/*pthread_t pth;
	pthread_create(&pth, NULL, run_server, port);
	pthread_join(pth, &rvalue);*/

	if (argc > 1) {
		run_server(argv[1]);
	} else {
		run_server(port);
	}

	return 0;
}

void * run_server(void * args)
{
	int status, i, sockserver, sock;
	int client[MAX_CLIENT];
	int clientc = 0;

	struct sockaddr_in address;
	socklen_t length = sizeof(struct sockaddr_in);

	if ((sockserver = create_tcp_server(NULL, (char*)args)) < 0) {
		fprintf(stderr, "create_tcp_server failed\n");
		exit(1);
	}

	if (nonblock(sockserver) < 0) {
		exit(1);
	}

	printf("Listen on TCP port %s\n", PORT);

	if (chdir("/") < 0) {
		perror("chdir");
		exit(1);
	}

	if (fork() != 0) {
		exit(0);
	}
	if (setsid() < 0) {
		perror("setsid");
		exit(1);
	}
	if (fork() != 0) {
		exit(0);
	}
	printf("PID: %d\n", getpid());
	for (i = 0 ; i < getdtablesize() ; i++) {
		if (i != sockserver) {
			close(i);
		}
	}
	
	fd_set lfdset;

	int run = 1;
	while (run) {
		
		FD_ZERO(&lfdset);
		FD_SET(sockserver, &lfdset);
		for (i = 0 ; i < clientc ; i++) {
			FD_SET(client[i], &lfdset);
		}
		
		if (select(FD_SETSIZE, &lfdset, NULL, NULL, NULL) < 0) {
			if (errno != EINTR) {
				perror("select");
				exit(1);
			} else {
				continue;
			}
		}

		if (FD_ISSET(sockserver, &lfdset)) {
			if ((sock = accept(sockserver, (struct sockaddr*)(&address), &length)) < 0) {
				perror("accept");
				continue;
			}
			if (nonblock(sock) < 0) {
				close(sock);
				continue;
			}
			if (clientc == MAX_CLIENT) {
				char * toomanyco = "Sorry, no slot available, retry later\n";
				if (write(sock, toomanyco, strlen(toomanyco)) < 0) {
					perror("write");
				}
				close(sock);
			} else {
				client[clientc++] = sock;
				//fprintf(stdout, "%i connections [+1]\n", clientc);
				//fflush(stdout);
				char * motd = "Welcom to TCP Hub monitor.\nType 'help' for help.\n> ";
				if (write(sock, motd, strlen(motd)) < 0) {
					perror("write");
				}
			}
		}
		for (i = 0 ; i < clientc ; i++) {
			if (FD_ISSET(client[i], &lfdset)) {
				if (process_connection(client[i]) < 0) {
					if (shutdown(client[i], SHUT_RDWR) < 0) {
						perror("shutdown");
					}
					close(client[i]);
					client[i] = client[--clientc];
					//fprintf(stdout, "%i connections [-1]\n", clientc);
					continue;
				}
			}
		}
	}

	return NULL;
}

int process_connection(int sock)
{
	static char buffer[BUF_SIZE];
	int r, i;
	char cmd[32], arg[32], answer[256];
	if ((r = read(sock, buffer, BUF_SIZE-1)) < 0) {
		if (errno != EAGAIN) {
			perror("read");
			exit(1);
		}
	} else if (r == 0) {
		return -1;
	} else {
		int pos = 0, apos = 0;
		// cmd
		while (pos < r-1 && buffer[pos] != ' ' && pos < 31) {
			cmd[pos] = buffer[pos];
			pos++;
		}
		cmd[pos++] = '\0';
		//arg
		while (pos < r-1 && buffer[pos] != ' ' && apos < 31) {
			arg[apos] = buffer[pos];
			apos++; pos++;
		}
		arg[apos] = '\0';

		if (!strcmp(cmd, "help")) {
			if (apos > 0) {
				if (!strcmp(arg, "help")) {
					sprintf(answer, "Print help.\n");
				} else if (!strcmp(arg, "start")) {
					sprintf(answer, "Usage: 'start <port>'.\nRun tcp hub server on port <port>.\n");
				} else if (!strcmp(arg, "stop")) {
					sprintf(answer, "Usage: 'stop <port>'.\nStop tcp hub server running on port <port>.\n");
				} else if (!strcmp(arg, "quit")) {
					sprintf(answer, "Close monitor connection.\n");
				} else if (!strcmp(arg, "shutdown")) {
					sprintf(answer, "Shutdown TCP Hub monitor server (and all sons).\n");
				} else if (!strcmp(arg, "getpid")) {
					sprintf(answer, "Print PID of TCP Hub monitor.\n");
				} else if (!strcmp(arg, "list")) {
					sprintf(answer, "Show current running tcp hub server.\n");
				} else {
					sprintf(answer, "Sorry, no help about command '%s'\n", arg);
				}
			} else {
				sprintf(answer, "List of available commands: 'help', 'start', 'stop', 'list', 'quit', 'getpid', 'shutdown'.\nFor help about an command, type 'help <command>'.\n");
			}
		} else if (!strcmp(cmd, "start")) {
			if (apos > 0) {
				if (add_hub(arg) < 0) {
					sprintf(answer, "Starting hub on port %s ... failed\n", arg);
				} else {
					sprintf(answer, "Starting hub on port %s ...\n", arg);
				}
			} else {
				sprintf(answer, "Usage: 'start <port>'.\n");
			}
		} else if (!strcmp(cmd, "shutdown")) {
			exit(0);
		} else if (!strcmp(cmd, "stop")) {
			if (apos > 0) {
				if (rm_hub(arg) < 0) {
					sprintf(answer, "Stoping hub on port %s ... failed\n", arg);
				} else {
					sprintf(answer, "Stoping hub on port %s ...\n", arg);
				}
			} else {
				sprintf(answer, "Usage: 'stop <port>'.\n");
			}
		} else if (!strcmp(cmd, "getpid")) {
			sprintf(answer, "PID of TCP Hub monitor: %d.\n", getpid());
		} else if (!strcmp(cmd, "list")) {
			/*if (pthread_mutex_lock(&hub_mtx) < 0) {
				perror("pthread_mutex_lock");
				exit(1);
			}*/
			sprintf(answer, "+---------------+----------+\n|Service        |PID       |\n+---------------+----------+\n");
			if (write(sock, answer, strlen(answer)) < 0) {
				perror("write");
			}
			for (i = 0 ; i < hub_count ; i++) {
				sprintf(answer, "|%15s|%10d|\n", hub_port[i], hub_pid[i]);
				if (write(sock, answer, strlen(answer)) < 0) {
					perror("write");
				}
			}
			sprintf(answer, "+---------------+----------+\nTotal: %d services\n", hub_count);
			/*if (pthread_mutex_unlock(&hub_mtx) < 0) {
				perror("pthread_mutex_unlock");
				exit(1);
			}*/
		} else if (!strcmp(cmd, "quit")) {
			return -1;
		} else {
			sprintf(answer, "Sorry, unknow command '%s'.\n", cmd);
		}
		if (write(sock, answer, strlen(answer)) < 0) {
			perror("write");
		}
		if (write(sock, "> ", 2) < 0) {
			perror("write");
		}
	}
}

int rm_hub(char * service)
{	
	int i;
	int r = 0;

	/*if (pthread_mutex_lock(&hub_mtx) < 0) {
		perror("pthread_mutex_lock");
		exit(1);
	}*/
	for (i = 0 ; i < hub_count ; i++) {
		if (!strcmp(hub_port[i], service)) {
			kill(hub_pid[i], 15);
			/*close(hub_pin[i]);
			close(hub_pout[i]);
			free(hub_port[i]);
			hub_pid[i] = hub_pid[hub_count-1];
			hub_pin[i] = hub_pin[hub_count-1];
			hub_pout[i] = hub_pout[hub_count-1];
			hub_port[i] = hub_port[hub_count-1];*/
			break;
		}
	}
	if (i == hub_count) {
		r = -1;
	} else {
		hub_count--;
	}
	/*if (pthread_mutex_unlock(&hub_mtx) < 0) {
		perror("pthread_mutex_unlock");
		exit(1);
	}*/
	return r;
}

int add_hub(char * service)
{
	//printf("Starting hub on port %s ... ", service);
	//fflush(stdout);

	int p[2][2];
	int i;
	
	for (i = 0 ; i < 2 ; i++) {
		if (pipe(p[i]) < 0) {
			printf("failed\n");
			perror("pipe");
			return -1;
		}
	}

	int pid = fork();
	switch (pid) {
		case -1: // error
			printf("failed\n");
			perror("fork");
			return -1;
			break;
		case 0: // son
			for (i = 0 ; i < 2 ; i++) {
				close(p[i][0]);
				if (dup2(p[i][1], i+1) < 0) {
					perror("dup2");
					return 1;
				}
				close(p[i][1]);
			}
			execlp("tcphub", "tcphub", service, NULL);
			perror("execlp");
			return 1;
			break;
		default: // father
			/*if (pthread_mutex_lock(&hub_mtx) < 0) {
				printf("failed\n");
				kill(pid, 15);
				perror("pthread_mutex_lock");
				return -1;
			}*/
			hub_pin[hub_count] = p[0][0];
			hub_pout[hub_count] = p[1][0];
			hub_pid[hub_count] = pid;
			if ((hub_port[hub_count] = malloc(strlen(service)+1)) == NULL) {
				printf("failed\n");
				perror("malloc");
				kill(pid, 15);
				return -1;
			}
			strcpy(hub_port[hub_count], service);
			hub_count++;
			/*if (pthread_mutex_unlock(&hub_mtx) < 0) {
				printf("failed\n");
				kill(pid, 15);
				perror("pthread_mutex_unlock");
				return -1;
			}*/
			for (i = 0 ; i < 2 ; i++) {
				close(p[i][1]);
			}
			//printf("done\n");
	}

	return 0;
}

/*int logpipe(int fd)
{
	//printf("listen\n");
	int r, w, i, j;
	char buffer[BUF_SIZE];
	char line[BUF_SIZE];
	fd_set lfdset;
	int b = 0, l = 0;
	int opt;
	if ((opt = fcntl(fd, F_GETFL)) < 0) {
		perror("fcntl (F_GETFL)");
		return -1;
	}
	if (fcntl(fd, F_SETFL, opt & ~O_NONBLOCK) < 0) {
		perror("fcntl (F_SETFL)");
		return -1;
	}
	while (1) {
		FD_ZERO(&lfdset);
		FD_SET(fd, &lfdset);
		printf("select\n");
		if (select(FD_SETSIZE, &lfdset, NULL, NULL, NULL) < 0) {
			perror("select");
		}
		printf("select\n");
		if (FD_ISSET(fd, &lfdset)) {
			printf("fd_isset\n");
			if ((r = read(fd, buffer, BUF_SIZE-b-1)) <= 0) {
				if (r == 0) {
					printf("tcphub terminated\n");
					return 0;
				} else {
					perror("read");
					return -1;
				}
			}
			printf("read %d\n", r);
			b += r;
			j = 0;
			l = 0;
			for (i = 0 ; i < b ; i++) {
				if (buffer[i] == '\n') {
					printf("\\n %d\n", i);
					line[j] = '\0';
					logline(line);
					j = 0;
					l = i;
				} else {
					line[j] = buffer[i];
					j++;
				}
			}
			memmove(buffer, buffer+l, l);
			if (l == 0 && b == BUF_SIZE-1) {
				printf("buffer complet (%d)\n", i);
				line[j] = '\0';
				logline(buffer);
				b = 0;
			}
		}
		*if (i == 2 && pfd[1].revents & POLLOUT) {
			if ((w = write(1, buffer, r)) < 0) {
				perror("write");
			}
		}*
	}
	perror("read");
	////free(pfd);
	return -1;
}*/

/*int logline(char * line)
{
	printf("logline\n");
	printf("%d\t\t%s\n", 1, line);
	printf("logline end\n");
	return 0;
}*/

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

void son_sig_handler(int signo)
{
    sigset_t allsigmask, backupsigmask;
    sigfillset(&allsigmask); /* All signals */
    sigprocmask(SIG_SETMASK, &allsigmask, &backupsigmask);
    int status;
    int pid = wait(&status);
	int i;
	/*if (pthread_mutex_lock(&hub_mtx) < 0) {
		perror("pthread_mutex_lock");
		exit(1);
	}*/
	for (i = 0 ; i < hub_count ; i++) {
		if (hub_pid[i] == pid) {
			break;
		}
	}
	if (i != hub_count) {
		close(hub_pin[i]);
		close(hub_pout[i]);
		free(hub_port[i]);
		hub_pid[i] = hub_pid[hub_count-1];
		hub_pin[i] = hub_pin[hub_count-1];
		hub_pout[i] = hub_pout[hub_count-1];
		hub_port[i] = hub_port[hub_count-1];
		hub_count--;
	}
	/*if (pthread_mutex_unlock(&hub_mtx) < 0) {
		perror("pthread_mutex_unlock");
		exit(1);
	}*/
    /*if (status != 0) {
        fprintf(stderr, "Process %i quit with status %i\n", pid, status);
    }*/
    sigprocmask(SIG_SETMASK, &backupsigmask, NULL);
}
