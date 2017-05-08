<%
    setdefault ("ID", "#")
    setdefault ("PORT", "#")
    setdefault ("STATUS", "#")
    setdefault ("HEALTH", "#")
    setdefault ("NAME", "#")
%>
{
  "@odata.context": "/redfish/v1/$metadata#Port.Port",
  "@odata.id": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Ports/{{PORT}}",
  "@odata.type": "#Port.v1_0_0.Port",
  "Id": "0/{{ID}}/{{PORT}}",
  "Name": "PCIe Port {{ID}}/{{PORT}}",
  "Description": "{{NAME}}",
  "Status": {
    "State": "{{STATUS}}",
    "Health": "{{HEALTH}}"
  },
  "PortId": "{{PORT}}",
  "PortProtocol": "PCIe",
  "PortType": "DownstreamPort",
  "CurrentSpeedGbps": 8,
  "Width": 2,
  "MaxSpeedGbps": 8,
  "Actions": {
    "#Port.Reset": {
      "target": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Ports/{{PORT}}/Actions/Port.Reset",
      "ResetType@Redfish.AllowableValues": [
        "ForceOff",
        "ForceRestart",
        "ForceOn"
      ]
    }
  },
  "Links": {
    "AssociatedEndpoints": [
      {
        "@odata.id": "/redfish/v1/Fabrics/PCIe/Endpoints/1"
      }
    ]
  }
}

