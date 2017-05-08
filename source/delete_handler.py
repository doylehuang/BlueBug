import authentication
import view_helper
import post_handler
from bottle import auth_basic
from authentication import pre_check_function_call
from pre_settings import command_name_enum
import controls.manage_user

############################
# Account service components
############################
@auth_basic (authentication.validate_user)
def delete_account (account):
    view_helper.verify_account_name (account)
    pre_check_function_call (command_name_enum.set_rm_config)
    
    result = controls.manage_user.user_delete_by_name (account)
    return post_handler.check_action_result (result)