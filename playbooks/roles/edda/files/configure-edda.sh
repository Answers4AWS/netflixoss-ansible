#!/bin/bash

region=`ec2metadata --availability-zone | sed 's/.$//'`

echo "Setting Edda region to $region"
perl -i -pe "s/us-east-1/$region/" /var/lib/tomcat7/webapps/edda/WEB-INF/classes/edda.properties

