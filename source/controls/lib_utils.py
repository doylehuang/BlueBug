import os
import ctypes

hdc_lib = '/usr/lib/libocshdc.so'
hsc_lib = '/usr/lib/libocshsc.so'
gpio_lib = '/usr/lib/libocsgpio.so'
fwupdate_lib = '/usr/lib/libocsfwupgrade.so'
parser_lib = '/usr/lib/libocstelemetry_parse.so'
auth_lib = '/usr/lib/libauth.so'
precheck_lib = '/usr/lib/libocsprecheck.so'
pru_lib = '/usr/lib/libocspru.so'
blademap_lib = "/usr/lib/libocsblademap.so"

def load_library(path, name):
    if os.path.isfile(path) :
        binary = ctypes.cdll.LoadLibrary(path)
    else:
        raise RuntimeError("Failed to load {0} library".format (name))
    
    if (binary is None):
        raise RuntimeError("Failed to load {0} library".format (name))
    
    return binary
    


def get_gpio_library():
    return load_library(gpio_lib, "ocsgpio")

def get_hsc_library():
    return load_library(hsc_lib, "ocshsc")

def get_hdc_library():
    return load_library(hdc_lib, "oschdc")

def get_fwupdate_library():
    return load_library(fwupdate_lib, "ocsfwupgrade")

def get_telemetry_library():
    return load_library(parser_lib, "ocstelemetry parser")

def get_authentication_library():
    return load_library(auth_lib, "ocsauth")

def get_precheck_library():
    return load_library(precheck_lib, "ocsprecheck")

def get_pru_library():
    return load_library(pru_lib, "ocspru")

def get_blade_map_library():
    return  load_library(blademap_lib, "ocsblademap")
