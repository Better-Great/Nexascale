#  How to Use These Scripts
## Making the Scripts Executable

1. The following commands can be used to make them executable:
```sh
chmod +x log_scanner_basic.py
chmod +x log_scanner_advance.py
```

2. To run the scripts:
```sh
# This will scan sample.log in the current directory and count ERROR occurrences.
./log_scanner_basic.py

.log_scanner_advanced.py sample.log
```

## Running the Advanced Script
I've added a directory scanning feature as the bonus. Here are some ways to use it:
1. Scan a single file:
```sh
./log_scanner_advance.py sample.log
```
2. Scan a directory (will find all .log files):
```sh
./log_scanner_advance.py /var/log
```
3. Filter by level:
```sh
./log_scanner_advance.py /var/log --level 
```
4. Filter by date range:
```sh
./log_scanner_advance.py /var/log --start-date 2025-03-02 --end-date 2025-03-
```
5. Show the filtered log entries:
```sh
./log_scanner_advance.py /var/log --level ERROR --show-logs
```


