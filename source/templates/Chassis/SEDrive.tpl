<%
    setdefault ("SLOT_ID", "#")
    setdefault ("SE_ID", "#")
    setdefault ("DRIVE_ID", "#")
%>

{
  "@odata.context": "/redfish/v1/$metadata#Drive",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Drives/Drive{{DRIVE_ID}}",
  "@odata.type": "#Drive.v1_1_0.Drive",
  "IndicatorLED": "{{drive_id_led}}",
  "Revision": "{{drive_revision}}",
  "Status": {
    "State": "{{drive_status}}",
    "Health": "OK"
  },
  "MediaType": "HDD",
  "CapableSpeedGbs": "{{drive_speed}}",
  "NegotiatedSpeedGbs": "{{drive_speed}}",
  "Links": {
  },
  "Actions": {
    "#Drive.On": {
      "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Drives/Drive{{DRIVE_ID}}/Actions/On"
    },
    "#Drive.Off": {
      "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Drives/Drive{{DRIVE_ID}}/Actions/Off"
    }
  }
}