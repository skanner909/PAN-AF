#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
import fw_creds
import datetime

fwhost = fw_creds.fwhost
fwkey = fw_creds.fwkey

def fwCmd(cmd):
  values = {'type': 'op', 'cmd': cmd, 'key': fwkey}
  palocall = 'https://%s/api/' % (fwhost)
  try:
    r = requests.post(palocall, data=values, verify=False)
  except error as e:
    return false
  if r:
    tree = ET.fromstring(r.text)
    if tree.get('status') == "success":
      return tree
    else:
      return false

def runningLatest(tree):
  if tree.find('./result/sw-updates/msg').text == "No updates available":
    return True
  else:
    return False

def getCurrent(tree):
  for version in tree.findall('./result/sw-updates/versions/entry'):
    if version.find('current').text == "yes":
      return version.find('version').text
    return False

def getLatest(tree):
  for version in tree.findall('./result/sw-updates/versions/entry'):
    if version.find('latest').text == "yes":
      return version.find('version').text
    return False

def checkDownloaded(tree, latest):
  for version in tree.findall('./result/sw-updates/versions/entry'):
    if version.find('version').text == latest:
      if version.find('downloaded').text == "yes":
        return True
      else:
        return False

#Get firewall software version info
cmd = "<request><system><software><check></check></software></system></request>"
versions = fwCmd(cmd)
if versions is not False:
  if not runningLatest(versions):
    current = getCurrent(versions)
    latest = getLatest(versions)
    if latest is not False:
      if checkDownloaded(versions, latest) is False:
        print("Downloading the latest PAN-OS")
        #download
      print("Installing the latest PAN-OS")
      #install
