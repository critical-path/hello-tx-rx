#!/bin/bash

home_directory=$HOME
main_directory=${home_directory}/hello
config_subdirectory=${main_directory}/config
log_subdirectory=${main_directory}/log
rx_subdirectory=${main_directory}/rx
tx_subdirectory=${main_directory}/tx
systemd_subdirectory=${main_directory}/systemd

echo "making main directory..."

mkdir ${main_directory}

echo "making subdirectories..."

mkdir ${config_subdirectory}
mkdir ${log_subdirectory}
mkdir ${rx_subdirectory}
mkdir ${tx_subdirectory}
mkdir ${systemd_subdirectory}

echo "changing file modes..."
chmod +x get_status.sh
chmod +x open_firewall.sh

echo "moving files to sub-directories..."

mv config.txt ${config_subdirectory}
mv lib_config.py ${config_subdirectory}

mv lib_log.py ${log_subdirectory}
mv app_log.py ${log_subdirectory}

mv log.txt ${rx_subdirectory}
mv lib_rx.py ${rx_subdirectory}
mv app_rx.py ${rx_subdirectory}

mv lib_tx.py ${tx_subdirectory}
mv app_tx.py ${tx_subdirectory}

mv hello_rx.service ${systemd_subdirectory}
mv hello_tx.service ${systemd_subdirectory}
mv hello_firewall.service ${systemd_subdirectory}

mv get_status.sh ${main_directory}
mv open_firewall.sh ${main_directory}
mv set_up.sh ${main_directory}

echo "making symbolic links..."

ln -s ${config_subdirectory}/config.txt ${log_subdirectory}
ln -s ${config_subdirectory}/lib_config.py ${log_subdirectory}

ln -s ${config_subdirectory}/config.txt ${rx_subdirectory}
ln -s ${config_subdirectory}/lib_config.py ${rx_subdirectory}

ln -s ${config_subdirectory}/config.txt ${tx_subdirectory}
ln -s ${config_subdirectory}/lib_config.py ${tx_subdirectory}

ln -s ${rx_subdirectory}/log.txt ${log_subdirectory}

echo "changing ownership of all files..."

chown -R $(id -un).$(id -gn) ${main_directory}/*

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

