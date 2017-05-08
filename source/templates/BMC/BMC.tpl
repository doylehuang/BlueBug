<%
    setdefault ("SLOT_ID", "#")
    setdefault ("Package", "vx.xx.xx")
    setdefault ("DateTime", "yyyy-MM-ddTHH:mm:ss+Z")
%>
{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Manager",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}",
  "@odata.type": "#Manager.v1_2_0.Manager",
  "Id": "1",
  "Name": "Manager",
  "ManagerType": "BMC",
  "Description": "BMC",
  "ServiceEntryPointUUID": "92384634-2938-2342-8820-489239905423",
  "UUID": "00000000-0000-0000-0000-000000000000",
  "Model": "AST2520",
  %if defined ("DateTime"):
        "DateTime": "{{DateTime}}",
  %end
  "DateTimeLocalOffset": "+00:00",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "SerialConsole": {
    "ServiceEnabled": true,
    "MaxConcurrentSessions": 1,
    "ConnectTypesSupported": [
      "Telnet",
      "SSH"
    ]
  },
  "CommandShell": {
    "ServiceEnabled": true,
    "MaxConcurrentSessions": 4,
    "ConnectTypesSupported": [
      "SSH"
    ]
  },
  "FirmwareVersion": "{{Package}}",
  "NetworkProtocol": {
    "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/NetworkProtocol"
  },
  "EthernetInterfaces": {
    "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/EthernetInterfaces"
  },
  "SerialInterfaces": {
    "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/SerialInterfaces"
  },
  "LogServices": {
    "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices"
  },
  "Links": {
    "ManagerForChassis": [
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
      }
    ],
    "Oem": {}
  },
  "Actions": {
    "#Manager.Reset": {
      "target": "/redfish/v1/Managers/System/{{SLOT_ID}}/Actions/Manager.Reset",
      "ResetType@Redfish.AllowableValues": [
        "WarmReset"
      ]
    },
    "Oem": {
      "Actions":{
        "#Manager.FirmwareUpdate": {
          "target": "/redfish/v1/Managers/System/{{SLOT_ID}}/Actions/Manager.FirmwareUpdate",
          "Operation@Redfish.AllowableValues": [
            "Prepare",
            "Apply",
            "Abort"
          ]
        },
        "#Manager.FirmwareUpdateState": {
          "target": "/redfish/v1/Managers/System/{{SLOT_ID}}/Actions/Manager.FirmwareUpdateState",
          "Operation@Redfish.AllowableValues": [
            "Query"
          ]
        },
        "#Manager.MasterWriteRead": {
          "target": "/redfish/v1/Managers/System/{{SLOT_ID}}/Actions/Manager.MasterWriteRead"
        },
        "#Manager.MasterPhaseWriteRead": {
          "target": "/redfish/v1/Managers/System/{{SLOT_ID}}/Actions/Manager.MasterPhaseWriteRead"
        }
      }
    }
  },
  "Oem": {
    "BMCHealth": "OK"
  }
}
