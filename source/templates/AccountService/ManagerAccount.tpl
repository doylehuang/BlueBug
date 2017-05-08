<%
    if defined ("TemplateDefault"):
        setdefault ("Account", "")
        setdefault ("groupname", "")
    end
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#ManagerAccount",
  "@odata.id": "/redfish/v1/AccountService/Accounts/{{Account}}",
  "@odata.type": "#ManagerAccount.v1_0_2.ManagerAccount",
  "Id": "{{Account}}",
   "Name": "User Account",
   "Enabled": true,
   "UserName": "{{Account}}",
   %if defined ("TemplateDefault"):
       "Password": "",
   %end
   %if defined ("groupname"):
       "RoleId": "{{groupname}}",
       "Links": {
           "Role": {
               "@odata.id": "/redfish/v1/AccountService/Roles/{{groupname}}"
           }
       }
   %end
}