#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import dbus.service
import collections
import math

from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
from utils import completion_code

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
SENSOR_THRESHOLD_INTERFACE = 'org.openbmc.SensorThresholds'
SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

bus = get_dbus()

def get_sensor_name(sensor_path):
    path_list = sensor_path.split("/")
    return path_list[-1]

#this table should ordered by sensor number
sensor_mainboard_temperature_table =\
[\
    "/org/openbmc/sensors/temperature/TMP5",\
    "/org/openbmc/sensors/temperature/TMP6",\
    "/org/openbmc/sensors/temperature/TMP7",\
    "/org/openbmc/sensors/temperature/TMP8",\
    "/org/openbmc/sensors/HSC/HSC1_TMP",\
    "/org/openbmc/sensors/HSC/HSC2_STBY_TMP",\
    "/org/openbmc/sensors/HSC/HSC3_GPU1_TMP",\
    "/org/openbmc/sensors/HSC/HSC4_GPU2_TMP",\
    "/org/openbmc/sensors/HSC/HSC5_GPU3_TMP",\
    "/org/openbmc/sensors/HSC/HSC6_GPU4_TMP",\
    "/org/openbmc/sensors/HSC/HSC7_GPU5_TMP",\
    "/org/openbmc/sensors/HSC/HSC8_GPU6_TMP",\
    "/org/openbmc/sensors/HSC/HSC9_GPU7_TMP",\
    "/org/openbmc/sensors/HSC/HSC10_GPU8_TMP",\
    "/org/openbmc/sensors/gpu/gpu1_temp",\
    "/org/openbmc/sensors/gpu/gpu2_temp",\
    "/org/openbmc/sensors/gpu/gpu3_temp",\
    "/org/openbmc/sensors/gpu/gpu4_temp",\
    "/org/openbmc/sensors/gpu/gpu5_temp",\
    "/org/openbmc/sensors/gpu/gpu6_temp",\
    "/org/openbmc/sensors/gpu/gpu7_temp",\
    "/org/openbmc/sensors/gpu/gpu8_temp",\
    "/org/openbmc/sensors/pmbus/pmbus01/temp_02",\
    "/org/openbmc/sensors/pmbus/pmbus02/temp_02",\
    "/org/openbmc/sensors/pmbus/pmbus03/temp_02",\
    "/org/openbmc/sensors/pmbus/pmbus04/temp_02",\
    "/org/openbmc/sensors/pmbus/pmbus05/temp_02",\
    "/org/openbmc/sensors/pmbus/pmbus06/temp_02",\
    #MSFT ask to hide in M1 release
    #"/org/openbmc/sensors/pcie/Mdot_2_temp1",\
    #"/org/openbmc/sensors/pcie/Mdot_2_temp2",\
    #"/org/openbmc/sensors/pcie/Mdot_2_temp3",\
    #"/org/openbmc/sensors/pcie/Mdot_2_temp4",\
]

sensor_fan_pwm_table =\
[\
    "/org/openbmc/control/fan/pwm1",
    "/org/openbmc/control/fan/pwm2",
    "/org/openbmc/control/fan/pwm3",
    "/org/openbmc/control/fan/pwm4",
    "/org/openbmc/control/fan/pwm5",
    "/org/openbmc/control/fan/pwm6"
]

#this table should ordered by sensor number
sensor_fan_rpm_table =\
[\
    "/org/openbmc/sensors/fan/fan_tacho1",
    "/org/openbmc/sensors/fan/fan_tacho2",
    "/org/openbmc/sensors/fan/fan_tacho3",
    "/org/openbmc/sensors/fan/fan_tacho4",
    "/org/openbmc/sensors/fan/fan_tacho5",
    "/org/openbmc/sensors/fan/fan_tacho6",
    "/org/openbmc/sensors/fan/fan_tacho7",
    "/org/openbmc/sensors/fan/fan_tacho8",
    "/org/openbmc/sensors/fan/fan_tacho9",
    "/org/openbmc/sensors/fan/fan_tacho10",
    "/org/openbmc/sensors/fan/fan_tacho11",
    "/org/openbmc/sensors/fan/fan_tacho12"
]

def get_chassis_thermal():
    result = {}
    result['temperatures'] = collections.OrderedDict()
    result['fans'] = collections.OrderedDict()

    try:
        for index in range(0, len(sensor_mainboard_temperature_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['value'] = 0
            property['upper_critical_threshold'] = 0

            object = bus.get_object(DBUS_NAME, sensor_mainboard_temperature_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            scale = interface.Get(SENSOR_HWMON_INTERFACE, 'scale')

            value = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['value'] = value

            property['upper_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_upper')

            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')
            property['sensor_name'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensor_name')

            result['temperatures'][index] = property

        for index in range(0, len(sensor_fan_rpm_table)):
            property = {}
            property['sensor_id'] = index+1
            property['sensor_number'] = 0
            property['lower_critical_threshold'] = 0
            property['value'] = 0
            property['PWM'] = 0

            object = bus.get_object(DBUS_NAME, sensor_fan_pwm_table[index/2])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            property['PWM'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            object = bus.get_object(DBUS_NAME, sensor_fan_rpm_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)

            property['sensor_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensornumber')
            property['sensor_name'] = interface.Get(SENSOR_HWMON_INTERFACE, 'sensor_name')
            property['value'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')

            property['lower_critical_threshold'] = interface.Get(SENSOR_THRESHOLD_INTERFACE, 'critical_lower')

            result['fans'][index] = property

    except Exception, e:
        print "!!! DBus error !!!\n"

    return result
