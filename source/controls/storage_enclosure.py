#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import obmc_dbuslib
import sys
import math
import time

sys.path.append ("/usr/sbin")

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from controls.utils import set_failure_dict, completion_code

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

bus = get_dbus()

MAX_EXPANDER_DRIVES = 22

def get_sensor_name(sensor_path):
    path_list = sensor_path.split("/")
    return path_list[-1]

def string_to_int(input_data):
    temp = [input_data[x:x+3] for x in xrange(0, len(input_data), 3)]
    output_data = [int(temp[x],16) for x in range(0,len(temp))]

    return output_data

def get_id_led_state(expander_id): #TBD
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.power_control('state')

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    if(int(pydata) == 0):
        result['id_led'] = 'Off'
    else:
        result['id_led'] = 'On'

    result[completion_code.cc_key] = completion_code.success

    return result

def get_expander_fru(expander_id):
    result = {}
    fru_name = 'STORAGEENCLOSURE'+str(expander_id)
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        result = dbusctl.get_fru_info(fru_name)

    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)
    
    result['SE_ID'] = expander_id
    result[completion_code.cc_key] = completion_code.success

    return result

def set_expander_drive_power(expander_id, drive_id, state):
    result = {}
    result[completion_code.cc_key] = completion_code.success
    return result

def get_expander_power(expander_id):
    result = {}
    result[completion_code.cc_key] = completion_code.success
    return result

sensor_expander1_temperature_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_HSC_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Top_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Bot_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Expander_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive1_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive2_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive3_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive4_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive5_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive6_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive7_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive8_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive9_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive10_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive11_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive12_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive13_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive14_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive15_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive16_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive17_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive18_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive19_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive20_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive21_Temp",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive22_Temp"
]
sensor_expander2_temperature_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_HSC_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Top_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Bot_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Expander_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive1_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive2_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive3_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive4_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive5_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive6_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive7_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive8_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive9_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive10_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive11_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive12_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive13_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive14_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive15_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive16_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive17_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive18_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive19_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive20_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive21_Temp",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive22_Temp"
]
sensor_expander3_temperature_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_HSC_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Top_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Bot_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Expander_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive1_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive2_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive3_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive4_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive5_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive6_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive7_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive8_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive9_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive10_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive11_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive12_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive13_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive14_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive15_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive16_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive17_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive18_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive19_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive20_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive21_Temp",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive22_Temp"
]
    
sensor_expander4_temperature_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_HSC_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Top_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Bot_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Expander_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive1_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive2_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive3_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive4_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive5_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive6_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive7_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive8_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive9_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive10_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive11_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive12_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive13_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive14_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive15_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive16_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive17_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive18_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive19_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive20_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive21_Temp",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive22_Temp"
]

sensor_expander1_power_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Brd_Status",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_Drive_Status",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_HSC_Power_Out",\
    "/org/openbmc/sensors/StorageEnclosure1/HDD1_HSC_Volt_Out"
]

sensor_expander2_power_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Brd_Status",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_Drive_Status",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_HSC_Power_Out",\
    "/org/openbmc/sensors/StorageEnclosure2/HDD2_HSC_Volt_Out"
]

sensor_expander3_power_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Brd_Status",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_Drive_Status",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_HSC_Power_Out",\
    "/org/openbmc/sensors/StorageEnclosure3/HDD3_HSC_Volt_Out"
]

sensor_expander4_power_table =\
[\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Brd_Status",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_Drive_Status",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_HSC_Power_Out",\
    "/org/openbmc/sensors/StorageEnclosure4/HDD4_HSC_Volt_Out"
]

def get_storage_enclosure_thermal(expander_id):
    result = {}
    result['SE_ID'] = expander_id
    result['temperatures'] = collections.OrderedDict()

    try:
        if(expander_id == 1):
            sensor_table = sensor_expander1_temperature_table
        elif(expander_id == 2):
            sensor_table = sensor_expander2_temperature_table
        elif(expander_id == 3):
            sensor_table = sensor_expander3_temperature_table
        elif(expander_id == 4):
            sensor_table = sensor_expander4_temperature_table
        else:
            print("Expander ID error!")
            return set_failure_dict(('Exception:', e), completion_code.failure)
        
        for index in range(0, len(sensor_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_name'] = get_sensor_name(sensor_table[index])
            property['sensor_number'] = 0
            property['celsius'] = 0
            property['upper_critical_threshold'] = 0

            object = bus.get_object(DBUS_NAME, sensor_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            properties = interface.GetAll(SENSOR_VALUE_INTERFACE)
            for property_name in properties:
                if property_name == 'value':
                    property['celsius'] = properties['value']

            property['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')

            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')

            result['temperatures'][str(index)] = property

    except Exception, e:
        print "!!! DBus error !!!\n"
    return result

def get_storage_enclosure_power(expander_id):
    result = {}

    try:
        if(expander_id == 1):
            sensor_table = sensor_expander1_power_table
        elif(expander_id == 2):
            sensor_table = sensor_expander2_power_table
        elif(expander_id == 3):
            sensor_table = sensor_expander3_power_table
        elif(expander_id == 4):
            sensor_table = sensor_expander4_power_table
        else:
            print("Expander ID error!")
            return set_failure_dict(('Exception:', e), completion_code.failure)
        
        result['SE_ID'] = expander_id
        result['power_consumption'] = 0
        result['sensor_number'] = 0
        result['voltage_value'] = 0
        result['upper_critical_threshold'] = 0
        result['lower_critical_threshold'] = 0

        object = bus.get_object(DBUS_NAME, sensor_table[2]) # HDD_HSC_Power_Out
        interface = dbus.Interface(object, DBUS_INTERFACE)

        scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')
        adjust = interface.Get(SENSOR_HWMON_INTERFACE, 'adjust')
        value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

        result['power_consumption'] = value * math.pow(10, scale) / adjust

        object = bus.get_object(DBUS_NAME, sensor_table[3]) # HDD_HSC_Volt_Out
        interface = dbus.Interface(object, DBUS_INTERFACE)

        result['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')

        scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')
        value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

        result['voltage_value'] = value * math.pow(10, scale)

        result['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')
        result['lower_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_lower')

    except Exception, e:
        print "!!! DBus error !!!\n"
    return result
