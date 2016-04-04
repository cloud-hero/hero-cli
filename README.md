### CloudHero CLI

- [Description](#description)
- [Install](#install)
- [Usage examples](#usage-examples)
  - [Listing your environments](#listing-your-environments)
  - [Adding a new node](#adding-a-new-node)
  - [Listing your nodes](#listing-your-nodes)

## Description
CloudHero CLI is a open-source application written in python and it is build on top of [CloudHero API](https://docs.cloudhero.io)


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
$./hero register -e my@email.com -p password -o acme 
```

##Login
In order to use CloudHero CLI you need to login.
```bash
$./hero login -e me@email.com -p password
```

## Usage examples

### Providers
In order to deploy new servers using CloudHero CLI you need to register a cloud provider.
Currently we support AWS EC2 and DigitalOcean.

#### Add DigitalOcean
```bash
$./hero providers add digital_ocean -a DO_Access_Token --name mydoprovider
```

#### Add AWS EC2
```bash
$./hero providers add ec2 -a access_key -s secret_key --name myec2provider
```

### Delete
```bash
$./hero providers rm provider_id
```

### Environments 
An environment is a group (stack) of servers. You can give them any name, but we usualy call them production, staging, development.


#### Listing your environments:
```bash
$./hero environments ls
ENVIRONMENT-ID                NAME                LOCATION       NODES     NODE-NAMES
56fc3d7410d3960813c70d9a      london-cluster      lon1           2         docker-test
```

#### Adding a new node
```bash
$./hero nodes add -e 56fc3d7410d3960813c70d9a --packages docker -tags cluster:docker,size:small --name docker-master
```

#### Listing your nodes
```bash
$./hero nodes ls
NODE-ID                  NODE-NAME           ENVIRONMENT-ID           ENVIRONMENT-NAME    STATUS    PROVIDER  PUBLIC-IP        PRIVATE-IP       PACKAGES       TAGS
56fcc67e10d3960812a70d9c docker-master       56fc3d7410d3960813c70d9a london-cluster      running   do-2      178.62.40.103    10.131.13.179    docker         cluster:docker, size:small
51fcbfcf10d3960813c70d9b mysql-db            56fc3d7410d3960813c70d9a sf-cluster          stopped   do-2      -                -                mysql   -
```
