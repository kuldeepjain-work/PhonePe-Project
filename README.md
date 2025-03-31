# Distributed Monitoring System

A system that allows running tests on slave/minion machines and viewing results through a central dashboard. For this Project I used SALT. Similar platform is ansible.

## System Components

This distributed monitoring system consists of two main components:

1. _Slave/Minion Side_: Machines that run the actual test files.
2. _Host/Storage Side_: Machine that stores test results and provides a web dashboard to view them.

## Slave/Minion Side Configuration

### Prerequisites

- Python 3.x
- SSH/SCP access to the storage host
- Cron (for scheduled execution)

### Setup Instructions

1. _Install Dependencies_:
   bash
   pip install -r requirements_minion.txt

2. _Configure Storage Host_:
   Edit the configuration to set the IP address of your storage host for SCP transfers.

3. _Set Up Cron Job_ (Optional):
   bash

   # Edit crontab

   crontab -e

   # Add a line to run tests periodically, for example every hour:

   0 \* \* \* \* /path/to/execute.sh

### Running Tests

Execute the test runner:

- For Refrence, I have also provided a sample pytest file.
- Save the test file locally.

bash
python3 run_pytest.py

You will be prompted for:

1. _The Path for the test file_: Enter the path to your pytest file
2. _The machine name(s) or pattern to run them on_: Specify which machines should execute the tests

The system will:

- Execute the tests on the specified machines
- Display the results locally
- Transfer the results to the storage host automatically

## Host/Storage Side Configuration

### Prerequisites

- Python 3.x
- FastAPI/Uvicorn
- Database (as specified in requirements)

### Setup Instructions

1. _Install Dependencies_:
   bash
   pip install -r requirements_host.txt

2. _Start the Dashboard Server_:
   bash
   uvicorn hosting_file:app --host 0.0.0.0 --port 8000 --reload

## Accessing the Dashboard

1. Open a web browser and navigate to:

   http://<localhost>:8000

2. _For New Users_:

   - Click on the registration link
   - Complete the registration form
   - Submit your credentials

3. _For Existing Users_:
   - Enter your login credentials
   - Access the dashboard

> _Note_: Test results will only appear in the dashboard after tests have been executed on the slave/minion side.

## Troubleshooting

- Ensure proper network connectivity between slave and host machines
- Verify that SCP transfers are configured correctly
- Check that all dependencies are installed on both systems
- Confirm that the host server is running and accessible on the specified port
