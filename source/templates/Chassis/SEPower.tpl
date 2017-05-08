<%
    setdefault ("SE_ID", "#")
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright © 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Power",
  "@odata.context": "/redfish/v1/$metadata#Power",
  "@odata.type": "#Power.v1_2_0.Power",
  "Id": "Power",
  "Name": "Power",
  "PowerControl": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Power#/PowerControl/1",
      "MemberId": "1",
      "Name": "Storage Enclosure {{SE_ID}} HSC Power",
      "PowerConsumedWatts": "{{power_consumption}}",
      "PowerLimit": {
        "LimitInWatts": 9000,
        "LimitException": "LogEventOnly"
      },
      "RelatedItem": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}"
        }
      ],
      "Status": {
        "State": "Enabled",
        "Health": "OK"
      },
      "Oem": {
        "HSC Status": "0x00",
        "HSC Status Manufacturer Specific": "0x00"
      }
    }
  ],
  "Voltages": [
    {
      "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Power#/Voltages/1",
      "MemberId": "1",
      "Name": "Storage Enclosure 1 HSC Voltage",
      "SensorNumber": "{{sensor_number}}",
      "Status": {
        "State": "Enabled",
        "Health": "OK"
      },
      "ReadingVolts": "{{voltage_value}}",
      "UpperThresholdCritical": "{{upper_critical_threshold}}",
      "LowerThresholdCritical": "{{lower_critical_threshold}}",
      "MinReadingRange": 0,
      "MaxReadingRange": 20,
      "PhysicalContext": "PowerSupply",
      "RelatedItem": [
        {
          "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}"
        }
      ]
    }
  ]
}