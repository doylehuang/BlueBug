#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import subprocess
from utils import *


def get_ocsfwversion():
    return generate_collection(doCommand())


def doCommand():
    """
    Read bmcversion.sh output and parse the output 
    """

    command = '/usr/lib/redfish/controls/bmcversion.sh'

    output = {}

    completion_Status = ""
    errorMsg = ""
    try:

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True);
        output, errorMsg = process.communicate()

        completion_Status = process.wait();

        if errorMsg:
            return {'status_code': -1, 'output: ': output, 'failed: ': errorMsg}

        else:
            return {'status_code': completion_Status, 'stdout': output, 'stderr': errorMsg}

    except Exception, e:
        return {'status_code': -2, 'stdout': output, 'failed: ': e}


def generate_collection(output):
    try:
        fwRsp = {}
        if (output['status_code'] == 0):

            sdata = output['stdout'].split('\n')

            for value in sdata:
                if "Package version" in value:
                    fwRsp["Package"] = value.split(":")[-1].strip()

            fwRsp[completion_code.cc_key] = completion_code.success

            return fwRsp
        else:
            fwFailedRsp = {}
            errorData = output['stderr'].split('\n')
            fwFailedRsp[completion_code.cc_key] = completion_code.failure

            for data in errorData:
                if "Error" in data:
                    fwFailedRsp[completion_code.desc] = data.split(":")[-1]

            return fwFailedRsp

    except Exception, e:
        return set_failure_dict(("ServerLog: Exception: ", e), completion_code.failure)
