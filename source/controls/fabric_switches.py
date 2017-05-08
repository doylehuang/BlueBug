#**************************************************************
#*                                                            *
#*   Copyright (C) Microsoft Corporation. All rights reserved.*
#*                                                            *
#**************************************************************

import dbus
import collections
from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager

bus = get_dbus()

DBUS_NAME = 'org.openbmc.Sensors'
DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'

SENSOR_HWMON_INTERFACE = 'org.openbmc.HwmonSensor'

port_object_path_table = \
[["/org/openbmc/sensors/gpu/gpu1_temp","/org/openbmc/sensors/gpu/gpu3_temp"], \
 ["/org/openbmc/sensors/gpu/gpu2_temp","/org/openbmc/sensors/gpu/gpu4_temp"], \
 ["/org/openbmc/sensors/gpu/gpu5_temp","/org/openbmc/sensors/gpu/gpu7_temp"], \
 ["/org/openbmc/sensors/gpu/gpu6_temp","/org/openbmc/sensors/gpu/gpu8_temp"]]

switches_object_path_table = \
[\
    "/org/openbmc/sensors/pxe/pxe0",\
    "/org/openbmc/sensors/pxe/pxe1",\
    "/org/openbmc/sensors/pxe/pxe2",\
    "/org/openbmc/sensors/pxe/pxe3"
]

def get_switches_devices(switches_id):
    result = {}
    result['ID'] = switches_id
    result['info'] = collections.OrderedDict()
    property = {}

    try:
        object = bus.get_object(DBUS_NAME, switches_object_path_table[switches_id-1])
        interface = dbus.Interface(object, DBUS_INTERFACE)
        property['serialnumber'] = interface.Get(SENSOR_HWMON_INTERFACE, 'Serial Number')
        property['udid'] = interface.Get(SENSOR_HWMON_INTERFACE, 'UDID')
        result['STATUS'] = "Enabled"
        result['HEALTH'] = "OK"

    except Exception as e:
        property['serialnumber'] = 'unknown'
        property['udid'] = 'unknown'
        result['STATUS'] = "Disabled"
        result['HEALTH'] = "Failed"

    result['info'] = property

    return result

def get_switches_ports(switches_id):
    result = {}
    result['ID'] = switches_id
    return result

def get_switches_ports_devices(switches_id, ports_id):
    result = {}
    object = bus.get_object(DBUS_NAME, port_object_path_table[switches_id-1][ports_id-1])
    interface = dbus.Interface(object, DBUS_INTERFACE)
    result['ID'] = switches_id
    result['PORT'] = ports_id
    try:
        name = interface.Get(SENSOR_HWMON_INTERFACE, 'Marketing Name')
        result['NAME'] = "PCIe Downstream GPU Port" + str(ports_id) +',' + name
        result['STATUS'] = "Enabled"
        result['HEALTH'] = "OK"
    except Exception as e:
        result['NAME'] = "unknown"
        result['STATUS'] = "Disabled"
        result['HEALTH'] = "Failed"

    return result