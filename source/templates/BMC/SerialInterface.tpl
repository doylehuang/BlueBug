<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#SerialInterface",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/SerialInterfaces/1",
  "@odata.type": "#SerialInterface.v1_0_2.SerialInterface",
  "Id": "1",
  "Name": "Managed Serial Interface 1",
  "Description": "Management for Serial Interface",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "InterfaceEnabled": true,
  "SignalType": "UART",
  "BitRate": "115200",
  "Parity": "None",
  "DataBits": "8",
  "StopBits": "1",
  "FlowControl": "None",
  "ConnectorType": "TTL UART Debug Header",
  "PinOut": "5v, 3.3vRX, 3.3vTX, Ground"
}