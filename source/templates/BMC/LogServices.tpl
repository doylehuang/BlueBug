<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#LogServiceCollection",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices",
  "@odata.type": "#LogServiceCollection.LogServiceCollection",
  "Name": "Log Service Collection",
  "Description": "Collection of Log Services for this Manager",
  "Members@odata.count": 1,
  "Members": [
    {
      "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1"
    }
  ]
}