/*
 * Module: ocslock.c
 *
 * Description: Ocslock library
 *
 * Copyright (C) 2016 Microsoft Corp
 *
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *    Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *    Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the
 *    distribution.
 *
 *    Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
*/

#include <string.h>
#include <pthread.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <syslog.h>
#include "ocslock.h"
#include "util.h"

pthread_mutex_t *ocsmutexes[NUM_OCSLOCKS] = { NULL };
pthread_cond_t *ocscondvars[NUM_OCSLOCKS] = { NULL };
/* 
*  Have a single per-process lock for all ocsmutexes/ocscondvars 
*  Although a per-mutex lock can be used, since this is used during initialization, not a performance issue
*/
static pthread_rwlock_t ocslock_initlock = PTHREAD_RWLOCK_INITIALIZER; 

PACK(typedef struct  
{
	pthread_mutex_t mutex_t;
	pthread_cond_t condvar_t;
})ocslock_info_t;

/* function callback for recovery function pointer
* default is null.  set by lock caller when critical
* area needs consistency on mutex EOWNERDEAD.
*/
static int(*mutex_recovery)(void);

/******************************************************************************
*	Function		Name: config_mutex_rec
*	Purpose:		Sets mutex callback function.
*	In parameters:	None
*	Return value:	None
*	Comments/Notes:
*******************************************************************************/
void config_mutex_rec(int(*rec_fn)()) {
	mutex_recovery = rec_fn;
}

/*
 * Private method: mutex initialize
*/
static int mutex_initialize(pthread_mutex_t *mutex){
	int response = 0;
    pthread_mutexattr_t mutex_attrib;

        if((response = pthread_mutexattr_init(&mutex_attrib)) != 0){
                syslog(LOG_ERR, "OCSLOCK Mutex_Attrib Initialize failed: mutexattr_init() resp(%d) error(%s)\n", response, strerror(errno));
                 return response;
        }

	if((response = pthread_mutexattr_setpshared(&mutex_attrib, PTHREAD_PROCESS_SHARED)) != 0){
		syslog(LOG_ERR, "OCSLOCK Mutex Initialize failed: mutexattr_setpshared() resp(%d) error(%s)\n", response, strerror(errno));
		return response;
	}
	if((response = pthread_mutexattr_settype(&mutex_attrib, PTHREAD_MUTEX_NORMAL)) != 0){
		syslog(LOG_ERR, "OCSLOCK Mutex Initialize failed: mutex_attr_settype resp(%d) error(%s)\n", response, strerror(errno));
		return response;
	}
	if((response = pthread_mutexattr_setrobust (&mutex_attrib, PTHREAD_MUTEX_ROBUST)) != 0){
		syslog(LOG_ERR, "OCSLOCK Mutex Initialize failed: mutex_attr_setrobust resp(%d) error(%s)\n", response, strerror(errno));
		return response;
	}
	if((response = pthread_mutex_init(mutex, &mutex_attrib)) != 0){
		syslog(LOG_ERR, "OCSLOCK Mutex Initialize failed: mutex_init resp(%d) error(%s)\n", response, strerror(errno));
		return response;
	}
	return response;
}

/*
 * Private method: condvar initialize
*/
static int condvar_initialize(pthread_cond_t *condvar){
	int response = 0;
    pthread_condattr_t cond_attrib;

	if((response = pthread_condattr_setpshared(&cond_attrib, PTHREAD_PROCESS_SHARED)) != 0){
		syslog(LOG_ERR, "OCSLOCK Condvar Initialize failed: condattr_setpshared() resp(%d) error(%s)\n", response, strerror(errno));
		return response;
	}
	if((response = pthread_cond_init(condvar, &cond_attrib)) != 0){
		syslog(LOG_ERR, "OCSLOCK Condvar Initialize failed: cond_init resp(%d) error(%s)\n", response, strerror(errno));
		return response;
	}
	return response;
}

/*
 * Public method: Ocslock init
 */
