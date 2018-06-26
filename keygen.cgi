#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET

fwcredsfile = "/home/pi/pan_dhcp/fw_creds.py"

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Manage Firewall Credentials</title>

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

.form1 input[type=text] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

.form1 input[type=password] {
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

</style>
</head>
<body>
<div class="titleblock">
  <div class="image">
    <img src="/logo.svg" height="75px">
  </div>
  <div class="text">
    Dynamic User System
  </div>
</div>

<ul>
  <li><a href="/cgi-bin/">Manage Devices</a></li>
  <li><a href="/cgi-bin/keygen.cgi">Manage Firewall</a></li>
</ul>
"""

form = cgi.FieldStorage()
fwip = form.getvalue("fwip")
fwusername = form.getvalue("fwusername")
fwpassword = form.getvalue("fwpassword")

if (fwip and fwusername and fwpassword):
  values = {'type': 'keygen', 'user': fwusername, 'password': fwpassword}
  apicall = 'https://%s/api/' % (fwip, )
  response = requests.post(apicall, data=values, verify=False)
  if response:
    tree = ET.fromstring(response.text)
    if tree.get('status') == "success":
      fwkey = tree.find('./result/key').text
  if fwkey:
    file = open(fwcredsfile, "w")
    line = 'fwhost = "%s"\n' % (fwip, )
    file.write(line)
    line = 'fwkey = "%s"\n' % (fwkey, )
    file.write(line)
    file.close()

print """
<div class="form1">
  <form method="post" action="/cgi-bin/keygen.cgi">
    <label>Firewall IP Address or Hostname</label><br>
    <input type="text" name="fwip"/><br>
    <label>User</label><br>
    <input type="text" name="fwusername"/><br>
    <label>Password</label><br>
    <input type="password" name="fwpassword"/><br>
    <input type="submit" value="Submit"/>
  </form>
</div>
</body>
</html>
"""
