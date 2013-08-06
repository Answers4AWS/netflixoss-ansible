#!/bin/bash
#    Copyright 2013 Answers for AWS LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Pulls the latest code from Github
# This script is designed to be run as the user that owns the directory, which
# based on the playbook for Aminator is 'root'

# Stop execution on failure
set -e

echo "Pulling latest NetflixOSS-Ansible code from Github"
cd /usr/local/netflixoss-ansible
git pull origin master
