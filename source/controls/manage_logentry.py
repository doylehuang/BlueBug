'''
Event Log Manager
'''
import collections
import dbus
import dbus.service
import os

from controls.utils import completion_code
from obmc.dbuslib.bindings import get_dbus
from obmc.events import EventManager

_DBUS = get_dbus()
_DBUS_EVENT_LOG_INTERFACE = 'org.openbmc.recordlog'
_DBUS_OBJECT_PATH = '/org/openbmc/records/events'
_DBUS_SERVICE_NAME = 'org.openbmc.records.events'
_EVENT_LOG_PATH = '/var/lib/obmc/events'
_EVENT_MANAGER = EventManager()

def clear_event_log():
    '''
    Clear all event logs.
    '''
    logid = _EVENT_MANAGER.remove_all_logs()
    result = {}
    if logid == 1:
        result[completion_code.cc_key] = completion_code.success
    else:
        result[completion_code.cc_key] = completion_code.failure
    return result

def get_event_log(logid):
    '''
    Get specified event log via DBUS and return only fields of interested.
    `log_id` must be a string.
    '''
    event = _EVENT_MANAGER.get_log(logid)
    if event is None:
        raise RuntimeError('fail to get log %s' % logid)
    result = {}
    result['Id'] = logid
    result['Severity'] = event.severity
    result['Created'] = event.time
    result['SensorType'] = event.sensor_type
    result['SensorNumber'] = event.sensor_number
    result['Message'] = event.message
    return result

def get_event_log_all():
    '''
    Get all event logs.
    '''
    result = {}
    result['members'] = []
    for logid in _EVENT_MANAGER.get_log_ids():
        entry = get_event_log(str(logid))
        result['members'].append(entry)
    return result
