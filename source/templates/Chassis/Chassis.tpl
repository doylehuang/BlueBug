<%
    setdefault ("SLOT_ID", "#")
    setdefault ("manufacturer", "")
    setdefault ("model_name", "")
    setdefault ("serial_number", "")
    setdefault ("part_number", "")
    setdefault ("asset_tag", "")
    setdefault ("indicator_led", "")
    setdefault ("power_state", "")
    setdefault ("health_status", "")
    setdefault ("cableleds", {})
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#Chassis",
  "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}",
  "@odata.type": "#Chassis.v1_3_0.Chassis",
  "Id": "{{SLOT_ID}}",
  "Name": "Computer System Chassis",
  "ChassisType": "RackMount",
  "Manufacturer": "{{manufacturer}}",
  "Model": "{{model_name}}",
  "SKU": "",
  "SerialNumber": "{{serial_number}}",
  "PartNumber": "{{part_number}}",
  "AssetTag": "{{asset_tag}}",
  "IndicatorLED": "{{indicator_led}}",
  "CableLED": [
     % for  i, (k, v) in enumerate(cableleds.iteritems()):
     {
         <% if i != len(cableleds)-1:
                closetag = ","
            else:
                closetag = ""
         end %>
         % for g, (ks, vs) in enumerate(v.iteritems()):
             <% if g != len(v)-1:
                    closetag_p = ","
                else:
                    closetag_p = ""
              end %>
             % if ks == "sensor_name":
                 "Name": "{{vs}}"
             % elif ks == "value":
                 "Value": "{{vs}}"
             % end
             {{closetag_p}}
         % end
     }{{closetag}}
     % end
  ],
  "PowerState": "{{power_state}}",
  "Status": {
    "State": "Enabled",
    "Health": "{{health_status}}"
  },
  "BMCHealth": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/BMCHealth"
  },
  "Thermal": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Thermal"
  },
  "Power": {
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Power"
  },
  "Links": {
    "Contains": [
    ],
    "ManagedBy": [
      {
        "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}"
      }
    ],
    "PCIeDevices": [
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/1"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/2"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/3"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/4"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/5"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/6"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/7"
      },
      {
        "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/8"
      }
    ]
  },
  "Actions": {
    "#System.On": {
      "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Actions/On"
    },
    "#System.Off": {
      "Target": "/redfish/v1/Chassis/System/{{SLOT_ID}}/Actions/Off"
    }
  }
}
