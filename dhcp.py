#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
import sqlite3
import StringIO
import fw_creds

fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey
dbfile = "/home/pi/pan_dhcp/devices.sql"
xmlfile = StringIO.StringIO()

def getDHCP(fwhost, fwkey):

  values = {'type': 'op', 'cmd': '<show><dhcp><server><lease><interface>all</interface></lease></server></dhcp></show>', 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  r = requests.post(palocall, data=values, verify=False)
  leases = []
  dhcptree = ET.fromstring(r.text)
  for lease in dhcptree.findall('./result/interface/entry'):
    ip = lease.find('ip').text
    mac = lease.find('mac').text
    if lease.find('hostname') is not None:
      host = lease.find('hostname').text
    else:
        host = ""
    info = {"ip" : ip, "mac" : mac, "host" : host}
    leases.append(info)
  return leases

def getDynamicName(dbfile, mac):

  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  val = (mac, )
  cursor.execute('select DeviceName from DevicesDynamic where DeviceMac = ?', val)
  return cursor.fetchone()

def getGroups(dbfile):

  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  cursor.execute('select distinct Groups from DevicesDynamic')
  groups = cursor.fetchall()
  return groups

def getGroupMembers(dbfile, group):

  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  val = (group, )
  cursor.execute('select DeviceName from DevicesDynamic where Groups = ?', val)
  return cursor.fetchall()

fwxml = '<uid-message>\n'
fwxml = fwxml + '\t<version>1.0</version>\n'
fwxml = fwxml + '\t<type>update</type>\n'
fwxml = fwxml + '\t<payload>\n'
fwxml = fwxml + '\t\t<login>\n'

leases=getDHCP(fwhost, fwkey)
for lease in leases:
  name = getDynamicName(dbfile, lease["mac"])
  if name is not None:
    fwxml = fwxml + '\t\t\t<entry name="' + name[0] + '" ip="' + lease["ip"] + '" timeout="0"/>\n'
  else:
    fwxml = fwxml + '\t\t\t<entry name="' + lease["mac"] + '-' + lease["host"] + '" ip="' + lease["ip"] + '" timeout="0"/>\n'

fwxml = fwxml + '\t\t</login>\n'
fwxml = fwxml + '\t\t<groups>\n'

groups = getGroups(dbfile)
for group in groups:
  fwxml = fwxml + '\t\t\t<entry name="' + group[0] +'">\n'
  members = getGroupMembers(dbfile, group[0])
  fwxml = fwxml + '\t\t\t\t<members>\n'
  for member in members:
   fwxml = fwxml + '\t\t\t\t\t<entry name="' + member[0] + '"/>\n'
  fwxml = fwxml + '\t\t\t\t</members>\n'
  fwxml = fwxml + '\t\t\t</entry>\n'

fwxml = fwxml + '\t\t</groups>\n'
fwxml = fwxml + '\t</payload>\n'
fwxml = fwxml + '</uid-message>'

xmlfile.write(fwxml)

files = {xmlfile: xmlfile.getvalue()}
values = {'type': 'user-id', 'key': fwkey}
palocall = 'https://' + fwhost + '/api'
r = requests.post(palocall, data=values, files=files, verify=False)
rtree = ET.fromstring(r.text)
print rtree.get('status')
