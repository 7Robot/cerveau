#include <sys/types.h>
#include <sys/socket.h> // listen()
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <unistd.h> // close()
#include <string.h> // memset()
#include <errno.h>
#include <stdio.h>

#include "server.h"

int create_tcp_server(const char* hostname, const char* servname)
{
	int socket;

	if ((socket = create_socket_stream(hostname, servname)) < 0)
		return -1;

	if (listen(socket, 8) < 0) {	/* (Socket, Waiting list size) */
		perror("listen");
		close(socket);
		return -1;
	}
	
	return socket;
}

int create_socket_stream(const char* hostname, const char* servname)
{
	struct addrinfo hints;
	struct addrinfo *result, *rp;
	int sfd, s;

	memset(&hints, 0, sizeof(struct addrinfo)); /* init hints */
	hints.ai_flags = AI_PASSIVE;				/* Not only loopback if hostname is null */
	hints.ai_family = AF_INET;					/* AF_UNSPEC/AF_INET/AF_INET6 */
	hints.ai_socktype = SOCK_STREAM;			/* STREAM(TCP), DGRAM(UDP), SEQPACKET(?) */
	hints.ai_protocol = 0;						/* Any protocol */
	hints.ai_canonname = NULL;
	hints.ai_addr = NULL;
	hints.ai_next = NULL;

	s = getaddrinfo(hostname, servname, &hints, &result);
	if (s != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
		return -1;
	}

	for (rp = result; rp != NULL; rp = rp->ai_next) {

		sfd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
		
		if (sfd == -1) {
			perror("socket");
			continue;
		}

		if (bind(sfd, rp->ai_addr, rp->ai_addrlen) == 0) {
			break;	/* Success */
		} else {
			perror("bind");
			fprintf(stderr, "Tried address: %s, service: %s\n", inet_ntoa(((const struct sockaddr_in*)(rp->ai_addr))->sin_addr), servname);
		}

		close(sfd);
	}
	freeaddrinfo(result);	/* No longer needed */

	if (rp == NULL) {	/* No address succeeded */
		fprintf(stderr, "Error: Could not bind\n");
		return -1;
	}

	return sfd;
}
