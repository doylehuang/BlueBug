{
   "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
   "@odata.context": "/redfish/v1/$metadata#UpdateService.UpdateService",
   "@odata.id": "/redfish/v1/UpdateService",
   "@odata.type": "#UpdateService.v1_1_0.UpdateService",
  "Id": "UpdateService",
  "Name": "Update Service",
  "Status": {
  "State": "Enabled",
  "Health": "OK"
     
     
  },
  "ServiceEnabled": true,
  "Actions": {
    "#UpdateService.SimpleUpdate": {
    "target": "/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate",
    "TransferProtocol@Redfish.AllowableValues": [ "TFTP", "OEM" ]
       
         
      }
 
    }
}
