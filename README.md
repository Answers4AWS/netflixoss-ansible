# NetflixOSS Ansible Playbooks

[![Join the chat at https://gitter.im/Answers4AWS/netflixoss-ansible](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Answers4AWS/netflixoss-ansible?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Welcome to the [NetflixOSS Cloud Prize award winning playbooks, AMIs and CloudFormation templates](http://techblog.netflix.com/2013/11/netflix-open-source-software-cloud.html).

[Ansible](https://github.com/ansible/ansible/) is a configuration management system that is [very simple to learn and use](http://answersforaws.com/episodes/2-ansible-and-aws/).

This project is a set of Ansible Playbooks to configure instances to run some of the [NetflixOSS](http://netflix.github.io/) projects.

These playbooks are quite low level as they include each step required to configure a service. If you are looking for the __easiest__ way to get started with NetflixOSS projects, launch your desired [NetflixOSS CloudFormation template](https://github.com/Answers4AWS/netflixoss-ansible/tree/master/cloudformation).

## Projects

- Archaius (waiting on https://github.com/Netflix/archaius/issues/132)
- [Aminator](#aminator)
- [Asgard](#asgard)
- [Edda](#edda)
- [Eureka](#eureka)
- [Genie](#genie)
- [Ice](#ice)
- Lipstick (coming soon)
- [Simian Army](#simian-army)

## Prerequisites

1. [Ansible installed](http://www.ansibleworks.com/docs/gettingstarted.html) on your laptop
1. The [Ansible EC2 Inventory](http://docs.ansible.com/intro_dynamic_inventory.html#example-aws-ec2-external-inventory-script) configured
1. Clone this repository

For steps 1 and 2, [watch the first 3 minutes of Episode 2 - Ansible and AWS](http://answersforaws.com/episodes/2-ansible-and-aws/).

## Features

These playbooks are built to be run on the following operating systems:
- Ubuntu 12.04 LTS
- Amazon Linux

They have also been written in a way where you can use the same playbook to configure a running server, or build a custom AMI.

### Base configuration

The base configuration is gets a system ready for production. You can find the [base tasks here](https://github.com/Answers4AWS/noss-ansible/tree/master/playbooks/roles/base/tasks), but in summary it:
- installs some packages
 - Python with the latest Boto
 - AWS CLI
 - security packages including fail2ban
 - Emacs and Vim (no religion here)
- does some basic system hardening

## Projects

### Aminator

[Aminator](https://github.com/Netflix/aminator) is a tool for creating EBS AMIs for AWS. Before running the playbook, there are a few things we need to do:

[More detailed instructions for Aminator can be found here](http://answersforaws.com/code/netflixoss/aminator/)

1. Create an Aminator [IAM Role](https://console.aws.amazon.com/iam/home?#roles) with [this policy](https://github.com/Netflix/aminator/wiki/Configuration#sample-policy)
1. Create an Aminator security group
 - Allow port 22 for SSH
1. If you don't already, create a new Key pair, and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. Launch a new EC2 instance using the above IAM Role, Security Group and key pair. Use Ubuntu 12.04 LTS as the AMI.
1. Set the `Name` tag of the instance to `Aminator`
1. Confirm you can see the instance using the Ansible EC2 inventory
```
$ /etc/ansible/hosts | grep 'Aminator'
```

Now you can run the playbook

```
$ ansible-playbook playbooks/aminator-ubuntu.yml -l 'tag_Name_Aminator'
```

If you are using this playbook, there is a decent chance you want to use the Ansible Provisioner for Aminator as well. Since this has not been merge yet (spam _mtripoli_ and _kvick_ if you want this merged), instead of pulling Aminator from their repo, it pulls from here: https://github.com/pas256/aminator.git. You can modify the file in `roles/aminator/vars/main.yml` and change the repo if you like. Aminator is installed to `/usr/local/aminator`.

The playbook also checks out this repo as well, so you can start baking your own AMIs based off these playbooks. You can find it here: `/usr/local/netflixoss-ansible`

One more thing. If you want to pay it forward, this playbook also installs [DistAMI](https://github.com/Answers4AWS/distami). Now there are no excuses for keeping useful AMIs private.

Once the playbook is finished, you can SSH to the instance an start aminating. Example:

```
ssh ubuntu@ec2.xyz
sudo aminate -e ec2_ansible_linux -B ami-bb2ab88b aminator-ubuntu.yml 
```

If all of that seems too hard, feel free to use the [Aminator CloudFormation template](https://github.com/Answers4AWS/netflixoss-ansible/blob/master/cloudformation/aminator.json) to bring up Aminator in just a few clicks.

### Asgard

[Asgard](https://github.com/Netflix/asgard) is an application deployments and cloud management web interface for AWS. Before running the playbook, there are a few things we need to do:

[More detailed instructions for Asgard can be found here](http://answersforaws.com/code/netflixoss/asgard/)

1. Create an Asgard security group
 - Allow port 22 for SSH
 - Allow port 80 for HTTP
 - Allow port 8080 for HTTP
1. If you don't already have one, create a new Key Pair, and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. Launch a new EC2 instance using the above Security Group and key pair. Use Ubuntu 12.04 LTS as the AMI.
1. Set the `Name` tag of the instance to `Asgard`
1. Confirm you can see the instance using the Ansible EC2 inventory
```
$ /etc/ansible/hosts | grep 'Asgard'
```

Now you can run the playbook

```
$ ansible-playbook playbooks/asgard-ubuntu.yml -l 'tag_Name_Asgard'
```

This will configure the instance to be running the [latest snapshot build](https://netflixoss.ci.cloudbees.com/job/asgard-master/lastSuccessfulBuild/artifact/target/) of Asgard. If you prefer to run the stable version of Asgard, you want to build the WAR file yourself, just specify the path to the WAR file:

```
$ ansible-playbook playbooks/asgard-ubuntu.yml -l 'tag_Name_Asgard' -e "local_war=$HOME/Downloads/asgard.war"
```

Once the playbook is finished, you will have Asgard running inside Tomcat on your EC2 instance. You can access Asgard via HTTP as the ROOT application (no directory). Example:

```
http://ec2-12-12-12-12.us-west-2.compute.amazonaws.com/
```

### Eureka

[Eureka](https://github.com/Netflix/eureka) is a service registry for resilient mid-tier load balancing and failover. Before running the playbook, there are a few things we need to do:

[More detailed instructions for Eureka can be found here](http://answersforaws.com/code/netflixoss/eureka/)

1. Create a Eureka security group
 - Allow port 22 for SSH
 - Allow port 80 for HTTP
1. If you don't already have one, create a new Key Pair, and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. Launch a new EC2 instance using the above Security Group and key pair. This time, we will use Amazon Linux.
1. Set the `Name` tag of the instance to `Eureka`
1. Confirm you can see the instance using the Ansible EC2 inventory
```
$ /etc/ansible/hosts | grep 'Eureka'
```

Now you can run the playbook

```
$ ansible-playbook playbooks/eureka-amazon-linux.yml -l 'tag_Name_Eureka'
```

This will configure the instance to be running the [latest snapshot build](https://netflixoss.ci.cloudbees.com/job/eureka-master/lastSuccessfulBuild/artifact/eureka-server/build/libs/eureka-server-1.1.121.war) of Eureka. If you prefer to build your own WAR file yourself, just specify the path to the WAR file:

```
$ ansible-playbook playbooks/eureka-amazon-linux.yml -l 'tag_Name_Eureka' -e "local_war=$HOME/Downloads/eureka-server.war"
```

Once the playbook is finished, you will have Eureka Server running inside Tomcat on your EC2 instance. You can access it via HTTP. Example:

```
http://ec2-12-23-34-45.us-west-1.compute.amazonaws.com/eureka/
```

### Edda

[Edda](https://github.com/Netflix/edda) is a service to track changes in an AWS region, multiple regions and/or multiple accounts. Before running the playbook, there are a few things we need to do:

[More detailed instructions for Edda can be found here](http://answersforaws.com/code/netflixoss/edda/)

1. Create an Edda security group
 - Allow port 22 for SSH
 - Allow port 80 for HTTP
1. If you don't already have one, create a new Key Pair, and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. Create an [IAM Role](https://console.aws.amazon.com/iam/home?#roles) called 'edda' with [this policy](https://github.com/Netflix/edda/wiki/AWS-Permissions#example-policy)
1. Launch a new EC2 instance using the above Security Group, key pair and IAM Role. You can use with Ubuntu or Amazon Linux for the OS.
1. Set the `Name` tag of the instance to `Edda`
1. Confirm you can see the instance using the Ansible EC2 inventory
```
$ /etc/ansible/hosts --refresh-cache | grep 'Edda'
```

Now you can run the playbook

```
$ ansible-playbook playbooks/edda-amazon-linux.yml -l 'tag_Name_Edda'
 or
$ ansible-playbook playbooks/edda-ubuntu.yml -l 'tag_Name_Edda'
```

This will configure the instance to be running the [latest snapshot build](https://netflixoss.ci.cloudbees.com/job/edda-master/lastSuccessfulBuild/artifact/build/libs/edda-2.1-SNAPSHOT.war) of Edda. If you prefer to build your own WAR file yourself, just specify the path to the WAR file:

```
$ ansible-playbook playbooks/edda-amazon-linux.yml -l 'tag_Name_Edda' -e "local_war=$HOME/Downloads/edda.war"
```

Once the playbook is finished, you will have Edda running inside Tomcat with MongoDB on your EC2 instance. You can access then [make queries to it via HTTP](https://github.com/Netflix/edda/wiki/REST). Example:

```
http://ec2-12-212-12-121.us-west-2.compute.amazonaws.com/edda/api/v2/view/instances;_pp
```

If all of that seems too hard, feel free to use the [Edda CloudFormation template](https://github.com/Answers4AWS/netflixoss-ansible/blob/master/cloudformation/edda.json) to bring it up in just a few clicks.

_NOTES_:

1. This is not production quality. If the instance dies, you loose your history. This is meant as a quick way to get Edda up and running and see if you like it. Have a look at [this wiki page for running Edda in production](https://github.com/Netflix/edda/wiki/Resiliency).


### Genie

[Genie](https://github.com/Netflix/genie) is the NetflixOSS Hadoop Platform as a Service. It provides REST-ful APIs to run Hadoop, Hive and Pig jobs, and to manage multiple Hadoop resources and perform job submissions across them.

[More detailed instructions for Genie can be found here](http://answersforaws.com/code/netflixoss/genie/)

1.  If you don't already have one, create a new Key Pair, and add it to your keychain or SSH agent so you don't need to specify it later:

        $ ssh-add mykey.pem

1.  Launch an Elastic MapReduce (EMR) Cluster using the above Key Pair
    -  Use the 2.4.2 AMI
    -  Make sure the master node is at least an `m1.medium` so that Tomcat has enough RAM to run
    -  Get EMR to install Hive 0.11
    -  Get EMR to Install Pig 0.11.1
1.  Either: 
    -  modify the `ElasticMapReduce-master` security group and allow port 7001 access from your IP address only
    -  OR, set up a [proxy to the Elastic MapReduce master](http://answersforaws.com/episodes/1-foxyproxy/) and access it that way
1.  Go to the EC2 page, and set the `Name` tag of the master node to `Genie`
1.  Confirm you can see the instance using the Ansible EC2 inventory

        $ /etc/ansible/hosts | grep 'Genie'

OK, you are now ready to install Genie on the master node of the EMR JobFlow.
 
    $ ansible-playbook playbooks/genie-hadoop-emr.yml -l 'tag_Name_Genie'

This will configure the master node to be running the 
[latest snapshot build](https://netflixoss.ci.cloudbees.com/job/genie-master/lastSuccessfulBuild/artifact/genie-web/build/libs/genie-web-0.22-SNAPSHOT.war)
of Genie. If you prefer to build your own WAR file yourself, just specify the path to the WAR file:

    $ ansible-playbook playbooks/genie-hadoop-emr.yml -l 'tag_Name_Genie' -e "local_war=/path/to/genie.war"

Once the playbook is finished, you will have Genie running inside Tomcat on your EMR master node. You can access it via HTTP. Example:

    http://ec2-123-123-123-123.compute.amazonaws.com:7001/



### Ice

[Ice](https://github.com/Netflix/ice) provides a birds-eye view of your AWS usage and costs. Before running the playbook, there are a few things we need to do:

[More detailed instructions for Ice can be found here](http://answersforaws.com/code/netflixoss/ice/)

1. Create an Ice security group
 - Allow port 22 for SSH
 - Allow port 80 for HTTP
1. If you don't already have one, create a new Key Pair, and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. [Enable programmatic billing access](http://docs.aws.amazon.com/awsaccountbilling/latest/about/programaccess.html) on your AWS account, and take note of the bucket name
1. Create another S3 bucket that will be used as a workspace for Ice.
1. Create an Ice [IAM Role](https://console.aws.amazon.com/iam/home?#roles) that allows S3 read access to your billing bucket, and read and write access to the S3 working space bucket. It will also need read-only access to EC2 for things like describing reserved instance offerings. A samply policy (that probably gives more access than necessary) is available [in this repository](https://github.com/Answers4AWS/netflixoss-ansible/blob/master/playbooks/roles/ice/files/samply-ice.policy).
1. Launch a new EC2 instance using the above Security Group, key pair and IAM role. You can use either Ubuntu or Amazon Linux.
1. Set the `Name` tag of the instance to `Ice`
1. Confirm you can see the instance using the Ansible EC2 inventory
```
$ /etc/ansible/hosts | grep 'Ice'
```
1. OK, the instance is now ready. Before running the playbook, [edit the variables file](https://github.com/Answers4AWS/netflixoss-ansible/blob/master/playbooks/roles/ice/vars/main.yml) and fill in the values for bucket names and the like. The file is documented.
 
Now you can run the playbook

```
$ ansible-playbook playbooks/ice-amazon-linux.yml -l 'tag_Name_Ice'
```

This will configure the instance to be running the 
[latest snapshot build](https://netflixoss.ci.cloudbees.com/job/ice-master/lastSuccessfulBuild/artifact/target/ice.war)
of Ice. If you prefer to build your own WAR file yourself, just specify the path to the WAR file:

```
$ ansible-playbook playbooks/ice-amazon-linux.yml -l 'tag_Name_Ice' -e "local_war=$HOME/Downloads/ice.war"
```

Once the playbook is finished, you will have Ice running inside Tomcat on your EC2 instance. You can access it via HTTP. Example:

```
http://ec2-123-123-123-123.compute.amazonaws.com/dashboard/summary
```



### Simian Army

The [Simian Army](https://github.com/Netflix/SimianArmy) are tools for keeping your cloud operating in top form. For example, Chaos Monkey is a resiliency tool that helps applications tolerate random instance failures. Before running the playbook, there are a few things we need to do:

[More detailed instructions for the Simian Army can be found here](http://answersforaws.com/code/netflixoss/simian-army/)

1. Create a Simian Army [IAM Role](https://console.aws.amazon.com/iam/home?#roles) with [this policy](https://github.com/Answers4AWS/netflixoss-ansible/blob/master/cloudformation/simian-army.json#L82)
1. Create a Simian Army security group
 - Allow port 22 for SSH
 - Allow port 80 for REST access only from your own IP address
1. Create a new Key pair (if you don't already have one) and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. Launch a new EC2 instance using the above IAM Role, Security Group and key pair. Use Ubuntu 12.04 LTS as the AMI.
1. Set the `Name` tag of the instance to `SimianArmy`
1. Confirm you can see the instance using the Ansible EC2 inventory
```
$ /etc/ansible/hosts | grep 'SimianArmy'
```

Now you can run the playbook

```
$ ansible-playbook playbooks/simian-army-ubuntu.yml -l 'tag_Name_SimianArmy'
```

Once the playbook is finished, you can SSH to the instance an start configure the Simian Army. Example:

```
ssh ubuntu@ec2.xyz
cd /usr/local/tomcat/webapps/simianarmy/WEB-INF/classes/
sudo emacs chaos.properties
sudo service tomcat7 restart
```

The log files are located at `/var/log/tomcat7`, with `catalina.out` being the main one.

If all of that seems too hard, feel free to use the [Simian Army CloudFormation template](https://github.com/Answers4AWS/netflixoss-ansible/blob/master/cloudformation/simian-army.json) to bring up the Simian Army in just a few clicks.


## Feedback

If you have feedback, comments or suggestions, please feel free to contact Peter at Answers for AWS, create an [Issue](https://github.com/Answers4AWS/netflixoss-ansible/issues), or submit a pull request.

## About Answers for AWS

These playbooks were written by [Peter Sankauskas](https://twitter.com/pas256), founder of [Answers for AWS](http://answersforaws.com/) - a consulting company focused on helping business get the most out of AWS. If you are looking for help with AWS, please [contact us](http://answersforaws.com/contact/). 

## License

Copyright 2013 Answers for AWS LLC

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
