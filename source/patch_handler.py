import authentication
import view_helper
import get_handler
import enums
import re
from bottle import HTTPError, auth_basic
from controls.utils import set_failure_dict, completion_code
from view_helper import parameter_parser
from netaddr import IPAddress
from controls.sys_works import ethernet_actions_results
import controls.manage_bmc
import controls.manage_network
import controls.manage_user
from authentication import pre_check_slot_id


def execute_patch_request_actions(requested, action_map, tree=[]):
    """
    Handler for all patch requests to change system parameters based on received information.

    :param requested: A dictionary that contains the set of system parameters to change.
    :param action_map: A mapping of the function to call for each parameter that can be set.
    Each mapping contains a tuple that has a function pointer, parameter parser, and additional
    arguments that should be passed to the function.
    :param tree: The ancestry of the current set of request properties.

    :return A result dictionary to be used to generate the response.
    """
    result = {}
    if requested is not None:
        for param, value in requested.items():
            if ("@" not in param):
                try:
                    if (hasattr(value, "keys")):
                        parents = list(tree)
                        parents.append(param)

                        action_data = execute_patch_request_actions(value, action_map,
                                                                    tree=parents)
                        view_helper.append_response_information(result, action_data)
                    elif (isinstance(value, list)):
                        for i, entry in enumerate(value):
                            parents = list(tree)
                            parents.append(param)
                            parents.append("[{0}]".format(i))

                            action_data = execute_patch_request_actions(entry, action_map,
                                                                        tree=parents)
                            view_helper.append_response_information(result, action_data)
                            i = i + 1
                    else:
                        action = ""
                        if len(tree):
                            action = "/".join(tree) + "/"
                        action = action + param

                        if (action in action_map):
                            call = action_map[action]
                            args = call[2].copy()
                            try:
                                call[1].parse_parameter(value, args)

                            except TypeError as error:
                                view_helper.append_invalid_property_type(result,
                                                                         action.split("/"))
                                continue

                            except Exception as error:
                                view_helper.append_invalid_property_value(result,
                                                                          action.split("/"), str(error))
                                continue
                            action_data = call[0](**args)
                            view_helper.append_response_information(result, action_data)
                        else:
                            view_helper.append_read_only_property(result, action.split("/"))

                except Exception as error:
                    view_helper.append_response_information(
                        result, set_failure_dict(str(error), completion_code.failure))
    return result

def validate_patch_request_and_execute (action_map, name):
    """
    Check the request for to make sure the object only contains valid properties.  If it does, then
    execute the requested actions.
    
    :param action_map: A mapping of the function to call for each parameter that can be set.
    Each mapping contains a tuple that has a function pointer, parameter parser, and additional
    arguments that should be passed to the function.
    :param name: The name of the resource to validate against.
    
    :return A result dictionary to be used to generate the response.
    """
    try:
        requested = view_helper.get_json_request_data ()
        
    except Exception as error:
        view_helper.raise_status_response (400,
            view_helper.create_response_with_status (description = str (error)))
    valid_set = view_helper.get_json_default_resource (name)
    errors = {}
    check_for_invalid_parameters (requested, valid_set, errors)
    if errors:
        view_helper.raise_status_response (400, errors)
    return execute_patch_request_actions (requested, action_map)

def check_for_invalid_parameters (requested, valid_set, errors, path = "#"):
    """
    Check that all the properties contained in the request object are valid for the resource the
    request was submitted against.
    
    :param requested: The request object to validate.
    :param valid_set: The complete set of valid properties.
    :param errors: The dictionary of errors that will be updated with parameters errors"
    """
    
    for param, value in requested.items ():
        if ("@" not in param):
            param_path = "{0}/{1}".format (path, param)
            if (param not in valid_set):
                view_helper.append_unknown_parameter_error (errors, param_path)
            elif (hasattr (value, "keys")):
                check_for_invalid_parameters (value, valid_set[param], errors, path = param_path)
            elif (isinstance (value, list)):
                if (not isinstance (valid_set[param], list)):
                    view_helper.append_parameter_type_error (errors, param_path)
                else:
                    for i, entry in enumerate (value):
                        check_for_invalid_parameters (entry, valid_set[param][0], errors,
                            path = "{0}[{1}]".format (param_path, i))
                
