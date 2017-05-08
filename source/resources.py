import os
import get_handler
import patch_handler
import post_handler
import delete_handler


TEMPLATE_ROOT = os.path.realpath ("/usr/lib/redfish/templates") + "/"

class redfish_resource:
    """
    Defines a single resource accessible via the REST interface.
    """
    
    def __init__ (self, common = None,
        get = None, post = None, patch = None, delete = None):
        """
        Initialize a resource to be provided by the REST interface.  The resource is initialized
        with the URI and template path for each configuration and the methods that are supported
        by the resource.
        
        :param common: A tuple of URI and template path for a resource that is common to all
        configurations.  If not specified, the specific configuration settings will be applied.

        :param get: The handler for GET requests for the resource.  If not specified, GET requests
        on the resource will not be supported.
        :param post: The handler for POST requests for the resource.  If not specified, POST
        requests on the resource will not be supported.
        :param patch: The handler for PATCH requests for the resource.  If not specified, PATCH
        requests on the resource will not be supported.
        :param delete: The handler for DELETE requests for the resource.  If not specified, DELETE
        requests on the resource will not be supported.
        """
        
        self.common = common
        self.get = get
        self.post = post
        self.patch = patch
        self.delete = delete
        
    def register_resource (self, app):
        """
        Register the resource with the REST handler.  If the resource is not valid for the given
        configuration, this call does nothing.
        
        :param app: The web server instance to register the resource with.
        """
        
        if (self.common):
            self.rest = self.common[0]
            self.template = TEMPLATE_ROOT + self.common[1]
        else:
            self.rest = None
            
        if (not self.rest):
            return
        (self.path, self.file) = os.path.split (self.template)
        
        if (self.get):
            app.route (self.rest, "GET", self.get)
        if (self.post):
            app.route (self.rest, "POST", self.post)
        if (self.patch):
            app.route (self.rest, "PATCH", self.patch)
        if (self.delete):
            app.route (self.rest, "DELETE", self.delete)

def get_max_num_systems ():
    """
    Get the maximum number of possible systems for the current configuration.
    
    :return The maximum number of systems.
    """
    
    return 4

REGEX_1_4 = "[1-4]"

def id_filter (config):
    """
    A bottle router filter that matches valid identifier numbers.  Based on the config, it will
    match against 4 valid IDs.
    
    :param config: The number of IDs to filter against.  This defaults to 4 if not sepeified or if
    the range isn't supported.
    """
    

    regex = REGEX_1_4
    
    def to_python (match):
        return match
    
    def to_url (system):
        return system
    
    return regex, to_python, to_url

def system_id_filter (config):
    """
    A Bottle router filter that matches a system identifier against valid values.
    """
    
    return id_filter (get_max_num_systems ())

def add_bottle_filters (app):
    """
    Add custom URL filters to the Bottle instance.
    
    :param app: The web server instance to add the filters to.
    """
    
    app.router.add_filter ("id", id_filter)
    app.router.add_filter ("sysid", system_id_filter)

