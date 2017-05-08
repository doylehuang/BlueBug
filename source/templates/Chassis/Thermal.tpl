<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Thermal",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal",
  "@odata.type": "#Thermal.v1_1_0.Thermal",
  "Id": "Thermal",
  "Name": "Thermal",
  "Temperatures": [
    % for  i, (k, v) in enumerate(temperatures.iteritems()):
    {
        "PhysicalContext": "SystemBoard",
        <% if i != len(temperatures)-1:
                closetag = ","
            else:
                closetag = ""
         end %>
        % for l, (ks, vs) in enumerate(v.iteritems()):
            % if ks == "sensor_id":
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Temperatures/{{vs}}",
                "MemberId": "{{vs}}",
            % elif ks == "sensor_number":
                "SensorNumber": "{{vs}}",
            % elif ks == "sensor_name":
                "Name": "{{vs}}",
            % elif ks == "value":
                "ReadingCelsius": "{{vs}}",
            % elif ks == "upper_critical_threshold":
                "UpperThresholdCritical": "{{vs}}",
            % end
        % end
        "MinReadingRange": 0,
        "MaxReadingRange": 200,
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
  "Fans": [
    % for  i, (k, v) in enumerate(fans.iteritems()):
    {
        "PhysicalContext": "Backplane",
        <% if i != len(fans)-1:
                closetag = ","
            else:
                closetag = ""
         end %>
        % for l, (ks, vs) in enumerate(v.iteritems()):
            % if ks == "sensor_id":
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Fans/{{vs}}",
                "MemberId": "{{vs}}",
            % elif ks == "sensor_name":
                "Name": "{{vs}}",
            % elif ks == "sensor_number":
                "SensorNumber": "{{vs}}",
            % elif ks == "value":
                "Reading": "{{vs}}",
                "ReadingUnits": "RPM",
            % elif ks == "lower_critical_threshold":
                "LowerThresholdCritical": "{{vs}}",
            % elif ks == "PWM":
            "Oem": {
                "PWM": "{{vs}}"
            },
            % end
        % end
        "MinReadingRange": 0,
        "MaxReadingRange": 5000,
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "Redundancy": [
        {
            "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal#/Redundancy/0"
        }
        ],
        "RelatedItem": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}"
            }
        ]
    }{{closetag}}
    % end
  ],
  "Redundancy": [
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
  ]
}
