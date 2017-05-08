<%
    setdefault ("SLOT_ID", "#")
    setdefault ("serial_number", "")
    setdefault ("bmc_health_status", "")
    setdefault ("bmc_health_value", "0")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#BMCHealth",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/BMCHealth",
  "@odata.type": "#BmcHealth.v1_3_0.BmcHealth",
  "Id": "{{SLOT_ID}}",
  "Name": "BMCHealth",
  "SerialNumber": "{{serial_number}}",
  "Status": "{{bmc_health_status}}",
  "Value": "{{bmc_health_value}}"
  
}
