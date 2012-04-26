#ifndef _TOOLS_H_
#define _TOOLS_H_

#ifdef __cplusplus
extern "C" {
#endif

/** Take an array of couple read fd / write fd, and listen on any read fd. When
 * data is read, write it on writef fd associated. Based of poll system call. */
int multipipe(int size, int fd[][2]);

/** Open socket from <host> on port <port>
 * Return associated file descriptor (-1 on error)
 */
int getsockfd(const char * host, const char * port);

/** Open serial port <device> at speed <speed>
 * Return associated file descriptor (-1 om error)
 */
int getttyfd(const char * device, int speed);

#ifdef __cplusplus
}
#endif
#endif
