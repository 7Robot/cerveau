#include "libcan.h"

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <dlfcn.h>

#define BUF_SIZE 256
#define ENV_MODULES_DIR "CAN_MODULES_DIR"
#define DEFAULT_DIR "/usr/bin/can"

char * can_module_dir = NULL;

struct can_ctx {
    int fd;
    FILE * stream;
    char * format;
    void (*recv)(unsigned int,can_t);
    int (*send)(int,can_t);
	void (*listen)(FILE*,void(*)(unsigned int,can_t));
    pthread_t pth;
	int status;
};

void * listen(void * c);

int can_init(can_ctx ** ctx, int fd, const char * format, void (*recv)(unsigned int, can_t))
{
	can_ctx * c = NULL;
	if ((c = calloc(1, sizeof(can_ctx))) == NULL) {
		perror("malloc");
		return -1;
	}

	/*int flags;
    if ((flags = fcntl(fd, F_GETFL)) < 0) {
        perror("fcntl(F_GETFL)");
        return;
    }
    if (fcntl(fd, F_SETFL, flags & ~O_NONBLOCK) < 0) {
        perror("fcntl(F_SETFL)");
        return;
    }*/
	c->fd = fd;

	if ((c->stream = fdopen(fd, "a+")) == NULL) {
		perror("fdopen");
		return -1;
	}

	if ((c->format = malloc(strlen(format)+1)) == NULL) {
		perror("malloc");
		return -1;
	}
	strcpy(c->format, format);

	c->recv = recv;

	void * hndl;
	char path[BUF_SIZE];

	snprintf(path, BUF_SIZE, "lib%s.so", format);
	printf("Try to load '%s' … ", path);
	hndl = dlopen(path, RTLD_LAZY);
	if (hndl == NULL) {
		printf("FAILED\n");
		if (can_module_dir == NULL) {
			char * env = getenv(ENV_MODULES_DIR);
			if ((env != NULL) && (strlen(env) != 0)) {
				if ((can_module_dir = malloc(strlen(env)+1)) == NULL) {
					perror("malloc");
					return -1;
				}
				strcpy(can_module_dir, env);
			}
		}
		if (can_module_dir != NULL) {
			snprintf(path, BUF_SIZE, "%s/lib%s.so", can_module_dir, format);
			printf("Try to load '%s' … ", path);
			hndl = dlopen(path, RTLD_LAZY);
			if (hndl == NULL) {
				printf("FAILED\n");
			} else {
				printf("Ok\n");
			}
		}
		if (hndl == NULL) {
			snprintf(path, BUF_SIZE, "%s/lib%s.so", DEFAULT_DIR, format);
			printf("Try to load '%s' … ", path);
			hndl = dlopen(path, RTLD_LAZY);
			if (hndl == NULL) {
				printf("FAILED\n");
				fprintf(stderr, "dlopen: unable to determine can module directory\n");
				fprintf(stderr, "check value of %s environment variable\n", ENV_MODULES_DIR);
				return -1;
			} else {
				printf("Ok\n");
			}
		}
	} else {
		printf("Ok\n");
	}
	c->send = dlsym(hndl, "can_write");
	if (c->send == NULL) {
		fprintf(stderr, "dlsym: %s\n", dlerror());
		return -1;
	}
	c->listen = dlsym(hndl, "can_listen");
	if (c->listen == NULL) {
		fprintf(stderr, "dlsym: %s\n", dlerror());
		return -1;
	}

	if ((errno = pthread_create(&(c->pth), NULL, listen, (void *) c)) < 0) {
		fprintf(stderr, "pthread_create\n");
		return -1;
	}
	c->status = 1;

	*ctx = c;
	
	return 0;
}

void * listen(void * c)
{
	can_ctx * ctx = (can_ctx *) c;
	ctx->listen(ctx->stream, ctx->recv);
	return NULL;
}

int can_id(can_ctx * ctx)
{
	return ctx->pth;
}

int can_send(can_ctx * ctx, can_t packet)
{
	return ctx->send(ctx->fd, packet);
}

void can_destroy(can_ctx * ctx)
{
	if (ctx != NULL) {
		free(ctx->format);
		if (ctx->status) {
			pthread_cancel(ctx->pth);
		}
	}
	free(ctx);
}
