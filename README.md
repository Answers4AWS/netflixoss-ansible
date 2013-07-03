# NetflixOSS Ansible Playbooks

[Ansible](https://github.com/ansible/ansible/) is a configuration management system that is [very simple to learn](http://www.ansibleworks.com/docs/gettingstarted.html) and use.

This project is a set of Ansible Playbooks to configure instances to run some of the [NetflixOSS](http://netflix.github.io/) projects.

- [Asgard](#asgard)
- Aminator (coming soon)
- Edda (coming soon)
- Eureka (coming soon)
- Ice (coming soon)
- Simian Army (coming soon)

## Prerequisites

1. [Ansible installed](http://www.ansibleworks.com/docs/gettingstarted.html) on your laptop
1. The [Ansible EC2 Inventory](http://www.ansibleworks.com/docs/api.html/#example-aws-ec2-external-inventory-script) configured
1. Clone this repository

## Features

These playbooks are built to be run on the following operating systems:
- Ubuntu 12.04 LTS
- Amazon Linux

They have also been written in a way where you can use the same playbook to configure a running server, or build a custom AMI.

### Base configuration

The base configuration is gets a system ready for production. You can find the [base tasks here](https://github.com/awsanswers/noss-ansible/tree/master/playbooks/roles/base/tasks), but in summary it:
- installs some packages
 - Python with the latest Boto
 - AWS CLI
 - security packages including fail2ban
 - Emacs and Vim (no religion here)
- does some basic system hardening

## Projects

### Asgard

[Asgard](https://github.com/Netflix/asgard) is an application deployments and cloud management web interface for AWS. Before running the playbook, there are a few things we need to do:

1. Create an Asgard security group
 - Allow port 22 for SSH
 - Allow port 8080 for HTTP
1. If you don't already, create a new Key pair, and add it to your keychain or SSH agent so you don't need to specify it later:
```
$ ssh-add mykey.pem
```
1. Launch a new EC2 instance using the above Security Group and key pair
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

Once the playbook finished, you will have Asgard running inside Tomcat on your EC2 instance. You can access Asgard on port 8080. Example:

```
http://ec2-54-245-157-159.us-west-2.compute.amazonaws.com:8080/asgard/
```

## Feedback

If you have feedback, comments or suggestions, please feel free to contact Peter at AWS Answers, create an Issue, or submit a pull request.

## About AWS Answers

These playbooks were written by [Peter Sankauskas](https://twitter.com/pas256), founder of [AWS Answers](http://awsanswers.com/) - a consulting company focused on helping business get the most out of AWS. If you are looking for help with AWS, please [contact us](http://awsanswers.com/contact/). 