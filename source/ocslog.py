import os
import ctypes

log_lib = '/usr/lib/libocslog.so'
log_binary = None

if os.path.isfile (log_lib) and log_binary is None:
    log_binary = ctypes.cdll.LoadLibrary (log_lib)
    
def initialize_log ():
    global log_binary
    
    if log_binary is None:
        log_binary = ctypes.cdll.LoadLibrary (log_lib)
            
    log_binary.log_init ()

def log_info (*args):
    print "".join (map (str, args))
    
def log_warn (*args):
    print "".join (map (str, args))
        
def log_error (*args):
    print "".join (map (str, args))