#include "libcan.h"

#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

int can_write(int fd, can_t packet)
{
    int i, id;
    uint8_t raw[12];
    raw[0] = 0xFD;
    id = packet.id;
    raw[1] = id >> 8;
    id &= 0xFF;
    raw[2] = id;
    raw[1] |= packet.length << 4;
    for (i = 0 ; i < packet.length ; i++) {
        raw[i+3] = packet.b[i];
    }
    raw[i+3] = 0xBF;
    if (write(fd, raw, i+4) == -1) {
        return -1;
    }
    fsync(fd);

    return 0;
}


void can_listen(FILE * stream, void(*receiv)(unsigned int, can_t))
{
	/* state = 1 : waiting FD
     * state = 2 : waiting length + ID high
     * state = 3 : waiting ID low
     * state = 0 : waiting BF
     * state = -k : waiting k bytes of data */
	int state = 1;
	can_t packet;
    uint8_t c;

	while(1) {
        /*if ((c = fgetc(stream)) != EOF) {
            perror("fgetc");
            return;
        }*/
		c = fgetc(stream);
        if (state == 1) { /* waiting FD */
            if (c == 0xFD) {
                state = 2; /* waiting length + id high */
            }
        } else if (state == 2) { /* waiting length + id high */
            packet.length = c>>4;
            if (packet.length > 8) {
                state = 1; /* waiting FD */
            } else {
                packet.id = (c%16)<<8;
                state = 3; /* waiting id low */
            }
        } else if (state == 3) { /* waiting id low */
            packet.id |= c;
            state = -packet.length;
        } else if (state == 0) { /* waiting BF */
            if (c == 0xBF) {
                receiv((unsigned int)pthread_self(), packet);
                state = 1; /* waiting FD */
            } else {
                state = 1; /* waiting FD */
            }
        } else {
            packet.b[packet.length + state] = c;
            state++;
        }
	}
}
