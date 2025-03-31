import os
import subprocess
from datetime import datetime
import getpass
import pytest
import salt.client

result_dir = "results"
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

username = getpass.getuser()


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
result_filename = f"{username}_{timestamp}.txt"
result_filepath = os.path.join(result_dir, result_filename)

def run_pytest(test_file_path,machine_input):
    absolute_test_file_path = os.path.abspath(test_file_path)

    if not os.path.exists(absolute_test_file_path):
        print(f"Test file not found: {absolute_test_file_path}")
        return


    machine_parts = [part.strip() for part in machine_input.split(',')]
    machines_str = ",".join([f"salt://{part}" if '*' in part else f"salt://{part}" for part in machine_parts])

    cmd = f"sudo pytest --hosts={machines_str} {absolute_test_file_path}"

    try:
        result = subprocess.run(cmd, shell=True ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(result_filepath, "w") as result_file:
            result_file.write(result.stdout)
        print(result.stdout)
    except Exception as e:
        print(f"Error running pytest: {str(e)}")

def transfer_file_to_server(result_dir):
    if not os.listdir(result_dir):
        print("No result files found in the results directory.")
        return

    files = os.listdir(result_dir)
    files = [os.path.join(result_dir, f) for f in files if os.path.isfile(os.path.join(result_dir, f))]
    master_path = max(files, key=os.path.getmtime)
    storage_host = "ubuntu@192.168.64.27"
    storage_path = f"/home/ubuntu/results/{os.path.basename(master_path)}"

    scp_command = f"scp -o StrictHostKeyChecking=no {master_path} {storage_host}:{storage_path}"
    try:
        subprocess.run(scp_command, shell=True, check=True)
        os.remove(master_path)
        print("File transferred and deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error transferring file: {str(e)}")
    except Exception as e:
        print(f"Error deleting the file: {str(e)}")

file_path = input("Enter the absolute file path of the test file: ").strip()
machine_input = input("Enter the machine name(s) or pattern: ")
run_pytest(file_path,machine_input)
transfer_file_to_server(result_dir)