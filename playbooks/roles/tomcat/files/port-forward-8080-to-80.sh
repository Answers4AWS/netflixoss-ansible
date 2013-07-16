#!/bin/bash

set -e

echo "Forwarding port 8080 to 80 for Tomcat"
iptables -t nat -A OUTPUT     -d localhost                  -p tcp --dport 80 -j REDIRECT --to-ports 8080
iptables -t nat -A OUTPUT     -d `ec2metadata --local-ipv4` -p tcp --dport 80 -j REDIRECT --to-ports 8080
iptables -t nat -A PREROUTING -d `ec2metadata --local-ipv4` -p tcp --dport 80 -j REDIRECT --to-ports 8080
