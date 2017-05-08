<%
    setdefault ("SLOT_ID", "#")
    setdefault ("ID", "#")
%>

{
    "@odata.context": "/redfish/v1/$metadata#PCIeDevice.PCIeDevice",
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/{{ID}}",
    "@odata.type": "#PCIeDevice.v1_0_0.PCIeDevice",
    "Id": {{ID}},
    "Name": "{{info['marketing_name']}}",
    "Description": "{{info['description']}}",
    "AssetTag": "free form asset tag",
    "Manufacturer": "{{info['manufacturer']}}",
    "Model": "{{info['model']}}",
    "SKU": "{{info['sku']}}",
    "SerialNumber": "{{info['serial_number']}}",
    "PartNumber": "{{info['gpu_part_number']}}",
    "DeviceType": "MultiFunction",
    "FirmwareVersion": "{{info['firmware_version']}}",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK"
    },
    "Links": {
        "PCIeFunctions": [
        {"@odata.id": "/redfish/v1/Chassis/1/PCIeDevices/{{ID}}/Functions/1"},
        {"@odata.id": "/redfish/v1/Chassis/1/PCIeDevices/{{ID}}/Functions/2"}
        ]
    }
}
