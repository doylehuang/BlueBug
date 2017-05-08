<%
    setdefault ("SLOT_ID", "#")
    setdefault ("ID", "#")
    setdefault ("FUNC", "#")
%>

{
    "@odata.context": "/redfish/v1/$metadata#PCIeFunction.PCIeFunction",
    "@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/{{ID}}/Functions/{{FUNC}}",
    "@odata.type": "#PCIeFunction.v1_0_0.PCIeFunction",
    "Id": "Function{{FUNC}}",
    "Name": "PCIe Function {{FUNC}}",
    "FunctionId": {{FUNC}},
    "FunctionType": "Virtual",
    "DeviceClass": "Coprocessor",
    "DeviceId": "",
    "VendorId": "",
    "ClassCode": "",
    "RevisionId": "",
    "SubsystemId": "",
    "SubsystemVendorId": "",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK"
    },
    "Links": {
        "PCIeDevice": [
            {"@odata.id": "/redfish/v1/Chassis/System/{{SLOT_ID}}/PCIeDevices/{{ID}}"}
        ]
    }
}
