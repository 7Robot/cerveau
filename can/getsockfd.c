#include <stdio.h>
#include <unistd.h>
#include <string.h>

#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>

#include <sys/types.h>
#include <sys/socket.h>

#ifdef __cplusplus
extern "C" {
#endif

int getsockfd(const char * host, const char * port) 
{ 
    struct hostent * hostent; 
    struct servent * servent; 
    struct sockaddr_in address; 
    int numero, sock; 
 
    memset(&address, 0, sizeof(struct sockaddr_in)); 
    if (inet_aton(host, &(address.sin_addr)) == 0) { 
        if ((hostent = gethostbyname(host)) == NULL) { 
            fprintf(stderr, "unknow host\n"); 
            return -1; 
        } 
        address.sin_addr.s_addr = ((struct in_addr *) (hostent->h_addr))->s_addr; 
    } 
    if (sscanf(port, "%d", &numero) == 1) { 
        address.sin_port = htons(numero); 
    } else if ((servent = getservbyname(port, "tcp")) == NULL) { 
        fprintf(stderr, "unknow service %s\n", port); 
        return -1; 
    } else { 
        address.sin_port = servent->s_port; 
    } 
    address.sin_family = AF_INET; 
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) { 
        perror("socket"); 
        return -1; 
    } 
    if (connect(sock, (struct sockaddr *) &address, sizeof(struct sockaddr_in)) < 0) { 
        perror("connect"); 
        return -1; 
    } 
 
    return sock; 
}

#ifdef __cplusplus
}
#endif
