#!/usr/bin/env python3
"""
Log File Error Scanner - Basic Version
"""

def count_errors(log_file):
    # Count the number of ERROR occurrences in a log file
    error_count = 0
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if "ERROR" in line:
                    error_count += 1
    except FileNotFoundError:
        print(f"File not found: {log_file}")
        return 0
    except Exception as e:
        print(f"Something went wrong: {e}")
        return 0
        
    return error_count


if __name__ == "__main__":
    log_file = "sample.log"
    
    errors = count_errors(log_file)
    print(f"Found {errors} occurrences of 'ERROR' in logs.")