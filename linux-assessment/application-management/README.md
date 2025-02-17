# Nginx Installation &Setup Script

This guide will walk you through the Nginx setup script. Irrespective of yoour experceince level, this script makes it super easy to get Nginx up and running with all the right configurations.

## What Does This Script Do?
In simple terms, this script:
- Installs Nginx
- Makes sure it starts when your server boots up
- Sets up automatic restarts if something goes wrong
- Keeps an eye on Nginx to make sure it's running smoothly
- Manages log files so they don't eat up your disk space

## Prerequisites
You'll need:
- A Linux system (Ubuntu/Debian-based)
- Root access or sudo privileges
- Basic command line knowledge

## Quick Start
1. Make it executable:
```sh
chmod +x nginx-install.sh
```
2. Run it:
```sh
sudo ./nginx-install.sh
```
That's it! The script will handle everything else.

## What Does The Script Actually Do?
Let's break down what the script sets up for you:
1. Installation & Basic Setup
- Installs the latest version of Nginx
- Enables it to start automatically when your server boots up
- Configures proper service settings

2. Automatic Recovery
- Sets up automatic restart if Nginx crashes
- Waits 5 seconds between restart attempts (prevents rapid-fire restarts)

3. Health Monitoring
- Creates a monitoring script that runs every 5 minutes
- Checks if Nginx is running
- Verifies that it's actually responding to requests
- Logs any issues it finds

4. Log Management
- Sets up log rotation to prevent disk space issues
- Keeps logs for 4 weeks
- Compresses old logs automatically
- Maintains clean log handover when rotating

## Monitoring & Maintenance
After running the script, you can:
Check Nginx status:
```sh
systemctl status nginx
```
View monitoring logs:
```sh
tail -f /var/log/nginx-monitoring.log
```
Check the monitoring schedule:
```sh
crontab -l
```

## Troubleshooting
If something goes wrong, here's where to look:

1. Nginx error logs:
```sh
tail -f /var/log/nginx/error.log
```
2. Access logs:
```sh
tail -f /var/log/nginx/access.log
```
3. System logs
```sh
journalctl -u nginx
```

## Common Questions
#### Q: Will this overwrite my existing Nginx setup?
A: If you already have Nginx installed, the script will update it but preserve your existing configurations.

#### Q: How do I know if it's working?
A: After installation, visit http://your-server-ip in your browser. You should see the Nginx welcome page.

#### Q: What if I want to uninstall everything?
A: Run these commands:
```sh
sudo systemctl stop nginx
sudo apt remove nginx
sudo rm /etc/systemd/system/nginx.service.d/restart.conf
sudo rm /usr/local/bin/check-nginx.sh
```
