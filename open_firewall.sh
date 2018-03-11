#!/bin/bash

echo "Opening firewall to UDP traffic from hosts on designated subnet..."
iptables --table filter --insert INPUT 1 --protocol udp --source 192.168.1.0/24 --destination 192.168.1.0/24 --jump ACCEPT

