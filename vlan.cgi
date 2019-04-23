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

def getInterfaces(fwhost, fwkey):
  output = []
  values = {'type': 'op', 'cmd': '<show><interface>all</interface></show>', 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  for entries in tree.findall('./result/hw'):
    for entry in entries.findall('entry'):
      info = {}
      info['name'] = entry.find('name').text
      output.append(info)
  return output

def createSubInterface(fwhost, fwkey, vlaninterface, vlannumber, vlannetwork, vlanzoneregion, vlandescription):

  #Create the sub-interface
  print "Creating the sub-interface: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/network/interface/ethernet/entry[@name='%s']/layer3/units/entry[@name='%s.%s']" % (vlaninterface, vlaninterface, vlannumber)
  element = '<comment>%s</comment>' % (vlandescription, )
  element += '<tag>%s</tag>' % (vlannumber, )
  element += "<ip><entry name='%s.1/24'/></ip>" % (vlannetwork, )

  values = {'type': type, 'action': action, 'xpath': xpath, 'element': element, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  response = tree.find('msg')
  print "%s<br>" % (response.text, )

  #Create the zone, enable user-id, and add the sub-interface
  print "Creating the zone, enable user-id in the zone, and adding the sub-interface to the zone: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/zone"
  element = '<entry name="%s"><network><layer3><member>%s.%s</member></layer3></network>' % (vlanzoneregion, vlaninterface, vlannumber)
  element += '<enable-user-identification>yes</enable-user-identification></entry>'

  values = {'type': type, 'action': action, 'xpath': xpath, 'element': element, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  response = tree.find('msg')
  print "%s<br>" % (response.text, )

  #Add the sub-interface to the default router
  print "Adding the sub-interface to the default router: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/interface"
  element = "<member>%s.%s</member>" % (vlaninterface, vlannumber) 

  values = {'type': type, 'action': action, 'xpath': xpath, 'element': element, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  response = tree.find('msg')
  print "%s<br>" % (response.text, )

  #Configure DHCP
  print "Conguring DHCP: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/network/dhcp/interface/entry[@name='%s.%s']/server" % (vlaninterface, vlannumber)
  element = "<option><dns><primary>208.67.222.222</primary><secondary>208.67.220.220</secondary></dns>"
  element += "<lease><timeout>120</timeout></lease><gateway>%s.1</gateway><subnet-mask>255.255.255.0</subnet-mask>" % (vlannetwork, )
  element += "</option><ip-pool><member>%s.10-%s.250</member></ip-pool><mode>enabled</mode>" % (vlannetwork, vlannetwork)

  values = {'type': type, 'action': action, 'xpath': xpath, 'element': element, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  response = tree.find('msg')
  print "%s<br>" % (response.text, )

  #Add a region
  print "Adding a region: "
  type = "config"
  action = "set"
  xpath = "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/region"
  element = '<entry name="%s">' % (vlanzoneregion, )
  element += "<address><member>%s.0/24</member></address>" % (vlannetwork, )
  element += "<geo-location><latitude>39.938</latitude><longitude>-105.047</longitude></geo-location></entry>"

  values = {'type': type, 'action': action, 'xpath': xpath, 'element': element, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  tree = ET.fromstring(r.text)
  response = tree.find('msg')
  print "%s<br>" % (response.text, )

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Add a VLAN</title>

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

.form1 {
    position: absolute;
    top: 125px;
    left: 175px;
    border-radius: 5px;
    background-color: #e8ebeb;
    padding: 5px;
    width: 80%;
}

.form1 label {
    font:normal 16px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

.form1 select {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

.form1 input[type=text] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

.form1 input[type=submit] {
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
    background-color: #306a89;
    border: none;
    color: white;
    width: 100%;
    padding: 15px;
    text-decoration: none;
    cursor: pointer;
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
    Add a VLAN
  </div>
</div>

<ul>
  <li><a href="/cgi-bin/">Manage Devices</a></li>
  <li><a href="/cgi-bin/keygen.cgi">Manage Firewall</a></li>
  <li><a href="/cgi-bin/vlan.cgi">Add a VLAN</a></li>
</ul>
"""

form = cgi.FieldStorage()
vlaninterface = form.getvalue("vlaninterface")
vlannumber = form.getvalue("vlannumber")
vlanzoneregion = form.getvalue("vlanzoneregion")
vlandescription = form.getvalue("vlandescription")
vlannetwork = form.getvalue("vlannetwork")

if (vlaninterface and vlannumber and vlanzoneregion and vlandescription and vlannetwork):
  print '<div class="response">'
  createSubInterface(fwhost, fwkey, vlaninterface, vlannumber, vlannetwork, vlanzoneregion, vlandescription)
  print "</div>"



else:
  print """
  <div class="form1">
    <form method="post" action="/cgi-bin/vlan.cgi">
      <label>Interface</label><br>
      <select name="vlaninterface"/>
  """
  interfaces = getInterfaces(fwhost, fwkey)
  for interface in interfaces:
    print '        <option value="%s">%s</option>' % (interface['name'], interface['name'])

  print """
      </select></br>
      <label>VLAN Number (1-4096)</label><br>
      <input type="text" name="vlannumber"/><br>
      <label>Zone/Region Name</label><br>
      <input type="text" name="vlanzoneregion"/><br>
      <label>Description</label><br>
      <input type="text" name="vlandescription"/><br>
      <label>Network (10.19.xxx)</label><br>
      <input type="text" name="vlannetwork"/><br>
      <input type="submit" value="Submit"/>
    </form>
  </div>
  """

print """
  </body>
  </html>
"""
