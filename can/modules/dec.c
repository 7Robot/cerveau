#include "libcan.h"

#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <string.h>

int can_write(int fd, can_t packet)
{
    char output[128];
    sprintf(output, "%-6i", packet.id);
    for (int i = 0 ; i < packet.length ; i++) {
        sprintf(output+strlen(output), "   %-3i", packet.b[i]);
    }
    sprintf(output+strlen(output), "\n");
    write(fd, output, strlen(output));
    fsync(fd);

    return 0;
}


void can_listen(FILE * stream, void(*receiv)(unsigned int, can_t))
{
    can_t packet;
    char line[128];

    while (1) {
        fgets(line, 128, stream);
        packet.length = sscanf(line, "%d%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu%*[ \t]%hhu", &packet.id,
                packet.b, packet.b+1, packet.b+2, packet.b+3, packet.b+4, packet.b+5, packet.b+6, packet.b+7) - 1;
        if (packet.length >= 0 && packet.id < 2048) {
            receiv((unsigned int)pthread_self(), packet);
        }
    }
}
