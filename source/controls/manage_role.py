#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import ctypes
from ctypes import *
from utils import *

auth_lib = '/usr/lib/libocsauth.so'

def ocs_group_list():    
    # List all available OCS User roles    
    # Ocs user roles are group id 
    # admin: group id 0
    # operator: group id 37
    # user: group id 100
        
    output = {}
    roles = {}
    
    output = {"admin":"admin",
            "operator":"operator",
            "user":"user"}
    roles["roles"] = output
    roles["role_number"] = len(output)
    
    return roles

def group_detail_by_name(g_name):    
    result={}
    id=0
    
    id =  get_group_id_by_name(g_name)
    result["name"] =g_name
    
    if id == 0:
        message= ('Incorrect role name: %s',g_name)
        result["role"] ={"Status":"Failed", "Error": message }        
        return result
        
    if g_name =="admin":
        result["role"]= {                         
                       "Id": id,
                       "Name": "admin",
                       "Description": "Administrator Role",
                       "IsPredefined": "True",
                       "AssignedPrivileges": {
                                              "Login" :"Log in to application",
                                              "ConfigureManager":"configure application",
                                              "ConfigureUsers":"configure users",
                                              "ConfigureSelf":"configure self",
                                              "ConfigureDevice":"configure device"
                                              },
                       "OemPrivileges": {
                                         "OemClearLog":"clear log",
                                         "OemPowerControl":"power control"
                                         }
                       }   
                          
    elif g_name =="operator":
        result["role"] = {
                    "Id": id,
                    "Name": "Operator",
                    "Description": "Operator Role",
                    "IsPredefined": "True",
                    "AssignedPrivileges": {
                                            "Login" :"Log in to app",                                           
                                            "ConfigureSelf":"configure self",
                                            "ConfigureDevice":"configure device"
                                           },
                    "OemPrivileges": {}                    
                    }
    elif g_name =="user":
        result["role"] ={
                     "Id": id,
                     "Name": "user",
                     "Description": "ReadOnlyUser User Role",
                     "IsPredefined": "True",
                     "AssignedPrivileges": {                                            
                                             "Login" :"Log in to application",                                            
                                            },
                     "OemPrivileges": {}
                     }
    else:
        message="Group name is not supported"
        result["role"] ={"Status":"Failed", "Error":message }
    
    return result

def get_group_id_by_name(group_name):
    
    id=0
    try:
        g_name=c_char_p(group_name)
        g_id = c_int()
        
        if os.path.isfile(auth_lib) :
            auth_binary = ctypes.cdll.LoadLibrary(auth_lib)
            
        if auth_binary is None:
            return set_failure_dict("Failed to load csauth library.",completion_code.failure)

        ret = auth_binary.ocs_group_id(g_name, byref(g_id))    
        
        if ( ret ==0 ):
            id = g_id.value
    
    except:
        #log error message
        pass
        
    return id
        
    