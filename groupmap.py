#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
import fw_creds

fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

#Make call to firewall to get XML DHCP lease information
values = {'type': 'op', 'cmd': '<show><user><user-ids><all/></user-ids></user></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

#Convert the response from the firewall to an ElementTree to parse as XML
tree = ET.fromstring(r.text)

if (tree.get('status') == "success"):
  print tree.find('result').text
