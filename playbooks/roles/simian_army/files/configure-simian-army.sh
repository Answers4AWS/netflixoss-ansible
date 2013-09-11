#!/bin/bash

region=`ec2metadata --availability-zone | sed 's/.$//'`

echo "Setting Simian Army region to $region"
perl -i -pe "s/us-west-1/$region/" /var/lib/tomcat7/webapps/simianarmy/WEB-INF/classes/client.properties


exists=`sdb ListDomains --region $region 2>&1 | grep 'SIMIAN_ARMY'`
if [ -n "$exists" ]; then
	echo "The SIMIAN_ARMY SimpleDB domain in $region already exists"
else
	echo "Creating the SIMIAN_ARMY SimpleDB domain in $region"
	sdb CreateDomain SIMIAN_ARMY --region $region
fi
