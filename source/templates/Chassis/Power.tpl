<%
    setdefault ("SLOT_ID", "#")

    setdefault ("fan_HSC_Power_sensor_name", "")
    setdefault ("power_consumed_watts", "")
    setdefault ("HSC_status", "")
    setdefault ("HSC_status_MFR", "")

    setdefault ("reading_value", "")
    setdefault ("upper_critical_threshold", "")
    setdefault ("lower_critical_threshold", "")

    setdefault ("psu1_power_capacity", "")
    setdefault ("psu1_power_output_watt", "")
    setdefault ("psu1_model_number", "")
    setdefault ("psu1_manufacturer_name", "")
    setdefault ("psu1_firmware_version", "")    
    setdefault ("psu1_serial_number", "")
    setdefault ("psu1_part_number", "")

    setdefault ("psu2_power_capacity", "")
    setdefault ("psu2_power_output_watt", "")
    setdefault ("psu2_model_number", "")
    setdefault ("psu2_manufacturer_name", "")
    setdefault ("psu2_firmware_version", "")    
    setdefault ("psu2_serial_number", "")
    setdefault ("psu2_part_number", "")

    setdefault ("psu3_power_capacity", "")
    setdefault ("psu3_power_output_watt", "")
    setdefault ("psu3_model_number", "")
    setdefault ("psu3_manufacturer_name", "")
    setdefault ("psu3_firmware_version", "")
    setdefault ("psu3_serial_number", "")
    setdefault ("psu3_part_number", "")

    setdefault ("psu4_power_capacity", "")
    setdefault ("psu4_power_output_watt", "")
    setdefault ("psu4_model_number", "")
    setdefault ("psu4_manufacturer_name", "")
    setdefault ("psu4_firmware_version", "")
    setdefault ("psu4_serial_number", "")
    setdefault ("psu4_part_number", "")

    setdefault ("psu5_power_capacity", "")
    setdefault ("psu5_power_output_watt", "")
    setdefault ("psu5_model_number", "")
    setdefault ("psu5_manufacturer_name", "")
    setdefault ("psu5_firmware_version", "")
    setdefault ("psu5_serial_number", "")
    setdefault ("psu5_part_number", "")

    setdefault ("psu6_power_capacity", "")
    setdefault ("psu6_power_output_watt", "")
    setdefault ("psu6_model_number", "")
    setdefault ("psu6_manufacturer_name", "")
    setdefault ("psu6_firmware_version", "")
    setdefault ("psu6_serial_number", "")
    setdefault ("psu6_part_number", "")
%>

