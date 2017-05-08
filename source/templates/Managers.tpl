<%
    setdefault ("SLOT_ID", "#")
%>
{
    "@odata.type": "#ManagerCollection.ManagerCollection",
    "@odata.context": "/redfish/v1/$metadata#Managers",
    "@odata.id": "/redfish/v1/Managers",
    "Name": "Managers Collection",
    "Members@odata.count": 1,
    "Members": [
        {
            "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}"
        }
    ]
}