int ocslock_init(ocslock_t ocslockid) {
	if(ocslockid >= NUM_OCSLOCKS) {
		syslog(LOG_ERR, "ocslock init: enum (%d) not valid\n", (int)ocslockid); 
		return -1;
	}
	int shm_handle;
	mode_t org_mask = umask(0);
	shm_handle = shm_open(OCSLOCK_STRING[ocslockid],  O_CREAT | O_RDWR | O_TRUNC | O_EXCL, (S_IRWXU | S_IRWXG | S_IRWXO));
	umask(org_mask);

	if(shm_handle < 0) {
		syslog(LOG_ERR, "Ocslock Init: failed to open shared memory: return(%d) lock(%s) error(%s)\n", 
			shm_handle, OCSLOCK_STRING[ocslockid], strerror(errno));
		return -1;
	}

	if (ftruncate(shm_handle, sizeof(pthread_mutex_t)+sizeof(pthread_cond_t)) == -1) {
		syslog(LOG_ERR, "Ocslock Init: failed to truncate shm for lock(%s) error(%s)\n", OCSLOCK_STRING[ocslockid], strerror(errno));
		return -1;
	}
		
	ocslock_info_t *ocslock_info_ptr = (ocslock_info_t*)mmap(NULL, sizeof(ocslock_info_t),
		PROT_READ | PROT_WRITE, MAP_SHARED, shm_handle, 0);

	ocsmutexes[ocslockid] = (pthread_mutex_t*)(&(ocslock_info_ptr->mutex_t));
	if (ocsmutexes[ocslockid] == MAP_FAILED) {
		syslog(LOG_ERR, "Ocslock Init: failed mutex mmap: handle(%d), lock(%s) error(%s)\n", 
			shm_handle, OCSLOCK_STRING[ocslockid], strerror(errno));
		return -1;
	}

	if(mutex_initialize(ocsmutexes[ocslockid]) != 0){
		syslog(LOG_ERR, "Ocslock Init: mutex init failed for lock(%s)\n", OCSLOCK_STRING[ocslockid]);
		return -1;
	}

	ocscondvars[ocslockid] = (pthread_cond_t*)(&(ocslock_info_ptr->condvar_t));
	if (ocscondvars[ocslockid] == MAP_FAILED) {
		syslog(LOG_ERR, "Ocslock Init: failed condvar mmap: handle(%d), lock(%s) error(%s)\n", 
			shm_handle, OCSLOCK_STRING[ocslockid], strerror(errno));
		return -1;
	}

	if(condvar_initialize(ocscondvars[ocslockid]) != 0){
		syslog(LOG_ERR, "Ocslock Init: cond var init failed for lock(%s)\n", OCSLOCK_STRING[ocslockid]);
		return -1;
	}
	
	return 0;	
}

/*
 * Private method: get mutex handle
 */
int get_ocslock_handle(ocslock_t ocslockid) {
	if(ocslockid >= NUM_OCSLOCKS) {
		syslog(LOG_ERR, "ocslock get_ocslock_handle: ocslock id (%d) not valid\n", (int)ocslockid); 
		return -1;
	}
	
	if(ocsmutexes[ocslockid]!=NULL && ocscondvars[ocslockid]!=NULL) 
		return 0;

	int rc;
	rc = pthread_rwlock_wrlock(&ocslock_initlock);
	if (rc) {
		syslog(LOG_ERR, "Ocslock getocslockhandle: atomic gethandle lock failed, rc[%d] error(%s)", rc, strerror(errno));
		return rc;
	}

	int ret = 0;
	if(ocsmutexes[ocslockid]==NULL || ocscondvars[ocslockid]==NULL) {
	    int shm_handle = shm_open(OCSLOCK_STRING[ocslockid], O_RDWR, 0777);
	    if(shm_handle < 0) {
	    	syslog(LOG_ERR, "Ocslock Handle: failed to open shared memory: return(%d) lock(%s) error(%s)\n", 
				shm_handle, OCSLOCK_STRING[ocslockid], strerror(errno));
	        ret = -1;
	    }
	    else {
	    	ocslock_info_t *ocslock_info_ptr = (ocslock_info_t*)mmap(NULL, sizeof(ocslock_info_t), PROT_READ | PROT_WRITE, MAP_SHARED, shm_handle, 0);

			if(ocsmutexes[ocslockid]==NULL) {
				ocsmutexes[ocslockid] = (pthread_mutex_t*)(&(ocslock_info_ptr->mutex_t));
				if (ocsmutexes[ocslockid] == MAP_FAILED) {
				   syslog(LOG_ERR, "Ocslock Mutex Mmap: failed mmap: handle(%d) lock(%s) error(%s)\n", 
						shm_handle, OCSLOCK_STRING[ocslockid], strerror(errno));
			        ret = -1;
				}
			}
			
			if(ocscondvars[ocslockid]==NULL) {
				ocscondvars[ocslockid] = (pthread_cond_t*)(&(ocslock_info_ptr->condvar_t));
				if (ocscondvars[ocslockid] == MAP_FAILED) {
					syslog(LOG_ERR, "Ocslock Condvar Mmap: failed mmap: handle(%d) lock(%s) error(%s)\n", 
						shm_handle, OCSLOCK_STRING[ocslockid], strerror(errno));
					ret = -1;
				}
			}
	    }
	}
	
	rc = pthread_rwlock_unlock(&ocslock_initlock);
	if (rc) {
		syslog(LOG_ERR, "Ocslock getocslockhandle: atomic gethandle unlock failed, rc[%d] error(%s)", rc, strerror(errno));
	}

	if(ocsmutexes[ocslockid]==NULL || ocscondvars[ocslockid]==NULL) 
		ret = -1;

    return ret;
}

