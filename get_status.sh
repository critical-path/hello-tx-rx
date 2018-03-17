#!/bin/bash

current_directory=$(pwd)
main_directory=/var/lib/hello-tx-rx
log_directory=${main_directory}/log

echo "Running Hello log analyzer..."
cd ${log_directory}
python3 -B ${log_directory}/app_log.py
cd ${current_directory}

