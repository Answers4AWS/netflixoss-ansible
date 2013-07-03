# NetflixOSS Ansible Playbooks

[Ansible](https://github.com/ansible/ansible/) is a configuration management system that is [very simple to learn](http://www.ansibleworks.com/docs/gettingstarted.html) and use.

This project is a set of Ansible Playbooks to configure instances to run some of the [NetflixOSS](http://netflix.github.io/) projects.

- [Asgard](#Asgard)
- Aminator (coming soon)
- Edda (coming soon)
- Eureka (coming soon)
- Ice (coming soon)
- Simian Army (coming soon)

## Features

These playbooks are built to be run on:
- Ubuntu 12.04 LTS
- Amazon Linux.

They have also been written in a way where you can use the same playbook to configure a running server, or build a custom AMI.

### Base configuration

The base configuration is gets a system ready for production. You can find the [base tasks here](#), but in summary it:
- installs some packages
-- Python with the latest Boto
-- AWS CLI
-- security packages including fail2ban
-- Emacs and Vim (no religion here)
- does some basic system hardening

## Projects

### Asgard

[Asgard](https://github.com/Netflix/asgard) is an application deployments and cloud management web interface for AWS. To run the playbook, 
