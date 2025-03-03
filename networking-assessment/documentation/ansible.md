# Ansible Automation for Load Balancer Deployment on Azure

## 1. Establishing SSH Connection Between VMs
This is to ensure that the SSH key used in creating the VMs on Azure is available on the Load Balancer VM for secure remote access to the web servers. 

The Load balancer will server as the master VM, while the webserver 1 and 2 will be the slaves VM

```sh
# Copy your SSH key to the load balancer VM
scp -i ~/.ssh/nexascale_key ~/.ssh/nexascale_key azureuser@172.172.171.50:~/.ssh/

# Set proper permissions for the SSH key on the load balancer VM
chmod 600 ~/.ssh/nexascale_key

# Test SSH connection to the first web server
ssh -i ~/.ssh/nexascale_key azureuser@40.71.191.134

# Test SSH connection to the second web server
ssh -i ~/.ssh/nexascale_key azureuser@172.191.95.80
```
If SSH is successful, proceed with Ansible setup.

## 2. Ansible Configuration

### Step 1: Install Ansible on the Load Balancer Server
```sh
sudo apt update -y
sudo apt install ansible -y
```

### Step 2: Define Inventory File (inventory.ini)

Create an inventory file to manage target servers.
```sh
[webservers]
webserver1 ansible_host=40.71.191.134 ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/nexascale_key
webserver2 ansible_host=172.191.95.80 ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/nexascale_key

[loadbalancer]
loadbalancer ansible_host=172.172.171.50 ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/nexascale_key
```


### Step 3: Configuration Ssetup
Ensure that all the neccessary configuration for the file path are created as seen in the directory called `ansible/`

### Step4: Running Ansible Playbooks
Once everything is set up, run the playbooks in the following order:
```sh
ansible-playbook playbooks/webserver.yml
ansible-playbook playbooks/deploy.yml
ansible-playbook playbooks/haproxy.yml
```
### Step 5: Testing the Setup
**Step 1: Verify Web Servers Are Running**
```sh
# Access through the terminal 
curl -I http://40.71.191.134:8080
curl -I http://172.191.95.80:8090
# Access through the browser
http://40.71.191.134:8080
http://172.191.95.80:8090

```
**Step 2: Test Load Balancer Routing**
```sh
curl -I http://172.172.171.50
```