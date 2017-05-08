#ifndef __ocslog_h
#define __ocslog_h

#include <string.h>
#include <stdio.h>

#define LOG_ENTRY_SIZE 		256 // 256 B
#define LOG_OUTENTRY_SIZE 	16384 // 16KB
#define UNKNOWN_ERROR	-1
#define FAILURE			-2
#define SUCCESS			0

typedef enum LOG_LEVEL
{
	SILENT_LEVEL = 0,
	INFO_LEVEL = 1,
	ERROR_LEVEL = 2,
}loglevel_t;

#define PC_DEBUG 1 // J2010 not support full ocslog functions, so print to console directly.

#ifdef PC_DEBUG
#define	log_out(...)	printf (__VA_ARGS__); printf ("\n")
#define	log_info		log_out
#define	log_err(x, ...)	\
	do { \
		char message[LOG_ENTRY_SIZE]; \
		snprintf (message, sizeof (message), __VA_ARGS__); \
		log_out ("ERROR: %s -> %s", strerror (x), message); \
	} while (0)
#define	log_init(x)
#else
void log_out(char*, ...); 
void log_info(char*, ...); 
void log_err(int, char*,...);
void log_init(loglevel_t);
#endif

/* 
 * LOG_ERR macro
 * Note: Macro is required for getting error location information 
 */
#define log_fnc_err(err, ...) do {	\
	char new_message[LOG_ENTRY_SIZE];	\
	const char* file = __FILE__;	\
	const char* func = __FUNCTION__;	\
    int line = __LINE__;	\
    snprintf (new_message, sizeof (new_message), __VA_ARGS__); \
    log_err (err, "Location:(%s:%s:%d) \n%s", file, func, line, new_message); \
	} while(0)

#endif //__ocslog_h
