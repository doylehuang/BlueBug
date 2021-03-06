<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#AccountService",
  "@odata.id": "/redfish/v1/AccountService",
  "@odata.type": "#AccountService.v1_0_2.AccountService",
  "Id": "AccountService",
  "Name": "Account Service",
  "Description": "Account Service",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "ServiceEnabled": true,
  "AuthFailureLoggingThreshold": 3,
  "MinPasswordLength": 8,
  "AccountLockoutThreshold": 5,
  "AccountLockoutDuration": 30,
  "AccountLockoutCounterResetAfter": 30,
  "Accounts": {
    "@odata.id": "/redfish/v1/AccountService/Accounts"
  },
  "Roles": {
    "@odata.id": "/redfish/v1/AccountService/Roles"
  }
}