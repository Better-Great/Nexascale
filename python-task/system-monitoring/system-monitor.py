#!/usr/bin/env python3
"""
System Resource Monitor - Monitors CPU and memory usage
"""

import psutil
import time
from datetime import datetime
import os

def create_log_directory():
    """Create a logs directory if it doesn't exist"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def get_log_filename(log_dir):
    """Generate a timestamped log filename"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{log_dir}/system_usage_{timestamp}.csv"

def initialize_log_file(filename):
    """Create the log file with headers"""
    with open(filename, "w") as f:
        f.write("Timestamp,CPU_Usage,Memory_Usage\n")
    print(f"Log file created: {filename}")

def get_system_usage():
    """Get current CPU and memory usage percentages"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

def log_data(filename, cpu, memory):
    """Log data to console and file"""
    # Print to console
    print(f"CPU Usage: {cpu:.1f}% Memory Usage: {memory:.1f}%")
    
    # Log to file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"{timestamp},{cpu:.1f},{memory:.1f}\n")

def main():
    """Main function to run the monitoring"""
    # Setup logging
    log_dir = create_log_directory()
    log_filename = get_log_filename(log_dir)
    initialize_log_file(log_filename)
    
    # Set monitoring interval (in seconds)
    interval = 5
    
    print(f"Starting system monitoring (press Ctrl+C to stop)...")
    print(f"Logging data every {interval} seconds")
    
    # Monitoring loop
    try:
        while True:
            cpu, memory = get_system_usage()
            log_data(log_filename, cpu, memory)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    finally:
        print(f"Data saved to {log_filename}")

if __name__ == "__main__":
    main()