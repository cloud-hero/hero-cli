In the following tutorial we'll describe how you can create in a few minute a scalable server setup which can be used for a bunch of web applications.

Here we'll use WordPress as our demo application but pretty much anything that uses those technologies would work just fine.

Step 1.
-------
###### Install the CloudHero CLI
```
$ git clone git@github.com:cloud-hero/hero-cli.git
$ cd hero-cli/
$ pip install -r requirements.txt
```
Step 2.
-------
###### Login or create an account
```
$ ./hero login
```
Step 3.
-------
###### Choose one of your configured providers or create a new one
```
$ ./hero provider ls
```
Step 4.
-------
###### Create a new environment where the nodes will be launched.
In this step we will select which cloud provider we want to work with, which location to use and the name of our environment
```
$ ./hero environment create -p 56fe7d5910d39669c06a5276 -l eu-west-1 -n bigsite-prod
```
Step 5:
-------
###### Add servers.
In order to have this scalable our strategy is to create two web servers, a load balancer and a database server.
This way we would be able to either scale horisontally by adding more web servers of vertically by increasing the size of the web servers one at a time.
```
$ ./hero node add --help
$ ./hero node add -e 5704a4ad10d396155383cd67 --pkg apache.mod_php5,php,php.mysql,php.gd,php.apcu,glusterfs -s t2.micro -n web1
$ ./hero node add -e 5704a4ad10d396155383cd67 --pkg apache.mod_php5,php,php.mysql,php.gd,php.apcu,glusterfs -s t2.micro -n web2
$ ./hero node add -e 5704a4ad10d396155383cd67 --pkg haproxy -s t2.micro -n loadbalancer1
$ ./hero node add -e 5704a4ad10d396155383cd67 --pkg mysql -s t2.micro -n mysql1
```
Step 6.
-------
###### Get the IP addresses of our servers so we can make the final settings on them.
```
$ ./hero node ls
```
Step 7.
-------
###### Add my SSH keys so I could login on those servers
