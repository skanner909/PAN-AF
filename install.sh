#!/bin/bash

#check to make sure Python is installed
python --version

#install pip
sudo apt-get update -y
sudo apt-get install python-pip -y

#use pip to install requests

pip install requests

#install sqlite3
sudo apt-get install sqlite3 -y

#set some necessary permissions
cd /home
sudo chmod 777 pi
cd pi
mkdir pan_dhcp
chmod 777 pan_dhcp
cd pan_dhcp

#create the devices database
echo 'CREATE TABLE DevicesDynamic (DeviceName "TEXT", DeviceMac "TEXT", Groups "Text");' > create.sql
sqlite3 devices.sql < create.sql
rm create.sql
chmod 777 devices.sql

#install the code that updates the firewall
wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/dhcp.py
chmod 777 dhcp.py

#update cron to execute the script every minute
cd /etc/cron.d
sudo wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/pan_dhcp_cron

#install apache2 and configure it to allow cgi
sudo apt-get install apache2 -y
sudo a2enmod cgid
sudo systemctl apache2 restart

#copy cgi scripts into the cgi directory
cd /usr/lib/cgi-bin
sudo wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/index.cgi
sudo chmod 777 index.cgi
sudo wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/keygen.cgi
sudo chmod 777 keygen.cgi

#copy default web page
cd /var/www/html
sudo rm index.html
sudo wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/index.html
sudo chmod 777 index.html
sudo wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/dus.css
sudo chmod 777 dus.css
sudo wget https://raw.githubusercontent.com/p0lr/PAN_DUG/master/logo.svg
sudo chmod 777 logo.svg
