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

#Install supporting usermap and groupmap files
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/groupmap.py
sudo chown www-data groupmap.py
sudo chgrp www-data groupmap.py
sudo chmod 755 groupmap.py

sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/usermap.py
sudo chown www-data usermap.py
sudo chgrp www-data usermap.py
sudo chmod 755 usermap.py

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
sudo chown www-data index.cgi
sudi chgrp www-data index.cgi
sudo chmod 755 index.cgi
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/keygen.cgi
sudo chown www-data keygen.cgi
sudo chgrp www-data keygen.cgi
sudo chmod 755 keygen.cgi

#copy default web page
cd /var/www/html
sudo rm index.html
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/index.html
sudo chown www-data index.html
sudo chgrp www-data index.html
sudo chmod 755 index.html
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/dus.css
sudo chown www-data dus.css
sudo chgrp www-data dus.css
sudo chmod 755 dus.css
sudo wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/logo.svg
sudo chown www-data logo.svg
sudo chgrp www-data logo.svg
sudo chmod 755 logo.svg
