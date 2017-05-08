<%
    setdefault ("ID", "#")
    setdefault ("SLOT_ID", "#")
    setdefault ("STATUS", "#")
    setdefault ("HEALTH", "#")
%>
{
  "@odata.context": "/redfish/v1/$metadata#Switch.Switch",
  "@odata.id": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}",
  "@odata.type": "#Switch.v1_0_0.Switch",
  "Id": "PCIeSwitch{{ID}}",
  "Name": "PCIe Switch {{ID}}",
  "SwitchType ": "PCIe",
  "Manufacturer": "Broadcom",
  "Model": "PCIe PLX Switch",
  "SKU": "",
  "SerialNumber": "{{info['serialnumber']}}",
  "UDID": "{{info['udid']}}",
  "PartNumber": "",
  "Status": {
    "State": "{{STATUS}}",
    "Health": "{{HEALTH}}"
  },
  "Ports": {
    "@odata.id": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Ports"
  },
  "Links": {
    "Chassis": {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
    },
    "ManagedBy": [
      {
        "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}"
      }
    ]
  },
  "Actions": {
    "#Switch.Reset": {
      "target": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Actions/Switch.Reset",
      "ResetType@Redfish.AllowableValues": [
        "On",
        "ForceOff",
        "GracefulShutdown",
        "ForceRestart",
        "Nmi",
        "GracefulRestart",
        "ForceOn",
        "PushPowerButton"
      ]
    }
  }
}

