#include <sys/ioctl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <pthread.h>
#include <libcan.h>
#include <functions.h>

#include <linux/input.h>
#include <linux/joystick.h>

#define DELAY 200
#define NB_CONSIGNE 3

char *axis_names[ABS_MAX + 1] = {
"X", "Y", "Z", "Rx", "Ry", "Rz", "Throttle", "Rudder", 
"Wheel", "Gas", "Brake", "?", "?", "?", "?", "?",
"Hat0X", "Hat0Y", "Hat1X", "Hat1Y", "Hat2X", "Hat2Y", "Hat3X", "Hat3Y",
"?", "?", "?", "?", "?", "?", "?", 
};

char *button_names[KEY_MAX - BTN_MISC + 1] = {
"Btn0", "Btn1", "Btn2", "Btn3", "Btn4", "Btn5", "Btn6", "Btn7", "Btn8", "Btn9", "?", "?", "?", "?", "?", "?",
"LeftBtn", "RightBtn", "MiddleBtn", "SideBtn", "ExtraBtn", "ForwardBtn", "BackBtn", "TaskBtn", "?", "?", "?", "?", "?", "?", "?", "?",
"Trigger", "ThumbBtn", "ThumbBtn2", "TopBtn", "TopBtn2", "PinkieBtn", "BaseBtn", "BaseBtn2", "BaseBtn3", "BaseBtn4", "BaseBtn5", "BaseBtn6", "BtnDead",
"BtnA", "BtnB", "BtnC", "BtnX", "BtnY", "BtnZ", "BtnTL", "BtnTR", "BtnTL2", "BtnTR2", "BtnSelect", "BtnStart", "BtnMode", "BtnThumbL", "BtnThumbR", "?",
"?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", 
"WheelBtn", "Gear up",
};

void event(int x, int y);
void * update(void * arg);
void turn(int fd, int right);

#define NAME_LENGTH 128

int left;
int right;
int b[4] = { 0 };
can_ctx * canctx;
pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t cnd_mtx = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cnd = PTHREAD_COND_INITIALIZER;

int main (int argc, char **argv)
{
	int fd, i;
	unsigned char axes = 2;
	unsigned char buttons = 2;
	int version = 0x000800;
	char name[NAME_LENGTH] = "Unknown";
	uint16_t btnmap[KEY_MAX - BTN_MISC + 1];
	uint8_t axmap[ABS_MAX + 1];

	if (argc != 4) {
		puts("");
		puts("Usage: jstest <device> <host> <port>");
		puts("");
		return 1;
	}
	if ((fd = open(argv[1], O_RDONLY)) < 0) {
		perror("jsrobot");
		return 1;
	}

	ioctl(fd, JSIOCGVERSION, &version);
	ioctl(fd, JSIOCGAXES, &axes);
	ioctl(fd, JSIOCGBUTTONS, &buttons);
	ioctl(fd, JSIOCGNAME(NAME_LENGTH), name);
	ioctl(fd, JSIOCGAXMAP, axmap);
	ioctl(fd, JSIOCGBTNMAP, btnmap);


	printf("Driver version is %d.%d.%d.\n",
		version >> 16, (version >> 8) & 0xff, version & 0xff);

	printf("Joystick (%s) has %d axes (", name, axes);
	for (i = 0; i < axes; i++)
		printf("%s%s", i > 0 ? ", " : "", axis_names[axmap[i]]);
	puts(")");

	printf("and %d buttons (", buttons);
	for (i = 0; i < buttons; i++)
		printf("%s%s", i > 0 ? ", " : "", button_names[btnmap[i] - BTN_MISC]);
	puts(").");

	if (axes < 2) {
		printf("No enought axes.\n");
		exit(0);
	}

	int *axis;
	char *button;
	struct js_event js;

	axis = calloc(axes, sizeof(int));
	button = calloc(buttons, sizeof(char));

	int sock;
	if ((sock = getsockfd(argv[2], argv[3])) < 0) {
		fprintf(stderr, "Error: getsockfd(%s,%s)\n", argv[2], argv[3]);
		exit(1);
	}

	pthread_t pth;
	pthread_create(&pth, NULL, update, &sock);

	while (1) {
		if (read(fd, &js, sizeof(struct js_event)) != sizeof(struct js_event)) {
			perror("\njstest: error reading");
			return 1;
		}

		switch(js.type & ~JS_EVENT_INIT) {
		case JS_EVENT_BUTTON:
			button[js.number] = js.value;
			break;
		case JS_EVENT_AXIS:
			axis[js.number] = js.value;
			break;
		}

		if (button[1] && !b[1]) {
			b[1] = 1;
			can_write(sock, bin, 1051, 0);
		} else if (button[3] && !b[2]) {
			b[2] = 1;
			turn(sock, 0);
		} else if (button[3] && !b[3]) {
			b[3] = 1;
			turn(sock, 1);
		} else {
			b[1] = 0;
			b[2] = 0;
			b[3] = 0;
			event(axis[0], -axis[1]);
		}
	}

	return -1;
}

void turn(int fd, int right)
{
	short int value = 2106;
	if (!right) {
		value = -value;
	}
	// demi tour
	/*if (right) {
		packet.b[0] = 116;
		packet.b[1] = 16;
	} else {
		packet.b[0] = 140;
		packet.b[1] = 239;
	}*/
	can_write(fd, bin, 1026, 2, ((char*)&value)[0], ((char*)&value)[1]);
}

void event(int _x, int _y)
{
	static time_t t = 0;

	int x = (_x * 80) / 32767;
	int y = (_y * 80) / 32767;

	if (pthread_mutex_lock(&mtx) < 0) {
		perror("pthread_mutex_lock");
		exit(1);
	}

	left = y;
	right = y; + x * (y-80) / 160;
	
	if (x > 0) {
		left -= x * (y-80) / 160;
		right -= x * (y+80) / 160;
	} else {
		left += x * (y+80) / 160;
		right += x * (y-80) / 160;
	}

	if (pthread_mutex_unlock(&mtx) < 0) {
		perror("pthread_mutex_unlock");
		exit(1);
	}

    pthread_mutex_lock(&cnd_mtx);
    pthread_cond_signal(&cnd);
    pthread_mutex_unlock(&cnd_mtx);
}

void * update(void * arg)
{
	int l = 81;
	int r = 81;
	int u = 0;
	struct can_t packet;
	packet.id = 1032;
	packet.length = 2;
	while (1) {
		if (l == left && r == right) {
			u++;
		} else {
			u = 0;
		}
		if (u < NB_CONSIGNE) {
			if (pthread_mutex_lock(&mtx) < 0) {
				perror("pthread_mutex_lock");
				exit(1);
			}
			l = left;
			r = right;
			if (pthread_mutex_unlock(&mtx) < 0) {
				perror("pthread_mutex_unlock");
				exit(1);
			}
			packet.b[0] = l;
			packet.b[1] = r;
			can_pwrite(*((int*)arg), bin, &packet);
			usleep(DELAY * 1000);
		} else {
		    pthread_mutex_lock(&cnd_mtx);
		    pthread_cond_wait(&cnd, &cnd_mtx);
		    pthread_mutex_unlock(&cnd_mtx);
		}
		printf("\r");
		printf("%+04d %+04d %d %d %d", left, right, b[1], b[2], b[3]);
		fflush(stdout);

	}
}
