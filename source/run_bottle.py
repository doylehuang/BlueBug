from bottle import route, run, Bottle

import sys
sys.path.append ("/usr/lib/commonapi")

import bottle
import ocslog
import resources
import view_helper

 
app = Bottle()         
resources.add_bottle_filters (app)
for resource in resources.REDFISH_RESOURCES.itervalues ():
    resource.register_resource (app)

run(app, host='0.0.0.0', port=9080, debug=True)




