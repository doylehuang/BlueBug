<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#LogEntryCollection",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Entries",
  "@odata.type": "#LogEntryCollection.LogEntryCollection",
  "Name": "Log Service Collection",
  "Description": "Collection of Logs for this System",
  "members@odata.count": 1,
  "members": [
        {
          "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Entries/{{Id}}",
          "@odata.type": "#LogEntry.v1_0_0.LogEntry",
          "Id": "{{Id}}",
          "Name": "Log Entry {{Id}}",
          "EntryType": "SEL",
          "Severity": "{{Severity}}",
          "Created": "{{Created}}",
          "SensorType": "{{SensorType}}",
          "SensorNumber": "{{SensorNumber}}",
          "Message": "{{Message}}",
          "Oem": {}
        }
    ]
}



