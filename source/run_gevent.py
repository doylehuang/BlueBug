#!/usr/bin/python
import sys
import os
import gevent
from gevent.pywsgi import WSGIServer

import bottle
import resources
import view_helper



default_cert = "/usr/lib/cert.pem"


class msocs_bottle(bottle.Bottle):
    def default_error_handler(self, res):
        bottle.response.content_type = "application/json"
        return view_helper.get_error_body(res.status_code, msg=res.body)


app = msocs_bottle(__name__)
resources.add_bottle_filters(app)
for resource in resources.REDFISH_RESOURCES.itervalues():
    resource.register_resource(app)

bind = ('', 443)

server = WSGIServer(
    bind, app, keyfile=default_cert, certfile=default_cert)
server.serve_forever()
