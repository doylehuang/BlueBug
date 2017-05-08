
from manage_bmc import *


############################################################################################################
# Network interface 
###########################################################################################################

def ethernet_actions_results(res):
    try:
        results = {}
        
        if (res['status_code'] == 0):
                results = set_success_dict ()
        else:
            error_data = res['stderr'].split('\n')
            results = set_failure_dict (error_data)
            results['Error Code'] = res['status_code']
            
    except Exception, e:
        #Log_Error("Ethernet interface action parse results exception  :",e)
        return set_failure_dict(('Exception:',e),completion_code.failure)
    
    return results
