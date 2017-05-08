<%
    setdefault ("SLOT_ID", "#")
    setdefault ("SE_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright © 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosureSE_ID/Thermal",
  "@odata.context": "/redfish/v1/$metadata#Thermal",
  "@odata.type": "#Thermal.v1_1_0.Thermal",
  "Id": "Thermal",
  "Name": "Thermal",
  "Temperatures": [
    % for  i, (k, v) in enumerate(temperatures.iteritems()):
    {
        "PhysicalContext": "StorageBay",
        <% if i != len(temperatures)-1:
                closetag = ","
            else:
                closetag = ""
         end %>
        % for l, (ks, vs) in enumerate(v.iteritems()):
            % if ks == "sensor_id":
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}/Thermal#/Temperatures/{{vs}}",
                "MemberId": "{{vs}}",
            % elif ks == "sensor_name":
                "Name": "{{vs}}",
            % elif ks == "sensor_number":
                "SensorNumber": "{{vs}}",
            % elif ks == "celsius":
                "ReadingCelsius": "{{vs}}",
                "MinReadingRange": 0,
                "MaxReadingRange": 100,
            % elif ks == "upper_critical_threshold":
                "UpperThresholdCritical": "{{vs}}",
            % end
        % end
        "Status": {
        "State": "Enabled",
        "Health": "OK"
        },
        "RelatedItem": [
            {
                "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/StorageEnclosure{{SE_ID}}"
            }
        ]
    }{{closetag}}
    % end
  ]
}