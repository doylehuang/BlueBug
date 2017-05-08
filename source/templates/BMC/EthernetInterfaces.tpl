<%
    setdefault ("SLOT_ID", "#")
%>

{
  "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
  "@odata.context": "/redfish/v1/$metadata#EthernetInterfaceCollection",
  "@odata.id": "/redfish/v1/Managers/System/{{SLOT_ID}}/EthernetInterfaces",
  "@odata.type": "#EthernetInterfaceCollection.EthernetInterfaceCollection",
  "Name": "Ethernet Network Interface Collection",
  "Description": "Collection of EthernetInterfaces for this Manager",
    %if defined ("Interfaces_list"):
	    "Members@odata.count": {{len(Interfaces_list)}},
	    "Members": [
	    	% for  i, (k, v) in enumerate(Interfaces_list.iteritems()):   
	    	{      
			    <% if i != len(Interfaces_list)-1:
			            closetag = ","               
			       else: 
			            closetag = ""
			     end %>
			     "@odata.id": "/redfish/v1/Managers/1/EthernetInterface/{{v}}"
		    }{{closetag}}
	 	    % end
	    ]
    %end
}

