#!/bin/bash

# Creates and configures TUN/TAP device driver, necessary for creating a connection with openVPN
# See official documentation at https://www.kernel.org/doc/Documentation/networking/tuntap.txt
sudo mkdir -p /dev/net 
sudo mknod /dev/net/tun c 10 200
sudo chmod 666 /dev/net/tun
# Changes permissions to allow all users to read and write (not execute)

/bin/bash 
# Run terminal, because the container will otherwise exit immedeately