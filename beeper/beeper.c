#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/version.h>
#include <linux/input.h>
#include <stdio.h>
#include <stdlib.h>
//#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>


static int ring_bell(int val)
{
    ssize_t s;
    struct input_event ev;
    int fd = open("/dev/input/beeper", O_WRONLY);
    
    /* ev.time = ??; TODO */
    ev.type = EV_SND;
    ev.code = SND_TONE;
    ev.value = val; /* enable (ring) the bell */

    s = write(fd, &ev, sizeof (ev));
    if (s == -1) {
        perror("Writing bell event");
        return -1;
    }

    close(fd);
    return 1;
}

int main(int argc, char **argv)
{
	ring_bell(500);
	return 0;
}
