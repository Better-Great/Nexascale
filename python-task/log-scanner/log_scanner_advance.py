#!/usr/bin/env python3
"""
Log File Error Scanner - Advanced Version

This script scans a log file, counts occurrences of "ERROR", and can filter logs
by date or severity level (INFO, WARNING, ERROR).
"""

import os
import re
import argparse
from datetime import datetime
from enum import Enum, auto


class LogLevel(Enum):
    """Enum representing log severity levels."""
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class LogEntry:
    """Class representing a parsed log entry."""
    
    def __init__(self, date, level, message):
        """
        Initialize a log entry.
        
        Args:
            date (datetime): The timestamp of the log entry
            level (LogLevel): The severity level of the log entry
            message (str): The log message
        """
        self.date = date
        self.level = level
        self.message = message
    
    def __str__(self):
        """Return string representation of the log entry."""
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} {self.level.name} {self.message}"


class LogAnalyzer:
    """Class for analyzing log files."""
    
    def __init__(self, log_file_path):
        """
        Initialize the log analyzer.
        
        Args:
            log_file_path (str): Path to the log file
            
        Raises:
            FileNotFoundError: If the log file doesn't exist
        """
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"Log file not found: {log_file_path}")
        
        self.log_file_path = log_file_path
        self.log_entries = []
        self._parse_log_file()
    
    def _parse_log_file(self):
        """Parse the log file and populate log_entries list."""
        # Regular expression to match log entries
        # Format: YYYY-MM-DD HH:MM:SS LEVEL Message
        log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR) (.+)"
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    match = re.match(log_pattern, line.strip())
                    if match:
                        date_str, level_str, message = match.groups()
                        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        level = LogLevel[level_str]
                        self.log_entries.append(LogEntry(date, level, message))
        except Exception as e:
            print(f"Error parsing log file: {e}")
    
    def count_by_level(self, level=None):
        """
        Count log entries by severity level.
        
        Args:
            level (LogLevel, optional): If provided, count only entries with this level
            
        Returns:
            int: Count of matching log entries
        """
        if level is None:
            return len(self.log_entries)
        
        return sum(1 for entry in self.log_entries if entry.level == level)
    
    def filter_by_date(self, start_date=None, end_date=None):
        """
        Filter log entries by date range.
        
        Args:
            start_date (datetime, optional): Start date for filtering (inclusive)
            end_date (datetime, optional): End date for filtering (inclusive)
            
        Returns:
            list: Filtered log entries
        """
        filtered_entries = self.log_entries
        
        if start_date:
            filtered_entries = [entry for entry in filtered_entries 
                               if entry.date.date() >= start_date.date()]
        
        if end_date:
            filtered_entries = [entry for entry in filtered_entries 
                               if entry.date.date() <= end_date.date()]
        
        return filtered_entries
    
    def filter_by_level(self, level):
        """
        Filter log entries by severity level.
        
        Args:
            level (LogLevel): Severity level to filter by
            
        Returns:
            list: Filtered log entries
        """
        return [entry for entry in self.log_entries if entry.level == level]
    
    def print_entries(self, entries):
        """
        Print log entries.
        
        Args:
            entries (list): List of LogEntry objects to print
        """
        for entry in entries:
            print(entry)


def parse_date(date_str):
    """
    Parse date string in YYYY-MM-DD format.
    
    Args:
        date_str (str): Date string
        
    Returns:
        datetime: Parsed date
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


def main():
    """
    Main function to run the script.
    """
    parser = argparse.ArgumentParser(description="Analyze log files and count errors")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("--count-only", action="store_true", help="Only show error count")
    parser.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], 
                        help="Filter by log level")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    try:
        analyzer = LogAnalyzer(args.log_file)
        
        # Basic error count
        error_count = analyzer.count_by_level(LogLevel.ERROR)
        print(f"Found {error_count} occurrences of 'ERROR' in logs.")
        
        if args.count_only:
            return
        
        # Filter by level if specified
        if args.level:
            level = LogLevel[args.level]
            filtered_by_level = analyzer.filter_by_level(level)
            print(f"\nEntries with level {args.level}: {len(filtered_by_level)}")
            if not args.start_date and not args.end_date:
                analyzer.print_entries(filtered_by_level)
        
        # Filter by date if specified
        start_date = parse_date(args.start_date) if args.start_date else None
        end_date = parse_date(args.end_date) if args.end_date else None
        
        if start_date or end_date:
            date_range = f"{args.start_date or 'beginning'} to {args.end_date or 'end'}"
            filtered_by_date = analyzer.filter_by_date(start_date, end_date)
            
            if args.level:
                level = LogLevel[args.level]
                filtered_entries = [e for e in filtered_by_date if e.level == level]
                print(f"\nEntries with level {args.level} from {date_range}: {len(filtered_entries)}")
            else:
                filtered_entries = filtered_by_date
                print(f"\nEntries from {date_range}: {len(filtered_entries)}")
            
            analyzer.print_entries(filtered_entries)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()