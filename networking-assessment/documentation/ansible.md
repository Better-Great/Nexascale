

# Establish connection Between VMs

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



```sh
ansible-playbook playbooks/webserver.yml
ansible-playbook playbooks/deploy.yml
ansible-playbook playbooks/haproxy.yml
```
