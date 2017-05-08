#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import fcntl
import struct
import array

import fcntl
import os
import re
import socket
import struct
import ctypes
import array
import math
import subprocess 
import sys
from subprocess import Popen, PIPE
from utils import *

# From linux sockios.h
SIOCGIFHWADDR  = 0x8927          # Get hardware address    
SIOCGIFADDR    = 0x8915          # get PA address 
         
SIOCGIFNETMASK = 0x891b          # get network PA mask     
SIOCGIFNAME    = 0x8910          # get interface name          
SIOCSIFLINK    = 0x8911          # set interface channel       
SIOCGIFCONF    = 0x8912          # get interface list          
SIOCGIFFLAGS   = 0x8913          # get flags               
SIOCSIFFLAGS   = 0x8914          # set flags               
SIOCGIFINDEX   = 0x8933          # name -> if_index mapping
SIOCGIFCOUNT   = 0x8938          # get number of devices
SIOCGIFBRDADDR = 0x8919    

############################################################################################################
# Network actions Functions 
###########################################################################################################
def display_interface_by_name(if_name, rest = True):
    """ Display network interface information given device name."""    
    try:
        result={}
        if findInterfaceName (if_name):
            
            result["Id"]="%s" %if_name
            
            if rest:
                result["ODataId"]="/redfish/v1/Systems/1/ethernetinterfaces/%s" % if_name        
                result["Name"]="Simple Ethernet Interface"
                result["Description"]="System NIC %s" % if_name
            
            if interface_status(if_name):
                enabled="Up"
            else:
                enabled="Down"
                    
            result["Status_State"]= enabled
            result["Status_Health"]="Ok"
            
            result["MACAddress"] = get_macsocket(if_name)
            
            Address = get_ip_address(if_name)
            
            result["IPv4Addresses"]={"Address": Address,"SubnetMask": get_subnetmask_ifconfig(if_name),"AddressOrigin":"","Gateway":get_default_gateway()}   
            
            if get_default_interface() == if_name:
                preferred="True"
            else:
                preferred="False"
            
            ifIPV6 = get_IPV6(if_name).strip()
            
            if ifIPV6:
                ipv6= ifIPV6.split('/')[0]
                ipv6prefix=ifIPV6.split('/')[1]
            else:
                ipv6= ""
                ipv6prefix=""
                
            result["IPv6Addresses"]={"Address":ipv6,"PrefixLength":ipv6prefix,"AddressOrigin":"","AddressState":preferred}
    except Exception, e:
        #print ("Failed Exception :",e)
        return set_failure_dict(("Exception:", e),completion_code.failure) 
          
    result[completion_code.cc_key] = completion_code.success  
    return result    

def display_interfaces():
    """ Display all network interface information."""    
    result={}
    output={}
        
    ifs = list_Interfaces()
    for i in ifs:
        interfaceLink= "/redfish/v1/Chassis/RackManager/EthernetInterface/%s" % i            
        output.update({i:interfaceLink})
    
    result["Id"]=""
    result["ODataId"]=""
    result["Name"]=""
    result["eth_list"]=output
    result["eth_count"] =len(output) 

    result[completion_code.cc_key] = completion_code.success
    return result  

def display_cli_interfaces():
    try:
        """ Display all network interface information."""    
        result={}
        result["Interfaces_list"] = {}
        
        count = 0;
        ifs = list_Interfaces()
        for i in ifs:
            count = count+1
            result["Interfaces_list"].update({str(count):i})
        
        result["Interfaces_count"] =count
        
    except Exception, e:
        return set_failure_dict(("Exception:",e),completion_code.failure)
    
    result[completion_code.cc_key] = completion_code.success
    return result   
                                      

def get_command_output(command):
    try:  
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True);
        output, errorMsg = process.communicate() 
    
        completion_Status = process.wait();
        
        if errorMsg:
            return {'status_code':completion_Status, 'stdout':output, 'failed': errorMsg}
        
        return output       
    
    except Exception,e:      
        return {'status_code':completion_Status, 'stdout':output, 'failed': e} 
    
def call_network_command(command):
    try:  
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True);
        output, errorMsg = process.communicate() 
    
        completion_Status = process.wait();
        
        return {'status_code':completion_Status, 'stdout':output, 'stderr': errorMsg}       
    
    except Exception,e:      
        return {'status_code':completion_Status, 'stdout':output, 'failed': e}        

