# PAN_DUG
Dynamin User Groups for Palo Alto Networks devices

This package reads MAC address info from the both the firewall DHCP lease data as well as the firewall ARP table to create a username for each device.  This username can also be assigned statically using the web interface.

To install, issue the following commands:

1. wget -q https://raw.githubusercontent.com/p0lr/PAN_DUG/master/install.sh
2. chmod +x install.sh
3. ./install.sh

To use:

1. Browse to http://(ip)
2. Click on th Palo Alto Networks logo
3. Click on "Manage Firewall" in the navigation menu
4. Enter the firewall IP address or hostname, username, and password for an account that has the proper permissions

That's it!
