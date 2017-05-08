#!/usr/bin/python
# -*- coding: utf-8 -*-


import datetime
import obmc_dbuslib
from manage_network import *
from manage_fwversion import *
import subprocess
import dbus
import dbus.service
import collections
from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager
import shutil

def PSU_switch_phase(bus, slaveaddress, pmbusphase):
    PSU_PHASE = '0x04'
    cmd = 'i2cset -y -f ' + bus + ' ' + slaveaddress + ' ' + PSU_PHASE + ' ' + pmbusphase
    return subprocess.call(cmd, shell=True)


def bmc_i2c_master_phase_write_read(bus, slaveaddress, pmbusphase, readcount, writedata):
    result = {}
    if (("0x" in slaveaddress) & ("0x" in pmbusphase) & ("0x" in writedata)) != True:
        return set_failure_dict("Hexadecimal numbers must prefixed with 0x?", completion_code.failure)

    if (int(pmbusphase.replace('0x', '')) > 2):
        return set_failure_dict("PSU phase value must be between 0~2", completion_code.failure)
    if PSU_switch_phase(bus, slaveaddress, pmbusphase) != 0:
        return set_failure_dict("Switching PSU phase failed", completion_code.failure)

    if int(readcount.replace('0x', '')) == 0 :
        cmd = 'i2cset -y -f ' +  bus + ' ' + slaveaddress + ' ' + writedata
        return_code = subprocess.call(cmd, shell = True)
        if return_code != 0:
            if PSU_switch_phase(bus, slaveaddress, "0xFF") != 0:
                return set_failure_dict("Switching to default phase failed", completion_code.failure)
            return set_failure_dict("Write failed", completion_code.failure)
        else:
            result["BytesRead"] = 'Write success'
    else:
        if int(readcount.replace('0x', '')) == 1:
            tool = 'i2cget'
            op = 'b'
        elif int(readcount.replace('0x', '')) == 2:
            tool = 'i2cget'
            op = 'w'
        else:
            if PSU_switch_phase(bus, slaveaddress, "0xFF") != 0:
                return set_failure_dict("Switching to default phase failed", completion_code.failure)
            return set_failure_dict("ReadCount value must be between 0~2", completion_code.failure)

        cmd = tool  +' -y -f ' + bus + ' ' + slaveaddress + ' ' + writedata + ' ' + op
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell = True)
        (rdata, return_code) = proc.communicate()
        newdata = rdata.replace('\n', ' ')
        if newdata != "":
            result["BytesRead"] = str(newdata)
        else:
            if PSU_switch_phase(bus, slaveaddress, "0xFF") != 0:
                return set_failure_dict("Switching to default phase failed", completion_code.failure)
            return set_failure_dict("I2C Read failed", completion_code.failure)
    result[completion_code.cc_key] = completion_code.success
    if PSU_switch_phase(bus, slaveaddress, "0xFF") != 0:
        return set_failure_dict("Switching to default phase failed", completion_code.failure)
    return result


def bmc_i2c_master_write_read(bus, slaveaddress, readcount, writedata):
    result = {}
    if (("0x" in slaveaddress) & ("0x" in writedata)) != True:
        return set_failure_dict("Hexadecimal numbers must prefixed with 0x?", completion_code.failure)
    if int(readcount.replace('0x', '')) == 0 :
        cmd = 'i2cset -y -f ' +  bus + ' ' + slaveaddress + ' ' + writedata
        return_code = subprocess.call(cmd, shell = True)
        if return_code != 0:
            return set_failure_dict("Write failed", completion_code.failure)
        else:
            result["BytesRead"] = 'Write success'
    else:
        if int(readcount.replace('0x', '')) == 1:
            tool = 'i2cget'
            op = 'b'
        elif int(readcount.replace('0x', '')) == 2:
            tool = 'i2cget'
            op = 'w'
        else:
            return set_failure_dict("ReadCount value must be between 0~2", completion_code.failure)

        cmd = tool  +' -y -f ' + bus + ' ' + slaveaddress + ' ' + writedata + ' ' + op
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell = True)
        (rdata, return_code) = proc.communicate()
        newdata = rdata.replace('\n', ' ')
        if newdata != "":
            result["BytesRead"] = str(newdata)
        else:
            return set_failure_dict("I2C Read failed", completion_code.failure)
    result[completion_code.cc_key] = completion_code.success
    return result


def get_bmc_slot_id():
    result = {}
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.get_slot_id()
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)
    result["SLOT_ID"] = str(pydata)
    result[completion_code.cc_key] = completion_code.success
    return result

def set_bmc_warm_reset(action):
    result = {}
    if action.upper() == 'WARMRESET':
        op = 'WarmReset'
    else:
        return set_failure_dict("Unknown parameter", completion_code.failure)
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.bmc_reset_operation(str(op))
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    return set_success_dict(result)