############################################################################################################
# Network interface support Functions 
###########################################################################################################
def list_allroute():
    """ List static route"""    
        
    staticRouteListCommand = "route -n "
    
    return get_command_output(staticRouteListCommand) 

def add_defaultgateway(gateway):
    """ Add a static route with route"""
            
    addRouteCommand = "route add default gw {0} ".format(gateway)
    
    return get_command_output(addRouteCommand) 

def delete_staticroute(net, netmask, gateway):
    """ Add a static route with route"""    
        
    addRouteCommand = "route add -net {0} netmask {1} gw {2} ".format(net, netmask, gateway)
    
    return get_command_output(addRouteCommand)         
    

def set_static_interface(if_name, ip_address, netmask, gateway):
    """ To assign static IP address to an interface given device name."""    
   
    setToStaticCommand = "ifconfig {0} {1} netmask {2} ".format(if_name,ip_address, netmask)

    output = call_network_command(setToStaticCommand)
    
    if (output['status_code'] == 0):
        addRouteCommand = "route add default gw {0} ".format(gateway)
        gwoutput = call_network_command(addRouteCommand)        
        return gwoutput
    else:
        return output       
 
    
def set_dhcp_interfaces(if_name):
    """ To assign dynamic IP address to an interface given device name."""    
        
    set_dhcp_command = "udhcpc {0} ".format(if_name)    
    return call_network_command(set_dhcp_command)       

def enable_network_interface(if_name):
    """Enable network interface by device name."""

    enable_command = "ifup '{0}'".format(if_name)
    return call_network_command(enable_command)

def disable_network_interface(if_name):
    """Disable network interface by device name."""
    
    disable_command = "ifdown  '{0}'".format(if_name)
    return call_network_command(disable_command)
    
