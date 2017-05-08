#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <syslog.h>

#include "ocslock.h"

int main()
{
	int ocslock_id, ret;

	for(ocslock_id=0; ocslock_id<NUM_OCSLOCKS; ocslock_id++) {
		ret = ocslock_init(ocslock_id);
		if(ret!=0)
			syslog(LOG_ERR, "Ocslock-Init for ocslockid %d failed with error code %d\n", ocslock_id, ret);
	}

	return 0;
}
