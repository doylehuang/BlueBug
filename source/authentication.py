# -*- coding: UTF-8 -*-

import ocslog
#TODO from ocsaudit_log import *
from ctypes import c_int, byref, c_char_p
from bottle import request, HTTPError
from controls.manage_user import group_id_from_usr_name
from controls.lib_utils import get_precheck_library, get_authentication_library
from controls.obmc_dbuslib import ObmcRedfishProviders
from controls.manage_fwversion import *

dbusctl = ObmcRedfishProviders()

def pre_check_slot_id (slot_id):
    expected_slot_id =  dbusctl.get_slot_id()
    if str(expected_slot_id) == str(slot_id):
        return
    else:
        raise HTTPError(status=403, body="System is not present.")



    
def pre_check_function_call (op_category, device_id = 0):
    return  #TODO#
    try:
        # Log request in audit log
        username = get_current_username ()
        ocsaudit_rest_log_command (request.method, request.url, request.url_args, username)
        
        precheck_binary = get_precheck_library ()
            
        gp_id = c_int (get_current_role ())
        op_id = c_int (int (op_category))
        dev_id = c_int (int (device_id))
        
        output = precheck_binary.pre_check (gp_id, op_id, dev_id)
        
    except Exception as error:
        ocslog.log_error ("Exception calling pre-check manager", error)
        raise
    
    if (output == -4):
        raise HTTPError (status = 403, body = "System is not present.")
    elif (output == -5):
        raise HTTPError (status = 403, body = "System is not powered.")
    elif (output == -6):
        raise HTTPError (status = 403, body = "System firmware is loading.")
    elif (output != 0):
        raise HTTPError (status = 401)

def validate_user (username, password):
    try:
        auth_binary = get_authentication_library ()
            
        usr = c_char_p (username)
        psw = c_char_p (password)            
        auth = auth_binary.verify_authentication (usr, psw)  
    
        if auth == 0:
            return True
        else:
            return False
    except Exception as error:
        ocslog.log_error ("Failed to check user authentication", error)
        return False
    
def get_current_username ():
    try:
        user = request.auth or (None, None)
        if user is not None:
            return user[0]
        else:
            return None
    except:
        return None
    
def get_current_role ():
    username = get_current_username ()
    return group_id_from_usr_name (username)
