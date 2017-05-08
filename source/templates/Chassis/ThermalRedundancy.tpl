<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Redundancy/0",
  "MemberId": "0",
  "Name": "BaseBoard System Fans",
  "RedundancyEnabled": false,
  "RedundancySet": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/0"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/1"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/2"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/3"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/4"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/5"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/6"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/7"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/8"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/9"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/10"
        },
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/11"
        }
  ],
  "Mode": "N+m",
  "Status": {
    "State": "Disabled",
    "Health": "OK"
  },
  "MinNumNeeded": 10,
  "MaxNumSupported": 12
}
