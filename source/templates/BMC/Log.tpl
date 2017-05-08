<%
    setdefault ("SLOT_ID", "#")
%>


{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#LogService",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1",
  "@odata.type": "#LogService.v1_0_2.LogService",
  "Id": "Log1",
  "Name": "System Log Service",
  "MaxNumberOfRecords": 1000,
  "OverWritePolicy": "WrapsWhenFull",
  "DateTime": "{{DateTime}}",
  "DateTimeLocalOffset": "+00:00",
  "ServiceEnabled": true,
  "Status": {
    "State": "Enabled",
    "Health": "OK"
  },
  "Oem": {},
  "Actions": {
    "#LogService.ClearLog": {
      "target": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Actions/LogService.Reset"
    }
  },
  "Entries": {
    "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/LogServices/Log1/Entries"
  }
}