##
# The list of accesible resources from the REST interface.
##
REDFISH_RESOURCES = {
    ###################
    # Top-Level Redfish
    ###################
    "version" : redfish_resource (
        common = (
            "/redfish",
            "Redfish.tpl"),
        get = get_handler.get_redfish_version),
    "service_root" : redfish_resource (
        common = (
            "/redfish/v1",
            "ServiceRoot.tpl"),
        get = get_handler.get_service_root),
    "chassis_root" : redfish_resource (
        common = (
            "/redfish/v1/Chassis",
            "Chassis.tpl"),
        get = get_handler.get_chassis_root),
    "managers_root" : redfish_resource (
        common = (
            "/redfish/v1/Managers",
            "Managers.tpl"),
        get = get_handler.get_managers_root),
    "fabrics_root" : redfish_resource (
        common = (
            "/redfish/v1/Fabrics",
            "Fabrics.tpl"),
        get = get_handler.get_fabrics_root),
   
    #########################
    # Chassis components
    #########################      
    "chassis" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>",
        "Chassis/Chassis.tpl"),
        get = get_handler.get_chassis,
        patch = patch_handler.patch_chassis),
   "chassis_thermal" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/Thermal",
        "Chassis/Thermal.tpl"),
        get = get_handler.get_chassis_thermal),
    "bmc_health" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/BMCHealth",
        "Chassis/BmcHealth.tpl"),
        get = get_handler.get_bmc_health),
    "chassis_thermal_redundancy" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/Thermal<sensor_id>/Redundancy/0",
        "Chassis/ThermalRedundancy.tpl"),
        get = get_handler.get_chassis_thermal_redundancy),
    "chassis_power" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/Power",
        "Chassis/Power.tpl"),
        get = get_handler.get_chassis_power),
    "chassis_power_redundancy" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/Power<psu_id>/Redundancy/0",
        "Chassis/PowerRedundancy.tpl"),
        get = get_handler.get_chassis_power_redundancy),
    "chassis_se_master_write_read" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Actions/Chassis.MasterWriteRead",
        "Chassis/SeI2cData.tpl"),
        post = post_handler.post_chassis_se_master_write_read),
    "chassis_storage_enclosure_storage" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Storage",
        "Chassis/SEStorage.tpl"),
        get = get_handler.get_chassis_storage_enclosure_storage),
    "chassis_storage_enclosure_drive": redfish_resource(
        common=(
            "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Drives/Drive<disk_id>",
            "Chassis/SEDrive.tpl"),
        get=get_handler.get_chassis_storage_enclosure_drive),
    "chassis_storage_enclosure_drive_power_on": redfish_resource(
        common=(
            "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Drives/Drive<disk_id>/Actions/On",
            ""),
        post = post_handler.post_chassis_storage_enclosure_disk_power_on),
    "chassis_storage_enclosure_drive_power_off": redfish_resource(
        common=(
            "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Drives/Drive<disk_id>/Actions/Off",
            ""),
        post = post_handler.post_chassis_storage_enclosure_disk_power_off),
    "chassis_storage_enclosure_power" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Power",
        "Chassis/SEPower.tpl"),
        get = get_handler.get_chassis_storage_enclosure_power),
    "chassis_storage_enclosure_thermal" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/StorageEnclosure<se_id>/Thermal",
        "Chassis/SEThermal.tpl"),
        get = get_handler.get_chassis_storage_enclosure_thermal),
    "chassis_on" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/Actions/On",
        "Chassis/ChassisCtrl.tpl"),
        post = post_handler.post_chassis_action_power_on),
    "chassis_off" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/Actions/Off",
        "Chassis/ChassisCtrl.tpl"),
        post = post_handler.post_chassis_action_power_off),
    "chassis_pcie_devices" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/PCIeDevices/<pcie_id>",
        "Chassis/PCIeDevices.tpl"),
        get = get_handler.get_chassis_pcie_devices),
    "chassis_pcie_devices_functions" : redfish_resource (
        common = (
        "/redfish/v1/Chassis/System/<slot_id>/PCIeDevices/<pcie_id>/Functions/<func>",
        "Chassis/PCIeDevicesFunctions.tpl"),
        get = get_handler.get_chassis_pcie_devices_functions),

    #########################
    # BMC components
    #########################   
    "bmc" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>",
        "BMC/BMC.tpl"),
        get = get_handler.get_bmc,
        patch = patch_handler.patch_bmc),
    "bmc_networkprotocol" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/NetworkProtocol",
        "BMC/NetworkProtocol.tpl"),
        get = get_handler.get_bmc_networkprotocol),
    "bmc_ethernets" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/EthernetInterfaces",
        "BMC/EthernetInterfaces.tpl"),
        get = get_handler.get_bmc_ethernets),
    "bmc_ethernet" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/EthernetInterface/<eth:re:eth[0|1]>",
        "BMC/EthernetInterface.tpl"),
        get = get_handler.get_bmc_ethernet,
        patch = patch_handler.patch_bmc_ethernet),
    "bmc_log_service" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/LogServices",
        "BMC/LogServices.tpl"),
        get = get_handler.get_bmc_log_services),
    "bmc_log" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/LogServices/Log1",
        "BMC/Log.tpl"),
        get = get_handler.get_bmc_log),
    "bmc_clear_log" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/LogServices/Log1/Actions/LogService.Reset",
        "GeneralError.tpl"),
        post = post_handler.post_bmc_clear_log),
        
    "bmc_log_entries" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/LogServices/Log1/Entries",
        "BMC/LogEntries.tpl"),
        get = get_handler.get_bmc_log_entries),
    "bmc_log_entry" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/LogServices/Log1/Entries/<entry>",
        "BMC/LogEntry.tpl"),
        get = get_handler.get_bmc_log_entry),    
    "bmc_serialinterfaces" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/SerialInterfaces",
        "BMC/SerialInterfaces.tpl"),
        get = get_handler.get_bmc_serialinterfaces),
    "bmc_serialinterface" : redfish_resource (
        common = (
        "/redfish/v1/Managers/System/<slot_id>/SerialInterface/1",
        "BMC/SerialInterface.tpl"),
        get = get_handler.get_bmc_serialinterface),
    "bmc_fw_update" : redfish_resource (
        common = (
            "/redfish/v1/Managers/System/<slot_id>/Actions/Manager.FirmwareUpdate",
            ""),
        post = post_handler.post_bmc_fw_update),
    "bmc_fw_update_state" : redfish_resource (
        common = (
            "/redfish/v1/Managers/System/<slot_id>/Actions/Manager.FirmwareUpdateState",
            "BMC/FWUpdateState.tpl"),
        post = post_handler.post_bmc_fw_update_state),
    "bmc_warm_reset" : redfish_resource (
        common = (
            "/redfish/v1/Managers/System/<slot_id>/Actions/Manager.Reset",
            ""),
        post = post_handler.post_bmc_warm_reset),
    "bmc_master_write_read": redfish_resource(
        common=(
            "/redfish/v1/Managers/System/<slot_id>/Actions/Manager.MasterWriteRead",
            "BMC/BMCI2cData.tpl"),
        post=post_handler.post_bmc_master_write_read),
    "bmc_master_phase_write_read": redfish_resource(
        common=(
            "/redfish/v1/Managers/System/<slot_id>/Actions/Manager.MasterPhaseWriteRead",
            "BMC/BMCI2cData.tpl"),
        post=post_handler.post_bmc_master_phase_write_read),

    #########################
    # Fabrics components
    #########################
    "fabrics_pcie" : redfish_resource (
        common = (
            "/redfish/v1/Fabrics/PCIe",
            "Fabric/PCIe.tpl"),
        get = get_handler.get_fabrics_pcie),
    "pcie_switches" : redfish_resource (
        common = (
            "/redfish/v1/Fabrics/PCIe/Switches",
            "Fabric/Switches.tpl"),
        get = get_handler.get_pcie_switches),
    "switches_devices" : redfish_resource (
        common = (
            "/redfish/v1/Fabrics/PCIe/Switches/<switches_id>",
            "Fabric/SwitchesDevices.tpl"),
        get = get_handler.get_switches_devices),
    "switches_ports" : redfish_resource (
        common = (
            "/redfish/v1/Fabrics/PCIe/Switches/<switches_id>/Ports",
            "Fabric/SwitchesPorts.tpl"),
        get = get_handler.get_switches_ports),
    "switches_ports_devices" : redfish_resource (
        common = (
            "/redfish/v1/Fabrics/PCIe/Switches/<switches_id>/Ports/<ports_id>",
            "Fabric/SwitchesPortsDevices.tpl"),
        get = get_handler.get_switches_ports_devices),
    ############################
    # Account service components
    ############################
#    "account_service" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService",
#            "AccountService/AccountService.tpl"),
#        get = get_handler.get_account_service),
#    "accounts" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService/ManagerAccounts",
#            "AccountService/ManagerAccounts.tpl"),
#        get = get_handler.get_accounts,
#        post = post_handler.post_accounts),
#    "account" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService/ManagerAccount/<account>",
#            "AccountService/ManagerAccount.tpl"),
#        get = get_handler.get_account,
#        patch = patch_handler.patch_account,
#        delete = delete_handler.delete_account),
#    "roles" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService/Roles",
#            "AccountService/Roles.tpl"),
#        get = get_handler.get_roles),
#    "admin" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService/Role/admin",
#            "AccountService/ocs_admin.tpl"),
#        get = get_handler.get_ocs_admin),
#    "operator" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService/Role/operator",
#            "AccountService/ocs_operator.tpl"),
#        get = get_handler.get_ocs_operator),
#    "user" : redfish_resource (
#        common = (
#            "/redfish/v1/AccountService/Role/user",
#            "AccountService/ocs_user.tpl"),
#        get = get_handler.get_ocs_user),
    

}
