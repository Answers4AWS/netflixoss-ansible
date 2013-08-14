# Copyright 2013 Answers for AWS LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# A collection of variables, constants and functions that should be included in
# various scripts.
# Code adapted from: alestic-git

# Brand used in AMI name and description
brand="brand"

# Default size of AMI EBS volume
size=16 # GB

# Ubuntu release
codename=precise

# AMI name timestamp
now=$(date -u +%Y%m%d-%H%M)

copy_ami=1
# Command line options
while [ $# -gt 0 ]; do
  case $1 in
    --name)        brand=$2;     shift 2 ;;
    --size)        size=$2;      shift 2 ;;
    --codename)    codename=$2;  shift 2 ;;
    --now)         now=$2;       shift 2 ;;
    --no-copy)     copy_ami=0;   shift 1 ;;
    *)             echo "$0: Unrecognized option: $1" >&2; exit 1;
  esac
done


# Ubuntu release
case $codename in
  precise)    release=12.04     ;;
  quantal)    release=12.10     ;;
  raring)     release=13.04     ;;
  *)          echo "$0: Unrecognized codename: $codename" >&2; exit 1;
esac

# Architecture
if [ $(uname -m) = 'x86_64' ]; then
  arch=x86_64
  arch2=amd64
  ephemeraldev=/dev/sdb
else
  arch=i386
  arch2=i386
  ephemeraldev=/dev/sda2
fi

# AMI name and description
name="$brand-ubuntu-$release-$arch2-ebs-$now"
description="${brand^} on Ubuntu $release by AWS Answers"

# AMI details
imagename=$codename-server-cloudimg-$arch2
imageurl=http://uec-images.ubuntu.com/$codename/current/$imagename.tar.gz
amisurl=http://uec-images.ubuntu.com/query/$codename/server/released.current.txt
zoneurl=http://169.254.169.254/latest/meta-data/placement/availability-zone
zone=$(wget -qO- $zoneurl)
region=$(echo $zone | perl -pe 's/.$//')
akiid=$(wget -qO- $amisurl | egrep "ebs.$arch2.$region.*paravirtual" | cut -f9)

# Gets the AKI ID for a given region
function get_akiid() {
	local req_region=$1
	local akiid=$(wget -qO- $amisurl | egrep "ebs.$arch2.$req_region.*paravirtual" | cut -f9)
	echo $akiid
}

# Directories for image
image=/mnt/$imagename.img
thisImage=/mnt/$imagename.edit.img
imagedir=/mnt/$codename-cloudimg-$arch2
ebsimagedir=$imagedir-ebs

# Directories for Ansible
noss_ansible_dir=/usr/share/netflixoss-ansible
playbooks_dir=$noss_ansible_dir/playbooks
inventory_dir=$noss_ansible_dir/inventory

#export EC2_CERT=$(echo /tmp/cert.pem)
#export EC2_PRIVATE_KEY=$(echo /tmp/pk.pem)

# Runs a script as the ubuntu user in the image chroot environment
# Usage: imgRunScriptAsUbuntu SCRIPT_FILE_TO_EXECUTE [flags]
function imgRunScriptAsUbuntu() {	
	file=$1
	flags=$2
	run="$ebsimagedir/home/ubuntu/run-helper-cmd"
	
	if [ "$flags" != "rerun" ]; then
		sudo mv $file $run
		sudo chmod 755 $run
	fi
	sudo -E chroot $ebsimagedir sudo -u ubuntu -H -i ./run-helper-cmd
	if [ "$flags" != "nodelete" ]; then
		sudo rm -f $run
	fi
}



