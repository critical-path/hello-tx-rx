#!/bin/bash

main_directory=/var/lib/hello-tx-rx
systemd_directory=/usr/lib/systemd/system

echo "stopping services..."
sudo systemctl stop hello_rx.service
sudo systemctl stop hello_tx.service
sudo systemctl stop hello_firewall.service

echo "disabling services..."
sudo systemctl disable hello_rx.service
sudo systemctl disable hello_tx.service
sudo systemctl disable hello_firewall.service

echo "deleting services..."
sudo rm ${systemd_directory}/hello_rx.service
sudo rm ${systemd_directory}/hello_tx.service
sudo rm ${systemd_directory}/hello_firewall.service

echo "deleting main directory..."
sudo rm -fR ${main_directory}

echo "deleting user named hello-tx-rx..."
sudo userdel -r hello-tx-rx

echo "deleting group named hello-tx-rx..."
sudo groupdel hello-tx-rx

