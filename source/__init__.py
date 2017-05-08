import sys
sys.path.append ("/usr/lib/commonapi")

import ocslog
import authentication

try:
    ocslog.initialize_log ()
    
except Exception as error:
    print "Failed to initialize the ocslog", error
    


import bottle
import resources
import view_helper

class msocs_bottle (bottle.Bottle):
    def default_error_handler (self, res):
        bottle.response.content_type = "application/json"
        return view_helper.get_error_body (res.status_code, msg = res.body)
 
app = msocs_bottle (__name__)
resources.add_bottle_filters (app)
for resource in resources.REDFISH_RESOURCES.itervalues ():
    resource.register_resource (app)