# PAN_DUG
Dynamin User Groups for Palo Alto Networks devices

This package reads MAC address info from the both the firewall DHCP lease data as well as the firewall ARP table to create a username for each device.  This username can also be assigned statically using the web interface.

To install, issue the following commands:

wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/install.sh

chmod +x install.sh

./install.sh

To use:

Browse to http://<ip>

Click on th Palo Alto Networks logo

Click on "Manage Firewall" in the navigation menu

Enter the firewall IP address or hostname, username, and password for an account that has the proper permissions

That's it!