/******************************************************************************
*	Function Name: Ocs Unlock 
*	Purpose: Release the mutex 
*	In parameters: None
*	Return value: 0 for success. -1 if something failed.
*	Comments/Notes:
*******************************************************************************/
int ocs_unlock(ocslock_t ocslockid) { 
	int ret;
	ret = get_ocslock_handle(ocslockid);
	if(ret != 0) {
		syslog(LOG_ERR, "ocs_unlock: Could not get ocslock handle for lockid(%d)\n", ocslockid); 
		return -1;
	}
	ret = pthread_mutex_unlock(ocsmutexes[ocslockid]);
	if(ret != 0)
		syslog(LOG_ERR, "Ocslock - unlock failed with return(%d) for lock(%s) error(%s)\n", 
			ret, OCSLOCK_STRING[ocslockid], strerror(errno));
	return ret;	
}

/******************************************************************************
*	Function Name: OcsLock
*	Purpose: Check for and wait on the pthread mutex 
*	In parameters: None
*	Return value: 0 for success. -1 if something failed.
	Comments/Notes:
*******************************************************************************/
int ocs_lock(ocslock_t ocslockid) {
	int ret;
	ret = get_ocslock_handle(ocslockid);
	if(ret != 0) {
		syslog(LOG_ERR, "ocs_lock: Could not get ocslock handle for lockid(%d)\n", ocslockid); 
		return -1;
	}
	
	struct timespec maxtime; 
    	clock_gettime(CLOCK_REALTIME , &maxtime); 
    	maxtime.tv_sec += 5; 
	ret = pthread_mutex_timedlock(ocsmutexes[ocslockid], &maxtime);
	if(ret != 0) {
		if(ret == EOWNERDEAD || errno == EOWNERDEAD) {
			syslog(LOG_INFO, "owner dead: attempting to recover for lock(%s) error(%s)\n", OCSLOCK_STRING[ocslockid], strerror(errno));

			if (mutex_recovery != NULL) {
				if ((*mutex_recovery)() != 0) {
					syslog(LOG_ERR, "EOWNERDEAD mutex recovery failed for lock(%s)\n", OCSLOCK_STRING[ocslockid]);
				}
			}

			if(pthread_mutex_consistent(ocsmutexes[ocslockid]) != 0) { 
				syslog(LOG_ERR, "mutex pthread_mutex_consistent failed for lock(%s) error(%s)\n", OCSLOCK_STRING[ocslockid], strerror(errno));
				return -1;
			}
		}
		else if(errno == ETIMEDOUT || ret == ETIMEDOUT) {
			syslog(LOG_ERR, "ocslock timeout: return (%d) for lock(%s) error(%s)\n", ret, OCSLOCK_STRING[ocslockid], strerror(errno));
			return -1;
		}
		else {
			syslog(LOG_ERR, "ocslock mutex lock failed for lock(%s) with return(%d) error(%s)\n", OCSLOCK_STRING[ocslockid], ret, strerror(errno));
			return -1;
		}
	}
	return 0;
}

/******************************************************************************
*	Function Description: Ocs Conditional Signal 
*	Purpose: Signal the conditional variable 
*	In parameters: None
*	Return value: 0 for success. -1 if something failed.
*	Comments/Notes:
*******************************************************************************/
int ocs_condsignal(ocslock_t ocslockid) { 
	int ret;
	ret = get_ocslock_handle(ocslockid);
	if(ret != 0) {
		syslog(LOG_ERR, "ocs_condsignal: Could not get ocslock handle for lockid(%d)\n", ocslockid); 
		return -1;
	}
	ret = pthread_cond_signal(ocscondvars[ocslockid]);
	if(ret != 0)
		syslog(LOG_ERR, "ocs_condsignal failed with return(%d) for lock(%s) error(%s)\n", 
			ret, OCSLOCK_STRING[ocslockid], strerror(errno));
	return ret;	
}

/******************************************************************************
*	Function Description: Ocs Conditional Wait
*	Purpose: Wait on the pthread conditional wait 
*	In parameters: None
*	Return value: 0 for success. -1 if something failed.
	Comments/Notes:
*******************************************************************************/
int ocs_condwait(ocslock_t ocslockid) {
	int ret;
	ret = get_ocslock_handle(ocslockid);
	if(ret != 0) {
		syslog(LOG_ERR, "ocs_lock ocs_condwait: Could not get ocslock handle for lockid(%d)\n", ocslockid); 
		return -1;
	}
	 
	ret = pthread_cond_wait(ocscondvars[ocslockid], ocsmutexes[ocslockid]);
	if(ret != 0) {
		if(ret == EOWNERDEAD || errno == EOWNERDEAD) {
			syslog(LOG_INFO, "ocs_condwait owner dead: attempting to recover for lock(%s) error(%s)\n", OCSLOCK_STRING[ocslockid], strerror(errno));
			return -1;
		}
		else if(errno == ETIMEDOUT || ret == ETIMEDOUT) {
			syslog(LOG_ERR, "ocs_condwait timeout (SHOULD NOT OCCUR): return (%d) for lock(%s) error(%s)\n", ret, OCSLOCK_STRING[ocslockid], strerror(errno));
			return -1;
		}
		else {
			syslog(LOG_ERR, "ocs_condwait mutex lock failed for lock(%s) with return(%d) error(%s)\n", OCSLOCK_STRING[ocslockid], ret, strerror(errno));
			return -1;
		}
	}
	return 0;
}
