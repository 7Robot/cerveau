#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <poll.h>
#include <stropts.h>
#include <stdlib.h>

#define BUFSIZE 1024

int multipipe(int size, int fd[][2])
{
	int i, r, w, p;

	char ** buffers;
	if ((buffers = malloc(size * sizeof(char*))) == NULL) {
		perror("malloc");
		return -1;
	}
	for (i = 0 ; i < size ; i++) {
		if ((buffers[i] = malloc(BUFSIZE * sizeof(char))) == NULL) {
			perror("malloc");
			return -1;
		}
	}

	int * c;
	if ((c = malloc(size * sizeof(int))) == NULL) {
		perror("malloc");
		return -1;
	}
	for (i = 0 ; i < size ; i++) {
		c[i] = 0;
	}

	int * t;
	if ((t = malloc(size * sizeof(int))) == NULL) {
		perror("malloc");
		return -1;
	}

	struct pollfd * pfd = NULL;
	if ((pfd = malloc(2 * size * sizeof(struct pollfd))) == NULL) {
		perror("malloc");
		exit(1);
	}

	while (1) {

		p = 0;
		for (i = 0 ; i < size ; i++) {
			if (c[i] < BUFSIZE) {
				pfd[p].fd = fd[i][0];
				pfd[p].events = POLLIN;
				pfd[p].revents = 0;
				t[p] = i;
				p++;
			}

			if (c[i] > 0) {
				pfd[p].fd = fd[i][1];
				pfd[p].events = POLLOUT;
				pfd[p].revents = 0;
				t[p] = i;
				p++;
			}
		}

		if ((r = poll(pfd, p, -1)) <= 0) {
			if (r == 0 || errno == EINTR)
				continue;
			perror("poll");
			return -1;
		}

		for (i = 0 ; i < p ; i++) {
			if (pfd[i].revents & POLLIN) {
				if ((r = read(fd[t[i]][0], buffers[t[i]], BUFSIZE-c[t[i]])) < 0) {
					if ((r == 0) || (errno != EAGAIN && errno != EWOULDBLOCK)) {
						perror("read");
						return -1;
					}
				}
				c[t[i]] += r;
			}
			if (pfd[i].revents & POLLOUT) {
				if ((w = write(fd[t[i]][1], buffers[t[i]], c[t[i]])) < 0) {
					perror("write");
					return -1;
				}
				if (w != 0) {
					c[t[i]] -= w;
					memmove(buffers[t[i]], &(buffers[t[i]]), c[t[i]]);
				}
			}
		}
	}
}