def set_bmc_fwupdate(action):
    result = {}
    if action.upper() == 'PREPARE':
        op = 'Prepare'
    elif action.upper() == 'APPLY':
        op = 'Apply'
    elif action.upper() == 'ABORT':
        op = 'Abort'
    else:
        return set_failure_dict("Unknown parameter", completion_code.failure)
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.fw_update_operation(str(op))
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    return set_success_dict(result)

def set_bmc_fwupdate_push_mode(imageuri, transferprotocol):
    image_base_path = '/var/wcs/home/'
    op = 'Prepare'
    result = {}
    result["RetStatus"] = "OK"
    old_file = ""
    new_file = ""
    try:
        sp_imageuri = imageuri.split("//")
        old_file = image_base_path+sp_imageuri[1].split("?")[0]
        new_file = image_base_path+"image-bmc"
        body = sp_imageuri[1].split("?")[1].replace("component=", "").replace("partition=", "")
        component = body.split("&")[0].rstrip()
        partition = body.split("&")[1].rstrip()
        if component != 'bmc':
            result["RetStatus"] = 'Post [ImageURI] Parameter error - component setting must be bmc'
            return set_success_dict(result)
        elif partition != 'primary':
            result["RetStatus"] = 'Post [ImageURI] Parameter error - partition setting must be primary'
            return set_success_dict(result)
    except:
        result["RetStatus"] = 'Post [ImageURI] format Parameter error'
        return set_success_dict(result)

    if  transferprotocol.rstrip() != 'OEM':
        result["RetStatus"] = 'Post [transferprotocol] Parameter error - transferprotocol setting must be OEM'
        return set_success_dict(result)

    try:
        shutil.move(old_file, new_file)
    except:
        result["RetStatus"] = 'File not exist!!! [' + old_file + ']'
        return set_success_dict(result)

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.fw_update_operation(str(op))
    except Exception, e:
        return set_failure_dict(('Exception:', e), completion_code.failure)

    result["RetStatus"] = "OK"
    return set_success_dict(result)

def get_bmc_fwupdate_state(action):
    result = {}

    if action.upper() == 'QUERY':
        op = 'Query'
        try:
            dbusctl = obmc_dbuslib.ObmcRedfishProviders()
            pydata = dbusctl.fw_update_operation(str(op))
            newdata = pydata.replace('\n', '  ')
        except Exception, e:
            return set_failure_dict(('Exception:', e), completion_code.failure)
    else:
        return set_failure_dict("Unknown parameter", completion_code.failure)
    result["UPDATE_PROGRESS"] = newdata
    result[completion_code.cc_key] = completion_code.success
    return result


def set_bmc_attention_led(setting):
    result = {}
    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        dbusctl.led_operation(str(setting), 'identify')
    
    except Exception,e:
        return set_failure_dict(('Exception:', e),completion_code.failure)

    return set_success_dict(result)


def get_bmc_attention_led_status():
    result = {}

    try:
        dbusctl = obmc_dbuslib.ObmcRedfishProviders()
        pydata = dbusctl.led_operation('state', 'identify')

    except Exception,e:
        return set_failure_dict(('Exception:', e),completion_code.failure)
    
    if(pydata == 'Off'):
        result["indicator_led"] = 'Off'
        result['health_status'] = 'OK'
    elif (pydata == 'Lit'):
        result["indicator_led"] = 'Lit'
        result['health_status'] = 'Fail'
    elif (pydata == 'Blinking'):
        result["indicator_led"] = 'Blinking'
    else:
        result["indicator_led"] = 'Unknown'
        
    return set_success_dict(result)

def get_bmc_health_status():
    DBUS_NAME = 'org.openbmc.Sensors'
    DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'
    SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'
    HWMONSENSOR_INTERFACE = 'org.openbmc.HwmonSensor'

    pbus = get_dbus()
    try:
        result = {}
        object = pbus.get_object(DBUS_NAME, "/org/openbmc/sensors/bmc_health")
        interface = dbus.Interface(object, DBUS_INTERFACE)
        result["serial_number"] = interface.Get(HWMONSENSOR_INTERFACE, 'sensornumber')
        val = interface.Get(SENSOR_VALUE_INTERFACE, 'value')
        if val >= 0 and val < 0xff:
            result["bmc_health_status"] = hex(val)
        elif val == 0xff:
            result["bmc_health_status"] = ""
        else:
            result["bmc_health_status"] = "unknown error"
        result["bmc_health_value"] = hex(val)
    except Exception,e:
        return set_failure_dict(('Exception:', e),completion_code.failure)
    return set_success_dict(result)


