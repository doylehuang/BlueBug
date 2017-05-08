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

gpu_object_path_table =\
[\
    "/org/openbmc/sensors/gpu/gpu1_temp",\
    "/org/openbmc/sensors/gpu/gpu2_temp",\
    "/org/openbmc/sensors/gpu/gpu3_temp",\
    "/org/openbmc/sensors/gpu/gpu4_temp",\
    "/org/openbmc/sensors/gpu/gpu5_temp",\
    "/org/openbmc/sensors/gpu/gpu6_temp",\
    "/org/openbmc/sensors/gpu/gpu7_temp",\
    "/org/openbmc/sensors/gpu/gpu8_temp"
]

manufacturer_mapping_table =\
{
    '032': 'Foxconn'
}

model_mapping_table =\
{
    '15F8': 'P100'
}

def get_chassis_pcie_devices(pcie_id):
    result = {}
    result['ID'] = pcie_id
    result['info'] = collections.OrderedDict()
    property = {}

    object = bus.get_object(DBUS_NAME, gpu_object_path_table[pcie_id-1])
    interface = dbus.Interface(object, DBUS_INTERFACE)

    try:
        property['serial_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'Serial Number')
        property['marketing_name'] = interface.Get(SENSOR_HWMON_INTERFACE, 'Marketing Name')
        property['gpu_part_number'] = interface.Get(SENSOR_HWMON_INTERFACE, 'PartNumber')
        property['firmware_version'] = interface.Get(SENSOR_HWMON_INTERFACE, 'FirmwareVersion')
        property['description'] = property['marketing_name']

        property['manufacturer'] = 'unknown'
        manufacturer_number = property['serial_number'][0:3]
        if manufacturer_mapping_table.has_key(manufacturer_number):
            property['manufacturer'] = manufacturer_mapping_table[manufacturer_number]

        # gpu part number format: device_id-SKU-GPU_Revision
        property['model'] = 'unknown'
        gpu_part_number_items = property['gpu_part_number'].split('-')
        model_number = gpu_part_number_items[0]
        if model_mapping_table.has_key(model_number):
            property['model'] = model_mapping_table[model_number]
        property['sku'] = gpu_part_number_items[1]
    except Exception as e:
        property['serial_number'] = 'unknown'
        property['marketing_name'] = 'unknown'
        property['gpu_part_number'] = 'unknown'
        property['firmware_version'] = 'unknown'
        property['description'] = 'unknown'
        property['manufacturer'] = 'unknown'
        property['model'] = 'unknown'
        property['sku'] = 'unknown'

    result['info'] = property

    return result

def get_chassis_pcie_devices_functions(pcie_id, func):
    result = {}
    result['ID'] = pcie_id
    result['FUNC'] = func

    return result
