#!/bin/bash

# Function to check if script is run as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root or with sudo"
        exit 1
    fi
}

# Function to install Nginx
install_nginx() {
    echo "Updating package list..."
    apt update

    echo "Installing Nginx..."
    apt install -y nginx
    
    if [ $? -ne 0 ]; then
        echo "Failed to install Nginx"
        exit 1
    fi
}

# Function to configure auto-start and restart policies
configure_service() {
    echo "Enabling Nginx service..."
    systemctl enable nginx

    # Create directory for override configuration
    mkdir -p /etc/systemd/system/nginx.service.d/

    # Create override file for automatic restart
    cat > /etc/systemd/system/nginx.service.d/restart.conf << EOF
[Service]
Restart=always
RestartSec=5
EOF

    # Reload systemd configuration
    systemctl daemon-reload
}

# Function to create monitoring script
setup_monitoring() {
    echo "Setting up monitoring script..."
    
    # Create monitoring script
    cat > /usr/local/bin/check-nginx.sh << EOF
#!/bin/bash

# Check if Nginx is running
if ! systemctl is-active --quiet nginx; then
    systemctl restart nginx
    echo "Nginx was down, restarted at \$(date)" >> /var/log/nginx-monitoring.log
fi

# Check if Nginx is responding to HTTP requests
if ! curl -s --head http://localhost | grep "200 OK" > /dev/null; then
    systemctl restart nginx
    echo "Nginx was not responding, restarted at \$(date)" >> /var/log/nginx-monitoring.log
fi
EOF

    # Make script executable
    chmod +x /usr/local/bin/check-nginx.sh

    # Add to crontab if not already present
    if ! crontab -l | grep -q "check-nginx.sh"; then
        (crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/check-nginx.sh") | crontab -
    fi
}

# Function to setup log rotation
setup_logrotate() {
    echo "Setting up log rotation..."
    
    cat > /etc/logrotate.d/nginx << EOF
/var/log/nginx/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    notifempty
    create 0640 nginx nginx
    sharedscripts
    postrotate
        [ -s /run/nginx.pid ] && kill -USR1 \`cat /run/nginx.pid\`
    endscript
}
EOF
}

# Function to verify installation
verify_installation() {
    echo "Verifying Nginx installation..."
    
    # Check if service is running
    if ! systemctl is-active --quiet nginx; then
        echo "Error: Nginx is not running"
        return 1
    fi

    # Check if listening on port 80
    if ! ss -tulpn | grep :80 > /dev/null; then
        echo "Error: Nginx is not listening on port 80"
        return 1
    fi

    # Check if responding to HTTP requests
    if ! curl -s --head http://localhost | grep "200 OK" > /dev/null; then
        echo "Error: Nginx is not responding to HTTP requests"
        return 1
    fi

    echo "Nginx installation verified successfully!"
    return 0
}

# Main execution
main() {
    check_root
    install_nginx
    configure_service
    setup_monitoring
    setup_logrotate
    
    # Start Nginx
    systemctl start nginx
    
    # Verify installation
    verify_installation
    
    if [ $? -eq 0 ]; then
        echo "Nginx setup completed successfully!"
        echo "Monitoring script installed and running every 5 minutes"
        echo "Log rotation configured"
    else
        echo "Nginx setup encountered some issues. Please check the logs."
    fi
}

# Run main function
main