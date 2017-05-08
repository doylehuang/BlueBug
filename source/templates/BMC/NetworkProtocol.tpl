<%
    setdefault ("SLOT_ID", "#")
    setdefault ("Hostname", "j2010")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#ManagerNetworkProtocol",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/NetworkProtocol",
  "@odata.type": "#ManagerNetworkProtocol.v1_0_2.ManagerNetworkProtocol",
  "Id": "NetworkProtocol",
  "Name": "Manager Network Protocol",
  "Description": "Manager Network Service Status",
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  %if defined ("Hostname"):
        "HostName": "{{Hostname}}",
  %end
  "FQDN": "none ",
  "HTTP": {
    "ProtocolEnabled": true,
    "Port": 80
  },
  "HTTPS": {
    "ProtocolEnabled": true,
    "Port": 443
  },
  "SSH": {
    "ProtocolEnabled": true,
    "Port": 22
  },
  "Oem": {}
}