#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable(format='text')  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>
<head>
  <title>DUG Log</title>

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
    DUG Log
  </div>
</div>
"""

#Print the menu
menu = open("menu.html", "r")
for line in menu:
  print line

print '<div class="response"><pre>'
log = open("/var/dug/dug.log", "r").readlines()
for line in reversed(log):
  print line.strip()
print "</pre></div>"

print """
  </body>
  </html>
"""
