#!/bin/bash
set -e

# Check if hosts.old does not exist
if [ ! -f /etc/hosts.old ]; then
    # Copy hosts to hosts.old
    sudo sh -c 'cp /etc/hosts /etc/hosts.old'
    echo "hosts file has been copied to hosts.old"
else
    echo "hosts.old already exists"
fi

echo "running netbox import..."
python3 getNetBoxIPnames.py
echo "done"

if [ -f /etc/hosts.old ]; then
    if [ -f hosts.netbox ]; then
        # Copy hosts to hosts.old
        echo "merging to hosts..."
        sudo sh -c 'cat hosts.netbox >> /etc/hosts'
        echo "OK netbox hosts merged to hosts"
    else
        echo "FAIL hosts.netbox missing"
    fi
else
    echo "FAIL hosts.old missing"
fi
