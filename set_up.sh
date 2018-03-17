#!/bin/bash

main_directory=/var/lib/hello-tx-rx
config_subdirectory=${main_directory}/config
log_subdirectory=${main_directory}/log
rx_subdirectory=${main_directory}/rx
tx_subdirectory=${main_directory}/tx
systemd_subdirectory=${main_directory}/systemd

echo "edit config.txt before running this script..."

echo "making user and group named hello-tx-rx..."
sudo useradd -r hello-tx-rx -d ${main_directory} -s /usr/sbin/nologin

echo "adding your user to group named hello-tx-rx..."
sudo usermod $(id -un) -aG hello-tx-rx

echo "making main directory..."
sudo mkdir ${main_directory}

echo "making subdirectories..."
sudo mkdir ${config_subdirectory}
sudo mkdir ${log_subdirectory}
sudo mkdir ${rx_subdirectory}
sudo mkdir ${tx_subdirectory}
sudo mkdir ${systemd_subdirectory}

echo "changing file modes..."
chmod +x get_status.sh
chmod +x open_firewall.sh

echo "copying files to sub-directories..."
sudo cp config.txt ${config_subdirectory}
sudo cp lib_config.py ${config_subdirectory}
sudo cp lib_log.py ${log_subdirectory}
sudo cp app_log.py ${log_subdirectory}
sudo cp log.txt ${rx_subdirectory}
sudo cp lib_rx.py ${rx_subdirectory}
sudo cp app_rx.py ${rx_subdirectory}
sudo cp lib_tx.py ${tx_subdirectory}
sudo cp app_tx.py ${tx_subdirectory}
sudo cp hello_rx.service ${systemd_subdirectory}
sudo cp hello_tx.service ${systemd_subdirectory}
sudo cp hello_firewall.service ${systemd_subdirectory}
sudo cp open_firewall.sh ${main_directory}
sudo cp get_status.sh ${main_directory}

echo "making symbolic links..."
sudo ln -s ${config_subdirectory}/config.txt ${log_subdirectory}
sudo ln -s ${config_subdirectory}/lib_config.py ${log_subdirectory}
sudo ln -s ${config_subdirectory}/config.txt ${rx_subdirectory}
sudo ln -s ${config_subdirectory}/lib_config.py ${rx_subdirectory}
sudo ln -s ${config_subdirectory}/config.txt ${tx_subdirectory}
sudo ln -s ${config_subdirectory}/lib_config.py ${tx_subdirectory}
sudo ln -s ${rx_subdirectory}/log.txt ${log_subdirectory}

echo "changing ownership of files..."
sudo chown -R hello-tx-rx.hello-tx-rx ${main_directory}/*

echo "opening firewall..."
sudo ${main_directory}/open_firewall.sh

echo "making services..."
sudo cp ${systemd_subdirectory}/hello_rx.service /usr/lib/systemd/system/
sudo cp ${systemd_subdirectory}/hello_tx.service /usr/lib/systemd/system/
sudo cp ${systemd_subdirectory}/hello_firewall.service /usr/lib/systemd/system/

echo "enabling services..."
sudo systemctl enable hello_rx.service
sudo systemctl enable hello_tx.service
sudo systemctl enable hello_firewall.service

echo "starting services..."
sudo systemctl start hello_rx.service
sudo systemctl start hello_tx.service
sudo systemctl start hello_firewall.service

echo "if you experienced any error when starting the services, then you probably forgot to edit config.txt before running this script..."