def get_bmc_attention_cableled_status():
    import dbus
    import dbus.service
    import collections
    from obmc.dbuslib.bindings import get_dbus, DbusProperties, DbusObjectManager

    sensor_mainboard_cableled_table = [
        "/org/openbmc/control/cable_led/led0",
        "/org/openbmc/control/cable_led/led1",
        "/org/openbmc/control/cable_led/led2",
        "/org/openbmc/control/cable_led/led3",
        "/org/openbmc/control/cable_led/led4",
        "/org/openbmc/control/cable_led/led5",
        "/org/openbmc/control/cable_led/led6",
        "/org/openbmc/control/cable_led/led7",
        "/org/openbmc/control/cable_led/led8",
        "/org/openbmc/control/cable_led/led9",
        "/org/openbmc/control/cable_led/led10",
        "/org/openbmc/control/cable_led/led11",
        "/org/openbmc/control/cable_led/led12",
        "/org/openbmc/control/cable_led/led13",
        "/org/openbmc/control/cable_led/led14",
        "/org/openbmc/control/cable_led/led15",
    ]
    DBUS_NAME = 'org.openbmc.Sensors'
    DBUS_INTERFACE = 'org.freedesktop.DBus.Properties'
    SENSOR_VALUE_INTERFACE = 'org.openbmc.SensorValue'

    result = {}
    result['cableleds'] = collections.OrderedDict()
    pbus = get_dbus()
    try:
        for index in range(0, len(sensor_mainboard_cableled_table)):
            property = {}
            object = pbus.get_object(DBUS_NAME, sensor_mainboard_cableled_table[index])
            interface = dbus.Interface(object, DBUS_INTERFACE)
            sp_name = sensor_mainboard_cableled_table[index].split("/")
            property["sensor_name"] = sp_name[len(sp_name)-1]
            property['value'] = interface.Get(SENSOR_VALUE_INTERFACE, 'value')
            result['cableleds'][str(index)] = property

    except Exception,e:
        return set_failure_dict(('Exception:', e),completion_code.failure)
        
    return set_success_dict(result)


def show_bmc_hostname():
    result = {}

    result["Hostname"] = socket.gethostname()
    result[completion_code.cc_key] = completion_code.success

    return result




def get_bmc_time():
    """ Returns current date and time in UTC
    """
    try:
        result = {}

        now = str(datetime.datetime.utcnow())

        result["Year"] = now[0:4]
        result["Month"] = now[5:7]
        result["Day"] = now[8:10]
        result["Hour"] = now[11:13]
        result["Min"] = now[14:16]
        result["Sec"] = now[17:19]

        return set_success_dict(result)

    except Exception, e:
        return set_failure_dict("get_bmc_time() Exception: {0}".format(e))


def show_bmc_time(edm=False):
    """ Returns formatted date and time in UTC
    """
    try:
        result = {}

        now = get_bmc_time()

        if edm:
            result["DateTime"] = "{0}-{1}-{2}T{3}:{4}:{5}Z".format(now["Year"], now["Month"], now["Day"],
                                                                   now["Hour"], now["Min"], now["Sec"])
        else:
            result["DateTime"] = "{0}-{1}-{2} {3}:{4}:{5}".format(now["Year"], now["Month"], now["Day"],
                                                                  now["Hour"], now["Min"], now["Sec"])

        return set_success_dict(result)

    except Exception, e:
        return set_failure_dict("show_rack_manager_time() Exception: {0}".format(e))


def set_bmc_time(datetime=None, hour=-1, min=-1, sec=-1, month=-1, day=-1, year=-1):
    """ Sets system date and time
    """
    try:
        if datetime is not None:
            year, month, day, hour, min, sec = re.findall("\\d+", datetime)
        else:
            now = get_bmc_time()

            if hour == -1:
                hour = now["Hour"]
            elif hour > 23 or hour < 0:
                return set_failure_dict("Hour value out of range (0-23): {0}".format(hour), completion_code.failure)
            if min == -1:
                min = now["Min"]
            elif min > 59 or min < 0:
                return set_failure_dict("Minute value out of range (0-59): {0}".format(min), completion_code.failure)
            if sec == -1:
                sec = now["Sec"]
            elif sec > 59 or sec < 0:
                return set_failure_dict("Second value out of range (0-59): {0}".format(sec), completion_code.failure)
            if month == -1:
                month = now["Month"]
            elif month > 12 or month < 1:
                return set_failure_dict("Month value out of range (1-12): {0}".format(month), completion_code.failure)
            if day == -1:
                day = now["Day"]
            elif day > 31 or day < 1:
                return set_failure_dict("Day value out of range (1-31): {0}".format(day), completion_code.failure)
            if year == -1:
                year = now["Year"]

        newdate = "{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day, hour, min, sec)

        pipe = subprocess.check_output(["date", "-s", newdate], stderr=subprocess.STDOUT)

        return set_success_dict()

    except subprocess.CalledProcessError as e:
        return set_failure_dict("Failed to set system time: {0}".format(e.output.strip()), completion_code.failure)

    except Exception, e:
        return set_failure_dict("set_rack_manager_time() Exception: {0}".format(e))
