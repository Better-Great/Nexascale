# Python Utilities Project
This repository contains three Python utility scripts for different system and data management tasks.
## Project Structure
```sh
python-utilities/
├── README.md
├── system_monitoring/
│   ├── monitor.py
│   └── logs/
├── weather_api/
│   └── weather_fetcher.py
└── log_scanner/
    ├── log_scanner.py
    └── sample.log
```
### [1. System Monitoring Script](./system-monitoring/)
Located in the system-monitoring/ directory, this script monitors and displays CPU and memory usage of the system.
#### Features:
- Real-time CPU and memory usage monitoring
- Configurable refresh interval
- Option to log data to a file for later analysis

#### Usage:
```sh
cd system-monitoring
python system-monitor.py
```

### [2. Weather API Interaction](./weather-data-fetching/)
Located in the weather_api/ directory, this script fetches weather data from OpenWeatherMap API.
#### Features:

- Retrieves current weather conditions for specified cities
- Displays temperature, weather condition, and humidity
- Supports multiple city queries

#### Usage:
```sh
cd weather-data-fetching
python weather-app.py
```
**Note**: You need to add the OpenWeatherMap API key in the script or as an environment variable.

### [3. Log File Error Scanner](./log-scanner/)
Located in the log_scanner/ directory, this script scans log files for error occurrences.

#### Features:
- Counts occurrences of "ERROR" in log files
- Enhanced filtering by date and severity level
- Supports multiple log file analysis

#### Usage:
```sh
cd log-scanner
python log-scanner-basic.py
python log-scanner-advance.py
```

### Requirements
- Python 3.6+
- Required libraries:
    - `psutil` (for system monitoring)
    - `requests` (for API interaction)
    - `datetime` (for log filtering)