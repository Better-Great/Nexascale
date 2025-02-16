#!/bin/bash

# Color codes for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to validate directory path
validate_path() {
    if [[ ! "$1" =~ ^/.*$ ]]; then
        echo -e "${RED}Error: Please provide an absolute path${NC}"
        return 1
    fi
    return 0
}

# Script header
clear
echo "================================================="
echo "    Project Directory and SSH Setup Script v1.0"
echo "================================================="
echo

# Get project directory path
read -p "Enter project directory path (e.g., /var/www/project): " project_dir

# Validate directory path
while ! validate_path "$project_dir"; do
    read -p "Enter project directory path: " project_dir
done

# Get group name
read -p "Enter the developers group name: " group_name

# Verify group exists
if ! getent group "$group_name" > /dev/null; then
    echo -e "${RED}Error: Group $group_name does not exist${NC}"
    exit 1
fi

# Create and setup project directory
echo -e "\nSetting up project directory..."
if mkdir -p "$project_dir"; then
    chown "root:$group_name" "$project_dir"
    chmod 755 "$project_dir"
    echo -e "${GREEN}Successfully created and configured $project_dir${NC}"
else
    echo -e "${RED}Failed to create directory${NC}"
    exit 1
fi

# SSH restrictions
echo -e "\nSetting up SSH restrictions..."
read -p "Enter usernames to restrict SSH access (space-separated): " -a restricted_users

if [ ${#restricted_users[@]} -gt 0 ]; then
    # Backup SSH config
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
    
    # Add DenyUsers line
    echo -e "\n# SSH access restrictions" >> /etc/ssh/sshd_config
    echo "DenyUsers ${restricted_users[*]}" >> /etc/ssh/sshd_config
    
    # Restart SSH service
    if systemctl restart sshd; then
        echo -e "${GREEN}Successfully configured SSH restrictions${NC}"
    else
        echo -e "${RED}Failed to restart SSH service${NC}"
        echo "Restoring backup..."
        mv /etc/ssh/sshd_config.backup /etc/ssh/sshd_config
        systemctl restart sshd
        exit 1
    fi
else
    echo -e "${YELLOW}No users specified for SSH restriction${NC}"
fi

# Summary
echo -e "\n================================================="
echo "                 Setup Summary"
echo "================================================="
echo -e "Project Directory: ${GREEN}$project_dir${NC}"
echo -e "Owner Group: ${GREEN}$group_name${NC}"
echo -e "Permissions: ${GREEN}755${NC}"
if [ ${#restricted_users[@]} -gt 0 ]; then
    echo -e "SSH Restricted Users: ${GREEN}${restricted_users[*]}${NC}"
fi
echo "================================================="