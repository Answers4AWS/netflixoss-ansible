#!/bin/bash

region=`ec2metadata --availability-zone | sed 's/.$//'`

echo "Setting Edda region to $region"
perl -i -pe "s/^edda\.region\=.*/edda.region=$region/" /var/lib/tomcat7/webapps/edda/WEB-INF/classes/edda.properties

