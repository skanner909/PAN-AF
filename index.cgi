#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting
import sqlite3

dbfile = "/home/pi/pan_dhcp/devices.sql"

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>Manage Dynamic Devices</title>

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

.form2 {
  position: absolute;
  width: 80%;
  top: 465px;
  left: 175px;
  border-radius: 5px;
  background-color: #e8ebeb;
  padding: 5px;
}

.form2 table {
  table-layout: auto;
  width: 100%;
  border-collapse: collapse;
  border: 5px solid #e8ebeb;
  border-radius: 5px;
  background-color: white;
}

.form2 th {
  padding: 15px;
  background-color: #306a89;
  color: white;
  border: 5px solid #e8ebeb;
  border-radius: 5px;
  font:normal 16px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

.form2 tr {
  width: 100%;
}

.form2 td {
  padding: 5px;
  border: 5px solid #e8ebeb;
  border-radius: 5px;
  font:normal 14px "Nimbus Sans Cond", tahoma, helvetica, arial, sans-serif;
}

.form2 .datacolumn {
  width: 31%;
  align: left;
}

.form2 .radiocolumn {
  width: 7%;
  align: center;
}

.form2 input[type=submit] {
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
devicename = form.getvalue("devicename")
devicemac = form.getvalue("devicemac")
devicetag = form.getvalue("devicetag")
devicedelete = form.getvalue("devicedelete")

if (devicedelete):
  print devicedelete
  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  try:
    cursor.execute('DELETE FROM DevicesDynamic WHERE DeviceName = ?', (devicedelete, ))
  except sqlite3.Error as e:
    print e.args[0]
  conn.commit()
  conn.close()

if (devicename and devicemac):
  conn = sqlite3.connect(dbfile)
  cursor = conn.cursor()
  values = (devicename, devicemac, devicetag)
  cursor.execute('INSERT INTO DevicesDynamic ("DeviceName", "DeviceMac", "Groups") VALUES (?,?,?)', values)
  conn.commit()
  conn.close()

print """
<div class="form1">
  <form method="post" action="/cgi-bin/index.cgi">
    <label>Name</label><br>
    <input type="text" name="devicename"/><br>
    <label>MAC Address</label><br>
    <input type="text" name="devicemac"/><br>
    <label>Group</label><br>
    <input type="text" name="devicetag"/><br>
    <input type="submit" value="Submit"/>
  </form>
</div>
"""

conn = sqlite3.connect(dbfile)
cursor = conn.cursor()
cursor.execute('select DeviceName, DeviceMac, Groups from DevicesDynamic order by Groups')
rows = cursor.fetchall()

print """
<div class="form2">
  <form method="post" action="/cgi-bin/index.cgi">
    <table>
      <col class="radiocolumn" />
      <col class="datacolumn" />
      <col class="datacolumn" />
      <col class="datacolumn" />
      <tr>
        <th>Delete</th>
        <th>Device Name</th>
        <th>MAC Address</th>
        <th>Group</th>
      </tr>
"""

for row in rows:
  print '      <tr><td align="center"><input type="radio" name="devicedelete" value="%s"/></td>' % (row[0], )
  for field in row:
    print "       <td>%s</td>" % (field, )
  print "      </tr>"

conn.close()

print """
    </table>
    <input type="submit" value="Submit">
  </form>
</div>
</body>
</html>
"""
