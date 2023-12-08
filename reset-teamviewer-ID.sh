#!/bin/bash
# Proper header for a Bash script.

netcard=$(ip route get 8.8.8.8 | grep -oP 'dev \K\S+')
macadr=$(ip link show $netcard | grep -oE 'link/ether\s([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}' | cut -d' ' -f2)
new_random2=$(openssl rand -hex 1)
newmacadr=${macadr:0:15}${new_random2}
teamviewpath=$(which teamviewer)

echo $newmacadr

if [ "$macadr" != "$newmacadr" ]; then
    sudo systemctl stop teamviewerd
    sudo rm /opt/teamviewer/config/global.conf

    sudo systemctl stop networking
    sudo ip link set dev $netcard down
    sudo ip link set dev $netcard address $newmacadr
    sudo ip link set dev $netcard up
    sudo systemctl start networking

    sudo systemctl start teamviewerd
    echo "Now you need Start again Teamviewer, accept EULA and Login again"
    
else
    echo "Run again!"
fi
