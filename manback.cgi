#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET

import sys
sys.path.insert(0, '/var/dug/')
import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

import datetime
now = datetime.datetime.now()
stamp = "%s-%s-%s-%s-%s-%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

print 'Content-Type: application/xml'
print 'Content-Disposition: attachment; filename="config-%s.xml"\n' % (stamp, )

values = {'type': 'op', 'cmd': '<show><config><running/></config></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost, )
r = requests.post(palocall, data=values, verify=False)

tree = ET.fromstring(r.text)
config = tree.find('./result/config')
output = ET.tostring(config)
print output
