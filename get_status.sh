#!/bin/bash

home_directory=$HOME
main_directory=${home_directory}/hello
log_subdirectory=${main_directory}/log

echo "Running Hello log analyzer..."
cd ${log_subdirectory}
python3 -B app_log.py
