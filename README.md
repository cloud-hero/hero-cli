# Welcome to the CloudHero CLI! 

You can use our CLI to create any type of server environments or a scalable and high available container service on top of major public or private cloud providers.


## Description
CloudHero CLI is a open-source application written in python and it is build on top of [CloudHero API](https://docs.cloudhero.io)

## [Take the crash course here](https://github.com/cloud-hero/hero-cli/blob/master/docs/WEB-EXAMPLE.md)!

## Install
```
git clone https://github.com/cloud-hero/hero-cli.git  
cd hero-cli
pip install -r requirements.txt
./hero
```

## Account Registration
Once installed you need to create a account. If you already have an active CloudHero account you can skip this step.
```bash
$./hero register -e my@email.com -p password -o my_organization
```

## Login
In order to use CloudHero CLI you need to login.
```bash
$./hero login -e me@email.com -p password
```

## Usage examples

### Provider
In order to deploy new servers using CloudHero CLI you need to register a cloud provider.
Currently we support `AWS EC2` and `DigitalOcean`.

##### Add DigitalOcean
```bash
$./hero provider add digital_ocean -a DO_Access_Token --name my_dev_cloud
```

##### Add AWS EC2
```bash
$./hero provider add ec2 -a access_key -s secret_key --name my_prod_cloud
```

##### Delete
```bash
$./hero provider rm provider_id
```

##### List
```bash
$./hero provider ls
```

### Environment
An environment is a group of servers (nodes). You can give them any name, but we usualy call them production, staging, development.

##### Create
```bash
$./hero env create -p provider_id -l location -n name
```

| Parameter   | Description
| ----------- | -----------
| provider_id | The cloud provider that you choose to spin up the nodes. Use `$./hero provider ls` to obtain the id
| location    | The location where you want to spin up your servers. See below available locations. (eg. ams2 or us-east-1) 
| name        | Name your environment.(eg. Production or Staging)


###### Cloud Providers Locations

| Digital Ocean      | Amazon EC2                            |
|--------------------|---------------------------------------|
| Code - Name        | Code - Name                           |
| ams2 - Amsterdam 2 | us-east-1 - US East (N. Virginia)     |
| ams3 - Amsterdam 3 | us-west-2 - US West (Oregon)          |
| fra1 - Frankfurt 1 | us-west-1 - US West (N. California)   |
| lon1 - London 1    | eu-west-1 - EU (Ireland)              |
| nyc1 - New York 1  | eu-central-1 - EU (Frankfurt)         |
| nyc2 - New York 2  | ap-southeast-1 - Asia Pacific (Singapore) |
| nyc3 - New York 3  | ap-northeast-1 - Asia Pacific (Tokyo) |
| sfo1 - San Francisco 1 | ap-southeast-2 - Asia Pacific (Sydney) |
| sgp1 - Singapore 1 | ap-northeast-2 - Asia Pacific (Seoul) |
| tor1 - Toronto 1   | sa-east-1 - South America (São Paulo) |

##### List
```bash
$./hero env ls
```

##### Delete
```bash
$./hero env rm env_id
```

| Parameter  | Description |
|------------|-------------|
|env_id      | The environemnt that you created to run servers into. Use `$./hero environment ls` to obtain the id.

### Nodes
Nodes are servers which CloudHero will provision, install packages on and configure automatically for you.

##### Add
```bash
$./hero nodes add -e env_id -k package -s size --name mynode
```

| Parameters             | Description |
|------------------------|-------------|
| `-e` env_id            | The environemnt that you created to run servers into. Use `$./hero environment ls` to obtain the id.
| `-k` pakage            | Specify a comma separated list of packages which you would like to install. Eg. `-k apache,php,mysql`
| `--name` node_name     | Specify the name of the node which you would like to create or add more like it. Eg. `--name web1`


The following sizes are supported for DigitalOcean and Amazon.

| Digital Ocean |
| :-----------: |
| 512mb , 1gb , 2gb , 4gb , 8gb , 16gb , 32gb , 48gb , 64gb |
 
|AWS EC2 Instance Family | Current Generation Instance Types
|------------------------| ---------------------------------
| General purpose        | t2.nano , t2.micro , t2.small , t2.medium , t2.large , m4.large , m4.xlarge , m4.2xlarge , m4.4xlarge , m4.10xlarge , m3.medium , m3.large , m3.xlarge , m3.2xlarge
| Compute optimized      | c4.large , c4.xlarge , c4.2xlarge , c4.4xlarge , c4.8xlarge , c3.large , c3.xlarge , c3.2xlarge , c3.4xlarge , c3.8xlarge
| Memory optimized       | r3.large , r3.xlarge , r3.2xlarge , r3.4xlarge , r3.8xlarge
| Storage optimized      | i2.xlarge , i2.2xlarge , i2.4xlarge , i2.8xlarge , d2.xlarge , d2.2xlarge , d2.4xlarge , d2.8xlarge
| GPU instancesg         | 2.2xlarge , g2.8xlarge


###### Available packages

| Package         | Description |
|----------------:|-------------|
| apache          | The Apache HTTPd server
| apache.mod_php5 | Apache with support for PHP
| docker          | It will setup a Docker node or if you add it to multiple nodes a Docker cluster.
| glusterfs       | GlusterFS Scalable Network Filesystem
| haproxy         | HAProxy
| memcached       | The Memcached Server
| mongodb         | The MongoDB Server
| mysql           | The MYSQL Server
| nginx           | The nginx web server
| php             | PHP with the minimal standar modules 
| php.gd          | PHP with default and GD module
| php.mysql       | PHP with default and MYSQL module
| php.apcu        | PHP with default and APCU module
| redis           | The Redis Server

CloudHero always installs official and stable packages, either provided by the distro or by the makers of the software. The best practices are taken into account so you could always take over your infrastructure whenever you want to.
Don't take our word for it! The formulas for installing packages are [avaiable for study and improvement](https://github.com/cloud-hero/saltstack-formulas).

##### Scale
This option allows you to horizontally scale any running node, both up and down.
####### UP
```bash
$./hero nodes scale up -e env_id --name node_to_scale --count number_of_nodes 
```

####### DOWN
```bash
$./hero nodes scale down -e env_id --name node_to_scale --count number_of_nodes 
```

##### Delete
```bash
$./hero nodes scale rm node_id
```

##### SSH
This option allows you to connect securely using SSH to your nodes
```bash
$./hero nodes ssh node_id
```


### Docker
You connect to any Docker Swarm cluster provisioned with CloudHero CLI or API
```bash
$./hero docker env_id

EXPORT DOCKER_HOST=tcp://ip_of_swarm_node:4000
# Run this command to configure your shell: 
# eval "$(hero docker my-env)"
```
