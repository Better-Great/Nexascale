

#### 1. Create an SSH Key 
Before creating the VMs, you need an SSH key to securely access them. If you don’t have an SSH key, create one using:
```sh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/nexascale_key
```

#### 2. Step 2: Create a Resource Group
Now, create a resource group called nexascale:
```sh 
az group create --name nexascale --location eastus
```
Azure free services are region-specific, so I opted for `eastus`

#### Step 3: Create the VMs
**1. Create the Load Balancer VM**
```sh
az vm create \
  --resource-group nexascale \
  --name loadbalancer \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/nexascale_key.pub \
  --public-ip-address loadbalancer-ip
```

**2. Create the Webserver 1 VM**
```sh
az vm create \
  --resource-group nexascale \
  --name webserver1 \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/nexascale_key.pub \
  --public-ip-address webserver1-ip
```

**3. Create the Webserver 2 VM**
```sh
az vm create \
  --resource-group nexascale \
  --name webserver2 \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/nexascale_key.pub \
  --public-ip-address webserver2-ip
```

**Verify Everything**
```sh
az vm list-ip-addresses --resource-group nexascale --output table

az vm list --resource-group nexascale --show-details --output table
```

**How to Access the Virtual Machines
```sh
# Loadbalancer Server
ssh -i ~/.ssh/nexascale_key azureuser@172.172.171.50
# Webeserver 1
ssh -i ~/.ssh/nexascale_key azureuser@40.71.191.134
# Webserver 2
ssh -i ~/.ssh/nexascale_key azureuser@172.191.95.80
```


Log into the Loadbalancer Server,
This would server as the master node

And create an ssh key on the server 
```
ssh-keygen -t rsa -b 4096 -f ~/.ssh/ansible_key
```