#!/bin/bash

# Generate a timestamp in the format YYYY-MM-DD_HH-MM-SS
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Define the local output filename using the timestamp
local_output_file="/home/ubuntu/output_minions/${timestamp}.txt"

# Execute the local script and redirect its output to the local file
sudo bash /home/ubuntu/execute.sh >> "$local_output_file"

# Define remote server details
storage_host="ubuntu"
storage_ip="192.168.64.27"
storage_path="/home/ubuntu/output_minions"  # Update with the actual remote directory path

# Transfer the output file to the remote machine using scp
scp -o StrictHostKeyChecking=no "${local_output_file}" "${storage_host}@${storage_ip}:${storage_path}"