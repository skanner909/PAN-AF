#!/usr/bin/env python

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

import os.path

def lastBack():
  if (os.path.isfile("/var/backup/lastback.txt")):
    file = open("/var/backup/lastback.txt", "r")
    lastpcap = file.read()
    file.close()
    return lastpcap
  else:
    return False

def getLastBack(lastback):
  try:
    file = open(lastback, "r")
    config = file.read()
    return config
  except:
    return False

def getConfig(fwhost, fwkey):
  values = {'type': 'op', 'cmd': '<show><config><running/></config></show>', 'key': fwkey}
  call = 'https://' + fwhost + '/api'
  try:
    request = requests.post(call, data=values, verify=False)
    tree = ET.fromstring(request.text)
    config = tree.find('./result/config')
    return ET.tostring(config)
  except:
    return False

lastback = lastBack()
if lastback:
  previousconfig = getLastBack(lastback)
  currentconfig = getConfig(fwhost, fwkey)
  if(previousconfig and currentconfig):
    if previousconfig != currentconfig:
      filename = "/var/backup/%s.xml" % (stamp, )
      file = open(filename, "w")
      file.write(currentconfig)
      file.close()

      file = open("/var/backup/lastback.txt", "w")
      file.write(filename)
      file.close()

  else:
    if not previousconfig:
      print "There was a problem reading the latest backup file"
    if not currentconfig:
      print "There was a problem getting the current configuration from the firewall"

else:
  runningconfig = getConfig(fwhost, fwkey)
  filename = "/var/backup/%s.xml" % (stamp, )
  file = open(filename, "w")
  file.write(runningconfig)
  file.close()

  file = open("/var/backup/lastback.txt", "w")
  file.write(filename)
  file.close()