def get_macsocket(if_name):
    try:
        ''' Obtain the device's mac address. '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        ifreq = struct.pack('16sH14s', if_name,1, b'\x00'*14)
        
        res = fcntl.ioctl(s.fileno(), SIOCGIFHWADDR, ifreq)
        address = struct.unpack('16sH14s', res)[2]
        mac = struct.unpack('6B8x', address)
        
        result =  ":".join(['%02X' % i for i in mac])
        
        return str(result)
               
    except Exception, e:
        #Log_err(Exception ,e)
        return None 
    
def get_network_mac_address(if_name):
    result = {}
    
    try:
        result["MacAddress"] = get_macsocket(if_name)
            
    except Exception, e:  
        return set_failure_dict("get_mac_address() Exception {0}".format(str(e)),completion_code.failure) 
    
    result[completion_code.cc_key] = completion_code.success
    
    return result            
            
def get_network_ip_address(if_name):
    result = {}
    
    try:
        result["IPAddress"] = get_ip_address(if_name)
            
    except Exception, e:  
        return set_failure_dict("get_network_ip_address() Exception {0}".format(str(e)),completion_code.failure) 
    
    result[completion_code.cc_key] = completion_code.success
    
    return result

def get_network_subnetmask(if_name):
    result = {}
    
    try:
        result["SubnetMask"] = get_subnetmask_ifconfig(if_name)
            
    except Exception, e:  
        return set_failure_dict("get_network_subnetmask() Exception {0}".format(str(e)),completion_code.failure) 
    
    result[completion_code.cc_key] = completion_code.success
    
    return result

def get_network_gateway():
    result = {}
    
    try:
        result["Gateway"] = get_default_gateway()
            
    except Exception, e:  
        return set_failure_dict("get_network_gateway() Exception {0}".format(str(e)),completion_code.failure) 
    
    result[completion_code.cc_key] = completion_code.success
    
    return result

def get_network_status(if_name):
    result = {}
    
    try:
        result["InterfaceStatus"] = "Up" if interface_status(if_name) else "Down"
            
    except Exception, e:  
        return set_failure_dict("get_network_status() Exception {0}".format(str(e)),completion_code.failure) 
    
    result[completion_code.cc_key] = completion_code.success
    
    return result

def get_subnetmask_ifconfig(if_name):
    interfaceCommand = "/sbin/ifconfig %s |  awk '/Mask/{print $4}' "%if_name
    
    output= get_command_output(interfaceCommand)
    
    if output:
        return output.strip().split(':')[1]
    
    return None

def get_mac_ifconfig(if_name):
    interfaceCommand = "/sbin/ifconfig %s |  awk '/HWaddr/{print $5}' "%if_name
    
    return get_command_output(interfaceCommand)

def get_IPV6(if_name):
    if_command = "/sbin/ifconfig %s |  awk '/inet6/{print $3}' " %if_name
    
    output= get_command_output(if_command)   
    return "%s" %output  

def get_default_gateway():
    """ Returns the default gateway """
    octet_list = []
    gw_from_route = None
    f = open ('/proc/net/route', 'r')
    for line in f:
        words = line.split()
        dest = words[1]
        try:
            if (int (dest) == 0):
                gw_from_route = words[2]
                break
        except ValueError:
            pass
    if not gw_from_route:
        return None 
    
    for i in range(8, 1, -2):
        octet = gw_from_route[i-2:i]
        octet = int(octet, 16)
        octet_list.append(str(octet)) 
    
    gw_ip = ".".join(octet_list)
    
    return gw_ip

def get_physical_interfaces():
    ''' Iterate over all the interfaces in the system. 
        Return physical interfaces (not 'lo', etc).'''
    
    SYSFS_NET_PATH = b"/sys/class/net"
    
    net_files = os.listdir(SYSFS_NET_PATH)
    interfaces = set()
    virtual = set()
    for d in net_files:
        path = os.path.join(SYSFS_NET_PATH, d)
        if not os.path.isdir(path):
            continue
        if not os.path.exists(os.path.join(path, b"device")):
            virtual.add(d)
        interfaces.add(d)

    results = interfaces - virtual 
    return results

def get_ip_address(if_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        res = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                SIOCGIFADDR,  
                struct.pack('256s', if_name[:15]))[20:24])
    except IOError:
        return None
    
    return res

def get_netmask(if_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    ifreq = struct.pack('16sH14s',if_name, socket.AF_INET, b'\x00'*14)
    try:
        res = fcntl.ioctl(s.fileno(), SIOCGIFNETMASK, ifreq)
    except IOError:
        return 0
    netmask = socket.ntohl(struct.unpack('16sH2xI8x', res)[2])

    return 32 - int(round( math.log(ctypes.c_uint32(~netmask).value + 1, 2), 1))

def get_all_interfaces():
    ''' Iterate over all the interfaces in the system. 
        Return all interfaces including virtual. ( 'lo', etc).'''
    max_possible = 128  
    
    bytes = max_possible * 32
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    names = array.array('B', '\0' * bytes)
    
    outbytes = struct.unpack('iL', 
        fcntl.ioctl( s.fileno(), SIOCGIFCONF,  struct.pack('iL', bytes, names.buffer_info()[0]))
        )[0]
    namestr = names.tostring()
    lst = []
    
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split('\0', 1)[0]
        ip   = namestr[i+20:i+24]
        lst.append((name, ip))
        
    return lst

def list_Interfaces():
    ''' Return a list of the names of the interfaces. '''
    return [br for br in get_physical_interfaces()]

def findInterfaceName(if_name):
    for br in get_physical_interfaces():
        if if_name == br:
            return br
    return None

def get_default_interface():
    """ Returns the default interface """
    default_if=''
    
    f = open ('/proc/net/route', 'r')
    for line in f:
        words = line.split()
        dest = words[1]
        try:
            if (int (dest) == 0):
                default_if = words[0]
                break
        except ValueError:
            pass
    return default_if

def interface_status(if_name):
    ''' Return True if the interface is up, False otherwise. '''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ifreq = struct.pack('16sh', if_name, 0)
    flags = struct.unpack('16sh', fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, ifreq))[1]

    # Set new flags
    if flags & 0x1:
        return True
    else:
        return False

#############################################
    #Rack Manager Firmware Version
#############################################
def get_service_version():
    try:
        version_cmd = "/etc/rmversions.sh"
        
        output = call_network_command(version_cmd)
        
        if (output['status_code'] == 0):
            return output
        else:
            #log_inf("failed to run version cmd",output)
            return set_failure_dict(output['stderr'],completion_code.failure)       
    except Exception, e:
        #lg_exception("Exception to call version command",e)
        return set_failure_dict(("Exception:",e),completion_code.failure) 
    