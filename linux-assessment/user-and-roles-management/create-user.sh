#!/bin/bash

# Color codes for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to validate input is not empty
validate_input() {
    local input=$1
    local message=$2
    if [[ -z "$input" ]]; then
        echo -e "${RED}Error: $message${NC}"
        return 1
    fi
    return 0
}

# Function to check if user exists
user_exists() {
    id "$1" &>/dev/null
    return $?
}

# Function to create user with password expiry
create_user() {
    local username=$1
    
    if user_exists "$username"; then
        echo -e "${YELLOW}Warning: User $username already exists. Skipping creation.${NC}"
        return 1
    fi

    # Create user with home directory and bash shell
    if useradd -m -s /bin/bash "$username"; then
        echo -e "${GREEN}Successfully created user: $username${NC}"
        
        # Prompt for password
        echo -e "\nSet initial password for $username"
        if passwd "$username"; then
            # Force password change on first login
            chage -d 0 "$username"
            echo -e "${GREEN}Password set successfully for $username${NC}"
            echo "User will be prompted to change password on first login"
            return 0
        else
            echo -e "${RED}Failed to set password for $username${NC}"
            return 1
        fi
    else
        echo -e "${RED}Failed to create user: $username${NC}"
        return 1
    fi
}

# Script header
clear
echo "================================================="
echo "      Linux User Management Script v1.0"
echo "================================================="
echo

# Create user group
read -p "Enter the name for the user group: " group_name

# Validate group name
while ! validate_input "$group_name" "Group name cannot be empty"; do
    read -p "Enter the name for the user group: " group_name
done

# Create group
if ! getent group "$group_name" > /dev/null; then
    if groupadd "$group_name"; then
        echo -e "${GREEN}Successfully created group: $group_name${NC}"
    else
        echo -e "${RED}Failed to create group. Exiting...${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Group $group_name already exists${NC}"
fi

# Get number of users to create
read -p "How many user accounts do you want to create? " num_users

# Validate number input
while ! [[ "$num_users" =~ ^[0-9]+$ ]] || [ "$num_users" -lt 1 ]; do
    echo -e "${RED}Please enter a valid number greater than 0${NC}"
    read -p "How many user accounts do you want to create? " num_users
done

# Create users
created_users=()
for ((i=1; i<=num_users; i++)); do
    echo -e "\n${YELLOW}User $i of $num_users${NC}"
    read -p "Enter username: " username
    
    # Validate username
    while ! validate_input "$username" "Username cannot be empty"; do
        read -p "Enter username: " username
    done
    
    if create_user "$username"; then
        created_users+=("$username")
        
        # Ask to add user to group
        read -p "Add $username to group $group_name? (y/n): " add_to_group
        case $add_to_group in
            [Yy]*)
                if usermod -aG "$group_name" "$username"; then
                    echo -e "${GREEN}Added $username to group $group_name${NC}"
                else
                    echo -e "${RED}Failed to add $username to group $group_name${NC}"
                fi
                ;;
            *)
                echo "Skipped adding $username to group $group_name"
                ;;
        esac
    fi
done

# Summary
echo -e "\n================================================="
echo "               Creation Summary"
echo "================================================="
echo -e "Group created: ${GREEN}$group_name${NC}"
echo "Users created:"
for user in "${created_users[@]}"; do
    echo -e "${GREEN}- $user${NC}"
done
echo "================================================="
echo "Remember: Users will be prompted to change their"
echo "passwords upon first login"
echo "================================================="