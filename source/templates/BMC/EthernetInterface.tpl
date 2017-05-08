<%
    if defined ("TemplateDefault"):
        setdefault ("Intf", "")
        setdefault ("Description", "")
        setdefault ("InterfaceHealth", "")
        setdefault ("InterfaceStatus", "")
        setdefault ("MacAddress", "")
        setdefault ("IPAddress", "")
        setdefault ("SubnetMask", "")
        setdefault ("Origin", "")
        setdefault ("Gateway", "")
    end
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#EthernetInterface",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/EthernetInterfaces/{{Intf}}",
  "@odata.type": "#EthernetInterface.v1_1_0.EthernetInterface",
  "Id": "{{Intf}}",
  "Name": "{{Intf}}",
  "Description": "{{Description}}",
    "Status": {
    	<% if defined ("InterfaceHealth"):
    		tag = ","
		else:
			tag = ""
		end %>

        % if defined ("InterfaceStatus"):
        	"State": "{{InterfaceStatus}}"{{tag}}
		% end
        % if defined ("InterfaceHealth"):
        	"Health": "{{InterfaceHealth}}"
        % end
    },
    % if defined ("MacAddress"):
    	"PermanentMACAddress": "{{MacAddress}}",
	% end
    "IPv4Addresses": [
        {
	        % if defined ("IPAddress"):
		    	"Address": "{{IPAddress}}",
			% end
			% if defined ("SubnetMask"):
		    	"SubnetMask": "{{SubnetMask}}",
			% end
			% if defined ("Origin"):
		    	"AddressOrigin": "{{Origin}}",
			% end
			% if defined ("Gateway"):
		    	"Gateway": "{{Gateway}}"
			% end
        }
    ]
}