def apply_ip_address (address = None, mask = None, gateway = None, addr_type = None,
    save_args = True, args = dict ()):
    """
    Helper function to aggregate network device parameters and apply the settings.
    
    :param address: The IP address to assign to the network interface.
    :param mask: The subnet mask.
    :param gateway: A default gateway to set for the system.
    :param addr_type: The type of IP address being assigned.
    :param save_args: A flag indicating if the specified parameters should be saved or if the
    device should be configured.  When configuring the device, any unspecified parameters will be
    extracted from the argument aggreation.
    :param args: The aggregation of network parameters that will be updated when not applying the
    specified parameters.
    
    :return Result information for the configuration request.
    """
    
    result = {}
    
    if (save_args):
        if (address is not None):
            args["ip_address"] = address
        if (mask is not None):
            args["netmask"] = mask
        if (gateway is not None):
            args["gateway"] = gateway
        if (addr_type is not None):
            args["addr_type"] = addr_type
    else:
        if ("addr_type" in args):
            if (args["addr_type"] == enums.AddressOrigin.DHCP):
                if (("ip_address" in args) or ("netmask" in args) or ("gateway" in args)):
                    result = set_failure_dict (
                        "No IP address information can be specified when using DHCP.",
                        completion_code.failure)
                else:
                    result = ethernet_actions_results (
                        controls.manage_network.set_dhcp_interfaces ("eth0"))
            else:
                missing = []
                if ("ip_address" not in args):
                    missing.append ("Address")
                if ("netmask" not in args):
                    missing.append ("SubnetMask")
                if ("gateway" not in args):
                    missing.append ("Gateway")
                    
                if missing:
                    for param in missing:
                        view_helper.append_missing_parameter_error (result, param)
                else:
                    del args["addr_type"]
                    result = ethernet_actions_results (
                        controls.manage_network.set_static_interface ("eth0", **args))
        else:
            view_helper.append_missing_parameter_error (result, "AddressOrigin")
        
    return result


def validate_datetime(time):
    """
    Validate that the DateTime value is formatted properly.

    :param time: The configuration to validate.

    :return The validated configuration.
    """
    if (not re.match('(\d{4})[-](\d{2})[-](\d{2})T(\d{2})[:](\d{2})[:](\d{2})Z$', time)):
        raise ValueError("{0} is not a DateTime value.".format(time))
    return time


#########################
# Chassis components
#########################
@auth_basic(authentication.validate_user)
def patch_chassis(slot_id):
    pre_check_slot_id(slot_id)
    actions = {
        "IndicatorLED": (controls.manage_bmc.set_bmc_attention_led,
                         parameter_parser("setting", int, enums.IndicatorLED), {})
    }
    result = validate_patch_request_and_execute(actions, "chassis")
    return get_handler.get_chassis(slot_id, patch=result)

@auth_basic(authentication.validate_user)
def patch_chassis_storage_enclosure(slot_id, se_id):
    raise NotImplementedError()

###################
# BMC components
###################
@auth_basic (authentication.validate_user)
def patch_bmc (slot_id):
    pre_check_slot_id(slot_id)
    actions = {
        "DateTime": (controls.manage_bmc.set_bmc_time,
            parameter_parser("datetime", str, validate_datetime), {})
    }
    
    result = validate_patch_request_and_execute (actions, "bmc")
    return get_handler.get_bmc (slot_id, patch = result)


@auth_basic (authentication.validate_user)
def patch_bmc_ethernet (slot_id, eth):
    pre_check_slot_id(slot_id)
    if (eth == "eth1"):
        raise HTTPError (status = 405)

    requested = view_helper.get_json_request_data ()
    if ("IPv4Addresses" in requested):
        address = requested["IPv4Addresses"]
        if (len (address) > 1):
            raise HTTPError (status = 400, body = "No more than one IP address may be specified.")
    
    ip_args = {}
    actions = {
        "IPv4Addresses/[0]/Address" : (apply_ip_address,
            parameter_parser ("address", str, IPAddress), {"args" : ip_args}),
        "IPv4Addresses/[0]/SubnetMask" : (apply_ip_address,
            parameter_parser ("mask", str, parameter_parser.validate_subnet_mask),
            {"args" : ip_args}),
        "IPv4Addresses/[0]/Gateway" : (apply_ip_address,
            parameter_parser ("gateway", str, IPAddress), {"args" : ip_args}),
        "IPv4Addresses/[0]/AddressOrigin" : (apply_ip_address,
            parameter_parser ("addr_type", str, enums.AddressOrigin), {"args" : ip_args})
    }
    
    result = validate_patch_request_and_execute (actions, "bmc_ethernet")
    if (not result):
        set_data = apply_ip_address (save_args = False, args = ip_args)
        view_helper.append_response_information (result, set_data)
        
    return get_handler.get_rack_manager_ethernet (eth, patch = result)
    
############################
# Account service components
############################
@auth_basic (authentication.validate_user)
def patch_account (account):
    pre_check_slot_id(slot_id)
    view_helper.verify_account_name (account)
    
    actions = {
        "Password" : (controls.manage_user.user_update_password, parameter_parser ("pwd", str),
            {"username" : account}),
        "RoleId" : (controls.manage_user.user_update_role,
            parameter_parser ("role", str, enums.RoleId), {"username" : account})
    }
    
    result = validate_patch_request_and_execute (actions, "account")
    return get_handler.get_account (account, patch = result)
