#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sys
import requests
import xml.etree.ElementTree as ET
sys.path.insert(0, '/var/dug/')
import fw_creds
fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>DHCP Leases</title>

<style>

.titleblock {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100px;
    background-color: #e8ebeb;
}

.titleblock > .image {
    position: absolute;
    left: 15px;
    top: 15px;
    height: 100px;
}

.titleblock > .text {
    position: absolute;
    top: 40px;
    left: 43%;
    font:normal 30px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

ul {
    position: absolute;
    top: 100px;
    left: 0px;
    list-style-type: none;
    margin: 0;
    padding: 0;
    width: 150px;
    height: 100%;
    background-color: #e8ebeb;
}

li a {
    display: block;
    color: #000;
    padding: 8px 16px;
    text-decoration: none;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

li a:hover {
    background-color: #306a89;
    color: white;
}

.response {
    position: absolute;
    top: 125px;
    left: 175px;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

</style>
</head>
<body>

<div class="titleblock">
  <div class="image">
    <img src="/logo.svg" height="75px">
  </div>
  <div class="text">
    DHCP Leases
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response">'

values = {'type': 'op', 'cmd': '<show><dhcp><server><lease><interface>all</interface></lease></server></dhcp></show>', 'key': fwkey}
palocall = 'https://%s/api/' % (fwhost)
r = requests.post(palocall, data=values, verify=False)

dhcptree = ET.fromstring(r.text)
print "<table cellpadding=5 cellspacing=0 border=1>"
print "<tr><td>IP</td><td>MAC</td><td>State</td><td>Duration</td><td>Lease Time</td></tr>"
for lease in dhcptree.findall('./result/interface/entry'):
  print "<tr>"
  print "<td>%s</td>" % (lease.find('ip').text, )
  print "<td>%s</td>" % (lease.find('mac').text, )
  if lease.find('state') is not None:
    print "<td>%s</td>" % (lease.find('state').text, )
  else:
    print "<td></td>"
  if lease.find('duration') is not None:
    print "<td>%s</td>" % (lease.find('duration').text, )
  else:
    print "<td></td>"
  if lease.find('leasetime') is not None:
    print "<td>%s</td>" % (lease.find('leasetime').text, )
  else:
    print "<td></td>"
  print "</tr>"
print "</table>"

print "</div>"


print """
  </body>
  </html>
"""
