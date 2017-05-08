<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#SerialInterfaceCollection",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/SerialInterfaces",
  "@odata.type": "#SerialInterfaceCollection.SerialInterfaceCollection",
  "Name": "Serial Interface Collection",
  "Description": "Collection of Serial Interfaces for this System",
  "Members@odata.count": 1,
  "Members": [
    {
      "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/SerialInterfaces/1"
    }
  ],
  "Oem": {}
}