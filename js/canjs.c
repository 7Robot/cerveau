#include <time.h>
#include <pthread.h>
#include <functions.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>


#include <linux/input.h>
#include <linux/joystick.h>

#define DELAY 200
#define NB_CONSIGNE 2

#define NAME_LENGTH 128
#define DEFAULT_DEVICE "/dev/input/js0"
#define DEFAULT_HOST "r2d2"
#define DEFAULT_PORT "7773"
#define DEFAULT_SENSITIVITY 1

int left, right, angle;
int sensi = 1; /* sensitivity */
pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t cnd_mtx = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cnd = PTHREAD_COND_INITIALIZER;
FILE * can;

int can_open(char * host, char * port)
{
    int fd;
    if ((fd = getsockfd(host, port)) < 0) {
        fprintf(stderr, "Error: getsockfd(%s,%s)\n", host, port);
        return -1;
    }
    can = fdopen(fd, "a");
    if (can == NULL) {
        perror("fdopen");
        return -1;
    }
    return 0;
}

void update_pos(int _x, int _y, int _z)
{
    int x = (_x * 80) / 32767;
    int y = (_y * 80) / 32767;
    int z = (_z * 1023) / 65536 + 511;

    if (pthread_mutex_lock(&mtx) < 0) {
        perror("pthread_mutex_lock");
        exit(1);
    }

    left = - (80 * (y + x)) / (80 + abs(x));
    right = - (80 * (y - x)) / (80 + abs(x));
    angle = z;

    if (pthread_mutex_unlock(&mtx) < 0) {
        perror("pthread_mutex_unlock");
        exit(1);
    }

    pthread_mutex_lock(&cnd_mtx);
    pthread_cond_signal(&cnd);
    pthread_mutex_unlock(&cnd_mtx);
}

void update(int axisc, int * axis, int buttonc, char * button)
{
    static char * b = NULL;
    if (b == NULL) {
        b = calloc(buttonc, sizeof(char));
    }

    if (button[0] && !b[0]) {
        b[0] = 1;
        fprintf(can, "asserv speed 0 0\n");
        fflush(can);
    } else if (button[1] && !b[1]) {
        b[1] = 1;
        fprintf(can, "asserv rot 18000\n");
        fflush(can);
    } else if (button[2] && !b[2]) {
        b[2] = 1;
        fprintf(can, "asserv rot -9000\n");
        fflush(can);
    } else if (button[3] && !b[3]) {
        b[3] = 1;
        fprintf(can, "asserv rot 9000\n");
        fflush(can);
    } else {
        int i;
        for (i = 0; i < 4 ; i++) {
            b[i] = 0;
        }
        update_pos(axis[0]*sensi, axis[1]*sensi, axis[2]*sensi);
    }
}

void * sender(void * arg)
{
    int l = INT_MIN;
    int r = INT_MIN;
    int a = INT_MIN;
    int u = 0;
    int v = 0;
    int todo;
    
    while (1) {

        todo = 0;

        if (pthread_mutex_lock(&mtx) < 0) {
            perror("pthread_mutex_lock");
            exit(1);
        }

        if (l == left && r == right) {
            u++;
        } else {
            u = 0;
            l = left;
            r = right;
        }
        if (a == angle) {
            v++;
        } else {
            v = 0;
            a = angle;
        }

        if (pthread_mutex_unlock(&mtx) < 0) {
            perror("pthread_mutex_unlock");
            exit(1);
        }
        
        if (u < NB_CONSIGNE) {
            fprintf(can, "asserv speed %d %d\n", r, l);
            fflush(can);
            todo = 1;
        }
        if (v < NB_CONSIGNE) {
            fprintf(can, "ax 1 angle set %d\n", a);
            fflush(can);
            usleep(100*1000);
            fprintf(can, "ax 2 angle set %d\n", a);
            fflush(can);
            todo = 1;
        }
        if (todo) {
            usleep(DELAY * 1000);
        } else {
            pthread_mutex_lock(&cnd_mtx);
            pthread_cond_wait(&cnd, &cnd_mtx);
            pthread_mutex_unlock(&cnd_mtx);
        }

    }
}

int main (int argc, char **argv)
{
    puts("");
    puts("Usage: jstest [<device> [<host> [<port> [<sensitivity>]]]]");
    puts("");

    if (argc > 5) {
        return 1;
    }

    char * device = (argc>1)?argv[1]:DEFAULT_DEVICE;
    char * host   = (argc>2)?argv[2]:DEFAULT_HOST;
    char * port   = (argc>3)?argv[3]:DEFAULT_PORT;
    sensi  = (argc>4)?atoi(argv[4]):DEFAULT_SENSITIVITY;

    if (can_open(host, port) < 0) {
        fprintf(stderr, "can_open failed\n");
        return EXIT_FAILURE;
    }

    pthread_t pth;
    pthread_create(&pth, NULL, sender, NULL);

    js_read(device, update);

    return EXIT_FAILURE;
}
