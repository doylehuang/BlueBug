<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0",
  "MemberId": "0",
  "Name": "PowerSupply Redundancy Group 1",
  "Mode": "Failover",
  "MaxNumSupported": 6,
  "MinNumNeeded": 3,
  "RedundancySet": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/0"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/1"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/2"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/3"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/4"
    },
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/5"
    }
  ],
  "Status": {
    "State": "Offline",
    "Health": "OK"
  }
}