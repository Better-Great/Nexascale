# System Resource Monitor
## Overview
This Python script monitors your computer's CPU and memory usage. It shows these stats on screen and saves them to a file for later review.
## Requirements
- Python 3.6 or higher
- `psutil` library (install with `pip install psutil`)

### Setup

1. Create a virtual environment (recommended):
```sh
sudo apt update
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
2. Install required package:
```sh
pip install psutil
```
3. Run the script
```sh
python system_monitor.py
```
4. To stop monitoring, press `Ctrl+C`

## How It Works
### Step-by-Step Explanation

#### 1. Create Log Directory (`create_log_directory function`):
- Checks if a "logs" folder exists
- Creates one if it doesn't exist
- Returns the folder name

#### 2. Generate Log Filename (`get_log_filename function`):
- Creates a unique filename using the current date and time
- Example: `logs/system_usage_20250313_120145.csv`

#### 3. Initialize Log File (`initialize_log_file function`):
- Creates a new CSV file
- Writes column headers: Timestamp, CPU_Usage, Memory_Usage

#### 4. Get System Usage (`get_system_usage function`):
- Uses `psutil` to measure current CPU usage (as %)
- Uses `psutil` to measure current memory usage (as %)
- Returns both values

#### 5. Log Data (`log_data function`):
- Shows CPU and memory usage on screen
- Adds current time, CPU, and memory values to the log file

#### 6. Main Function (`main`):
- Sets up the logging system
- Starts a loop that:
    - Gets current CPU and memory usage
    - Displays and logs the values
    - Waits 5 seconds
    - Repeats until you press Ctrl+C

## Understanding the Output
When running, you'll see updates like this:
```sh
CPU Usage: 24.0% Memory Usage: 20.5%
CPU Usage: 1.0% Memory Usage: 20.6%
```
The CSV file will contain:
```sh
Timestamp,CPU_Usage,Memory_Usage
2025-03-13 00:15:26,24.0,20.5
2025-03-13 00:15:36,1.0,20.6
```

### Why This Matters
Monitoring system resources helps you:
- Find programs that use too much CPU or memory
- Track resource usage over time
- Detect performance issues
- Plan for system upgrades

### Customization
You can easily modify the script to:
- Change how often it checks (currently every 5 seconds)
- Add more types of data to track
- Change where log files are saved

Just look for the `interval = 5` line in the code to adjust the timing.
