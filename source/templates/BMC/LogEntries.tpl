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
  "members@odata.count": {{len(members)}},
  "members": [
        % for i, log in enumerate(members):
        {
            <% closetag = ',' if i != len(members)-1 else '' %>

            "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Entries/{{log['Id']}}",
            "@odata.type": "#LogEntry.1.0.2.LogEntry",
            "Id": "{{log['Id']}}",
            "Name": "Log Entry {{log['Id']}}",
            "Severity": "{{log['Severity']}}",
            "Created": "{{log['Created']}}",
            "SensorType": "{{log['SensorType']}}",
            "SensorNumber": "{{log['SensorNumber']}}",
            "Message": "{{log['Message']}}"
        }{{closetag}}
        % end
    ],
      "Links": {
        "OriginOfCondition": {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal"
        },
        "Oem": {}
      },
      "Oem": {}
}

