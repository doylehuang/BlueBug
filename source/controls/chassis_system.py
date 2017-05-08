#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import obmc_dbuslib

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code
from utils import set_failure_dict

bus = get_dbus()

def get_chassis_power_state():
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.power_control('state')

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    if(int(pydata) == 0):
        result['power_state'] = 'Off'
    else:
        result['power_state'] = 'On'

    result[completion_code.cc_key] = completion_code.success

    return result

def get_chassis_fru():
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        result = dbusctl.get_fru_info('MOTHERBOARD')
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    result[completion_code.cc_key] = completion_code.success

    return result

def post_chassis_action_power_on():
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.power_control('state')
        result = {}
        if(pydata == 1):
            result['SUPPORT']='not support in previous status'
        else:
            dbusctl.power_control('On')
            result['SUPPORT']='OK'
        result[completion_code.cc_key] = completion_code.success
        return result
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

def post_chassis_action_power_off():
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.power_control('state')
        result = {}
        if(pydata == 0):
            result['SUPPORT']='not support in previous status'
        else:
            dbusctl.power_control('ForceOff')
            result['SUPPORT']='OK'
        result[completion_code.cc_key] = completion_code.success
        return result
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)
