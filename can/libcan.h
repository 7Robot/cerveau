#ifndef _LIBCAN_H_
#define _LIBCAN_H_

#include <stdint.h>

typedef struct {
	int id;
	int length;
	uint8_t b[8];
} can_t;

typedef struct can_ctx can_ctx;

char * can_module_dir;

int can_init(can_ctx ** ctx, int fd, const char * format, void (*)(unsigned int, can_t)); // Pour créer un context
int can_id(can_ctx * ctx); // Pour obtenir l'id du can (id du pthread)
int can_send(can_ctx * ctx, can_t packet); // Pour envoyer un packet
void can_destroy(can_ctx * ctx); // Pour détruire un context

#endif // _LIBCAN_H_
