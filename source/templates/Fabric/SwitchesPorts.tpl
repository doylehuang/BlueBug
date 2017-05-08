<%
    setdefault ("ID", "#")
%>
{
  "@odata.context": "/redfish/v1/$metadata#PortCollection.PortCollection",
  "@odata.id": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Ports",
  "@odata.type": "#PortCollection.PortCollection",
  "Name": "PCIe Port Collection",
  "Members@odata.count": 2,
  "Members": [
    {"@odata.id": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Ports/1"},
    {"@odata.id": "/redfish/v1/Fabrics/PCIe/Switches/{{ID}}/Ports/2"}
  ]
}
