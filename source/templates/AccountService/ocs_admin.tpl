{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Role",
  "@odata.id": "/redfish/v1/AccountService/Roles/Admin",
  "@odata.type": "#Role.v1_0_2.Role",
  "Id": "Admin",
  "Name": "User Role",
  "Description": "Admin User Role",
  "IsPredefined": true,
  "AssignedPrivileges": [
    "Login",
    "ConfigureManager",
    "ConfigureUsers",
    "ConfigureSelf",
    "ConfigureComponents"
  ],
  "OEMPrivileges": [
    "OemClearLog",
    "OemPowerControl"
  ]
}