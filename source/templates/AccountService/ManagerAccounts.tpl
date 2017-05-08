{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#ManagerAccountCollection",
  "@odata.type": "#ManagerAccountCollection.ManagerAccountCollection",
  "@odata.id": "/redfish/v1/AccountService/Accounts",
  "Name": "Accounts Collection",
  %if defined ("accounts"):
        "Members@odata.count": {{num_accounts}},
        "Members": [
            %sepr = ""
            %for list in accounts.itervalues ():
                %for usr in list:
                    %if (usr):
                        {{sepr}}{
                            "@odata.id": "/redfish/v1/AccountService/ManagerAccount/{{usr}}"
                        }
                        %sepr = ","
                    %end
                %end
            %end
        ]
}