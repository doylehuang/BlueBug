# -*- coding: UTF-8 -*-
#!/usr/bin/python

import os
import sys
import ctypes
from ctypes import *
from controls.utils import *
from utils_print import print_response


class command_name:
    """
    Enumration defination for the command name.
    """
    map = {
           0 : "GET_RM_STATE",
           1 : "SET_RM_STATE",
           2 : "SET_RM_CONFIG",
           
           3 : "GET_BLADE_STATE",
           4 : "SET_BLADE_STATE",
           5 : "SET_BLADE_CONFIG",
           
           #6 : "NUM_COMMANDS"           
    }
    
    def __init__(self,value):
        self.value = int(value)
        
    def __str__(self):
        return command_name.map[self.value]
    
    def __repr__(self):

        return str (self.value)
    
    def __int__(self):
        return self.value
    
class command_name_enum:
    """
    Enumertaion constants for the command name.
    """
    get_rm_state = command_name(0)
    set_rm_state = command_name(1)
    set_rm_config = command_name(2)
    get_blade_state = command_name(3)
    set_blade_state = command_name(4)
    set_blade_config = command_name(5)
    #num_commands = command_name(6)

def initialize_log():
    global log_binary
    try:
        if log_binary is None:
            log_binary = ctypes.cdll.LoadLibrary(log_lib)
            
        log_binary.log_init()
        
    except Exception,e:   
        #log_error("failed to get rm mode",e)
        print "Exception to get rm mode",e
        return -1
    
    return 0

    
def verify_caller_permission():
    global group_id
    global auth_binary
    
    try:
        if auth_binary is None:
            auth_binary = ctypes.cdll.LoadLibrary(auth_lib)
        
        caller_id = c_int()
        output = auth_binary.verify_caller_permission(byref(caller_id))
        
        if output == 0:
            group_id = caller_id.value
        else:
            #Log.Error("Failed to verify_caller_permission: ",output)
            #print "Failed to verify_caller_permission: ",output
            return -1
            
    except Exception, e:
        #print "Exception to verify caller permission:",e
        return -1
    
    return output
    
def pre_check_manager(command_id, deviceid):
    global precheck_binary
    
    global is_get_rm_call
    global is_set_rm_call
    global is_rm_config_call   
      
    try:
        if precheck_binary is None:
            precheck_binary = ctypes.cdll.LoadLibrary(precheck_lib)
        
        gp_id = c_int(int(group_id))
        cmd_id = c_int(int(command_id))
        dev_id = c_int(int(deviceid))
        rmid = c_int(int(rm_id))
        
        output = precheck_binary.pre_check(gp_id,cmd_id,dev_id,rmid)
        
        if output < 0:
            errordesc = create_string_buffer(256) 
            error = precheck_binary.get_app_error(output, errordesc) 
                         
            if error == 0:
                if errordesc.value.lower().strip() == "device is not present.".strip():
                    ret_val = {completion_code.cc_key:completion_code.notpresent, completion_code.desc:errordesc.value}
                    print_response(ret_val)
                    return False
                elif errordesc.value.lower().strip() == "device is not powered on.".strip():
                    ret_val = {completion_code.cc_key:completion_code.deviceoff, completion_code.desc:errordesc.value}
                    print_response(ret_val)
                    return False
                elif errordesc.value.lower().strip() == "device firmware is loading, retry again.".strip():
                    delay = c_int()
                    delay_output = precheck_binary.get_server_fwready_delay(dev_id, byref(delay))
                    if delay_output == 0:
                        ret_val = {completion_code.cc_key:completion_code.fwdecompress, completion_code.desc: "Server On. Firmware Decompression Time Remaining: {0} second(s)".format(delay.value)}
                        print_response(ret_val)
                        return False
                    else:
                        ret_val = {completion_code.cc_key:completion_code.fwdecompress, completion_code.desc: errordesc.value + "Delay time: Failure"}
                        print_response(ret_val)
                        return False
                else:
                    ret_val = {completion_code.cc_key:completion_code.failure, completion_code.desc:errordesc.value}
                    print_response(ret_val)
                    return False
            else:
                msg =  "Failed to call precheck get_app_error: ",error
                ret_val = {completion_code.cc_key:completion_code.failure, completion_code.desc:msg}
                print_response(ret_val)
                return False
            
        elif output > 0:
            print (completion_code.cc_key + ": " + completion_code.failure)
            print (completion_code.desc + ": {0}".format(output))
            return False
        else:
            if command_id == repr(command_name_enum.get_rm_state):
                is_get_rm_call = True
            elif command_id == repr(command_name_enum.set_rm_config):
                is_rm_config_call = True
            elif command_id == repr(command_name_enum.set_rm_state):
                is_set_rm_call = True
                
            return True
        
    except Exception, e:
        print_response((set_failure_dict("pre_check_manager(): Exception {0}".format(e), completion_code.failure)))        
        return False

def pre_check_helper (cmd_name, cache, device_id):
    if (cache):
        return True
    else:
        return pre_check_manager (repr (cmd_name), device_id) 
