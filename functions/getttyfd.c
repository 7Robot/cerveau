#include <termios.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

#ifdef __cplusplus
extern "C" {
#endif

static speed_t convertspeed(int s);

int getttyfd(const char * device, int s)
{
	struct termios config;
	int tty;
	speed_t speed;

	speed = convertspeed(s);

	tty = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
	if(tty == -1) {
		fprintf(stderr, "failed to open port %s\n", device);
		return -1;
	}
	if(!isatty(tty)) {
		fprintf(stderr, "%s is not a tty\n", device);
		return -1;
	}
	if(tcgetattr(tty, &config) < 0) {
		fprintf(stderr, "failed to get port config\n");
		return -1;
	}
	//
	// Input flags - Turn off input processing
	// convert break to null byte, no CR to NL translation,
	// no NL to CR translation, don't mark parity errors or breaks
	// no input parity check, don't strip high bit off,
	// no XON/XOFF software flow control
	//
	config.c_iflag &= ~(IGNBRK | BRKINT | ICRNL |
						INLCR | PARMRK | INPCK | ISTRIP | IXON);
	//
	// Output flags - Turn off output processing
	// no CR to NL translation, no NL to CR-NL translation,
	// no NL to CR translation, no column 0 CR suppression,
	// no Ctrl-D suppression, no fill characters, no case mapping,
	// no local output processing
	//
	// config.c_oflag &= ~(OCRNL | ONLCR | ONLRET |
	//                     ONOCR | ONOEOT| OFILL | OLCUC | OPOST);
	config.c_oflag = 0;
	//
	// No line processing:
	// echo off, echo newline off, canonical mode off, 
	// extended input processing off, signal chars off
	//
	config.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);
	//
	// Turn off character processing
	// clear current char size mask, no parity checking,
	// no output processing, force 8 bit input
	//
	config.c_cflag &= ~(CSIZE | PARENB);
	config.c_cflag |= CS8;
	//
	// One input byte is enough to return from read()
	// Inter-character timer off
	//
	config.c_cc[VMIN]  = 1;
	config.c_cc[VTIME] = 0;
	//
	// Communication speed (simple version, using the predefined
	// constants)
	//
	if(cfsetispeed(&config, speed) < 0 || cfsetospeed(&config, speed) < 0) {
		fprintf(stderr, "failed to set speed\n");
		return -1;
	}
	//
	// Finally, apply the configuration
	//
	if(tcsetattr(tty, TCSAFLUSH, &config) < 0) {
		fprintf(stderr, "failed to apply config\n");
		return -1;
	}
	
	return tty;
}

static speed_t convertspeed(int speed)
{
	switch (speed) {
		case 50:
			return B50;
		case 75:
			return B75;
		case 110:
			return B110;
		case 134:
			return B134;
		case 150:
			return B150;
		case 200:
			return B200;
		case 300:
			return B300;
		case 600:
			return B600;
		case 1200:
			return B1200;
		case 1800:
			return B1800;
		case 2400:
			return B2400;
		case 4800:
			return B4800;
		case 9600:
			return B9600;
		case 19200:
			return B19200;
		case 38400:
			return B38400;
		case 57600:
			return B57600;
		case 115200:
			return B115200;
		case 230400:
			return B230400;
	}
	fprintf(stderr, "warning: unknow speed value %d, default 9600 used\n", speed);
	return B9600;
}

#ifdef __cplusplus
}
#endif
