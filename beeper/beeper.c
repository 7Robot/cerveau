#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/version.h>
#include <linux/input.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>

// http://wingston.workshopindia.com/wingz/qt-application-to-play-music-on-the-mini2440s-beeper/

void ring_bell(int freq)
{
    ssize_t s;
    struct input_event ev;
    int fd = open("/dev/input/beeper", O_WRONLY);
    
    ev.type = EV_SND;
    ev.code = SND_TONE;
    ev.value = freq;

    s = write(fd, &ev, sizeof (ev));
    if (s == -1) {
        perror("Error writing bell event.");
        return;
    }
    
	close(fd);
}

int main(int argc, char **argv)
{	
	if(argc < 3) {
		perror("Usage : beeper <frequence> <duration> ... ");
		return EXIT_FAILURE;
	}
	else {
		int i = 1;
		while(i + 1 < argc) {
			int frequence = atoi(argv[i++]);
			int duration = atoi(argv[i++]);
			
			ring_bell(frequence);
			usleep(1000 * duration);
		}
		ring_bell(0);
		
		return EXIT_SUCCESS;
	}
}