{
    "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
    "@odata.context": "/redfish/v1/$metadata#Power",
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power",
    "@odata.type": "#Power.v1_2_0.Power",
    "Id": "Power",
    "Name": "Power",
    "PowerControl": [
    % for  i, (k, v) in enumerate(PowerControls.iteritems()):
    {
        <% if i != len(PowerControls)-1:
                closetag = ","
            else:
                closetag = ""
        end %>
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerControl/{{v['sensor_id']}}",
        "MemberId": "{{v['sensor_id']}}",
        "SensorNumber": "{{v['sensor_number']}}",
        "Name": "{{v['sensor_name']}}",
        "PowerConsumedWatts": "{{v['power_consumed_watts']}}",
        "PowerLimit": {
            "LimitInWatts": "{{v['power_limit']}}",
            "LimitException": "LogEventOnly"
        },
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
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
    }{{closetag}}
    % end
    ],
    "Voltages": [
    % for  i, (k, v) in enumerate(Voltages.iteritems()):
    {
        <% if i != len(Voltages)-1:
                closetag = ","
            else:
                closetag = ""
        end %>
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Voltages/{{v['sensor_id']}}",
        "MemberId": "{{v['sensor_id']}}",
        "SensorNumber": "{{v['sensor_number']}}",
        "Name": "{{v['sensor_name']}}",
        "ReadingVolts": "{{v['reading_value']}}",
        "UpperThresholdCritical": "{{v['upper_critical_threshold']}}",
        "LowerThresholdCritical": "{{v['lower_critical_threshold']}}",
        "MinReadingRange": "{{v['min_reading_range']}}",
        "MaxReadingRange": "{{v['max_reading_range']}}",
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "RelatedItem": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
            }
        ]
    }{{closetag}}
    % end
    ],
    "PowerSupplies": [
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/1",
        "MemberId": "1",
        "Name": "Power Supply Bay 1",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/1/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/1/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/1/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu1_power_capacity}}",
        "LastPowerOutputWatts": "{{psu1_power_output_watt}}",
        "Model": "{{psu1_model_number}}",
        "Manufacturer": "{{psu1_manufacturer_name}}",
        "FirmwareVersion": "{{psu1_firmware_version}}",
        "SerialNumber": "{{psu1_serial_number}}",
        "PartNumber": "{{psu1_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    },
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/2",
        "MemberId": "2",
        "Name": "Power Supply Bay 2",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/2/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/2/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/2/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu2_power_capacity}}",
        "LastPowerOutputWatts": "{{psu2_power_output_watt}}",
        "Model": "{{psu2_model_number}}",
        "Manufacturer": "{{psu2_manufacturer_name}}",
        "FirmwareVersion": "{{psu2_firmware_version}}",
        "SerialNumber": "{{psu2_serial_number}}",
        "PartNumber": "{{psu2_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    },
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/3",
        "MemberId": "3",
        "Name": "Power Supply Bay 3",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/3/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/3/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/3/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu3_power_capacity}}",
        "LastPowerOutputWatts": "{{psu3_power_output_watt}}",
        "Model": "{{psu3_model_number}}",
        "Manufacturer": "{{psu3_manufacturer_name}}",
        "FirmwareVersion": "{{psu3_firmware_version}}",
        "SerialNumber": "{{psu3_serial_number}}",
        "PartNumber": "{{psu3_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    },
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/4",
        "MemberId": "4",
        "Name": "Power Supply Bay 4",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/4/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/4/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/4/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu4_power_capacity}}",
        "LastPowerOutputWatts": "{{psu4_power_output_watt}}",
        "Model": "{{psu4_model_number}}",
        "Manufacturer": "{{psu4_manufacturer_name}}",
        "FirmwareVersion": "{{psu4_firmware_version}}",
        "SerialNumber": "{{psu4_serial_number}}",
        "PartNumber": "{{psu4_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    },
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/5",
        "MemberId": "5",
        "Name": "Power Supply Bay 5",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/5/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/5/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/5/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu5_power_capacity}}",
        "LastPowerOutputWatts": "{{psu5_power_output_watt}}",
        "Model": "{{psu5_model_number}}",
        "Manufacturer": "{{psu5_manufacturer_name}}",
        "FirmwareVersion": "{{psu5_firmware_version}}",
        "SerialNumber": "{{psu5_serial_number}}",
        "PartNumber": "{{psu5_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    },
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/PowerSupplies/6",
        "MemberId": "6",
        "Name": "Power Supply Bay 6",
        "Status": {
            "State": "Enabled",
            "Health": "Warning",
            "Oem": {
                "Microsoft": {
                    "@odata.type": "#OcsPower.v1_0_0.Status",
                    "Faults": "Faults"
                }
            }
        },
        "Oem": {
            "Actions": {
                "#PowerSupply.ClearFaults": {
                    "target":  "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/6/Actions/PowerSupply.ClearFaults"
                },
                "#PowerSupply.FirmwareUpdate": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/6/Actions/PowerSupply.FirmwareUpdate",
                    "FWRegion@Redfish.AllowableValues": [
                        "A",
                        "B",
                        "Bootloader"
                    ]
                },
                "#PowerSupply.FirmwareUpdateState": {
                    "target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power/PowerSupplies/6/Actions/PowerSupply.FirmwareUpdateState",
                    "Operation@Redfish.AllowableValues": [
                        "Abort",
                        "Query"
                    ]
                }
            }
        },
        "PowerCapacityWatts": "{{psu6_power_capacity}}",
        "LastPowerOutputWatts": "{{psu6_power_output_watt}}",
        "Model": "{{psu6_model_number}}",
        "Manufacturer": "{{psu6_manufacturer_name}}",
        "FirmwareVersion": "{{psu6_firmware_version}}",
        "SerialNumber": "{{psu6_serial_number}}",
        "PartNumber": "{{psu6_part_number}}",
        "RelatedItem": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
        }
        ],
        "Redundancy": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/0"
            }
        ]
    }
    ],
    "Redundancy": [
    {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power#/Redundancy/1",
        "MemberId": "1",
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
    ],
    "Oem": {}
}