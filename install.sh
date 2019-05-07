#!/bin/bash

#check to make sure Python is installed
python --version

#install the python requests module
sudo apt-get install python-requests -y

#install sqlite3
sudo apt-get install sqlite3 -y

#create the directory for the primary dug code to live
cd /var
sudo mkdir dug
sudo chown www-data dug
sudo chgrp www-data dug

cd /var/dug

#create the devices database
sudo touch create.sql
sudo chmod 777 create.sql
sudo echo 'CREATE TABLE DevicesDynamic (DeviceName "TEXT", DeviceMac "TEXT", Groups "Text");' > create.sql
sudo sqlite3 devices.sql < create.sql
sudo rm create.sql
sudo chown www-data devices.sql
sudo chgrp www-data devices.sql
sudo chmod 755 devices.sql

#install the code that updates the firewall
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/dug.py
sudo chown www-data dug.py
sudo chgrp www-data dug.py
sudo chmod 755 dug.py

#update cron to execute the script every minute
cd /etc/cron.d
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/dug.cron

#install apache2 and configure it to allow cgi
sudo apt-get install apache2 -y
sudo a2enmod cgid
sudo service apache2 restart

#copy cgi scripts into the cgi directory
cd /usr/lib/cgi-bin
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/index.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/keygen.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/vlan.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/usermap.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/groupmap.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/arp.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_BUG/master/menu.html
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

#copy default web page
cd /var/www/html
sudo rm index.html
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/index.html
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/dus.css
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/logo.svg
sudo chown www-data *.*
sudo chgrp www-data *.*
sudo chmod 755 *.*

#create the file to hold the distinct list of MAC addresses seen on the firewall
sudo touch macs.txt
sudo chown www-data macs.txt
sudo chgrp www-data macs.txt
sudo chmod 755 macs.txt
