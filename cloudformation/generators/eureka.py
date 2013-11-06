#!/usr/bin/python

# Eureka CloudFormation template

from troposphere import Template, Parameter, Join, Ref, FindInMap, Output, GetAtt, GetAZs
import troposphere.ec2 as ec2
import troposphere.autoscaling as auto
from troposphere.iam import Role, Policy, InstanceProfile, PolicyType

template = Template()
template.add_description('NetflixOSS Eureka 1.1.121 - Template by Answers for AWS')

keyname = template.add_parameter(Parameter(
    "KeyPairName",
    Description = "Name of an existing EC2 KeyPair to enable SSH access to the instance",
    Type = "String",
    MinLength = "1",
    MaxLength = "64",
    AllowedPattern = "[-_ a-zA-Z0-9]*",
    ConstraintDescription = "can contain only alphanumeric characters, spaces, dashes and underscores."
))

ip_address = template.add_parameter(Parameter(
    "YourIpAddress",
    Description = "Your IP address",
    Type = "String",
))

instance_type = template.add_parameter(Parameter(
    "InstanceType",
    Description = "EC2 instance type to launch for Application servers",
    Type = "String",
    Default = "m1.medium",
    AllowedValues = [ "m1.medium", "m1.large", "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge", "m3.xlarge", "m3.2xlarge", "c1.medium", "c1.xlarge", "cg1.4xlarge" ],
    ConstraintDescription = "must be a valid EC2 instance type"
))


template.add_mapping('RegionMap', {
    "us-east-1":      {"AMI": "ami-99247ff0"},
    "us-west-1":      {"AMI": "ami-ae0234eb"},
    "us-west-2":      {"AMI": "ami-f40991c4"},
    "eu-west-1":      {"AMI": "ami-c1c527b6"},
    "sa-east-1":      {"AMI": "ami-df45e3c2"},
    "ap-southeast-1": {"AMI": "ami-2a9cc978"},
    "ap-southeast-2": {"AMI": "ami-1970ec23"},
    "ap-northeast-1": {"AMI": "ami-91d3b690"}
})

role = template.add_resource(Role('EurekaRole',
    AssumeRolePolicyDocument = {
        "Statement": [{
            "Effect": "Allow",
            "Principal":{
                "Service":["ec2.amazonaws.com"]
            },
            "Action":["sts:AssumeRole"]
        }]
    },
    Path = "/",
    Policies = [
        Policy(
            PolicyName = "EurekaPolicy",
            PolicyDocument = {
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": [
                    "autoscaling:DescribeAutoScalingGroups",
                    "ec2:AssociateAddress",
                    "ec2:DisassociateAddress"

                  ],
                  "Resource": "*"
                }
              ]
            }
        )
    ]
))

instance_profile = template.add_resource(InstanceProfile(
    "EurekaInstanceProfile",
     Path = "/",
     Roles = [Ref(role)]
))
 

# Create a security group
sg = template.add_resource(ec2.SecurityGroup('EurekaSecurityGroup'))
sg.GroupDescription = 'Access to Eureka'
sg.SecurityGroupIngress = [
    ec2.SecurityGroupRule(
        IpProtocol = 'tcp',
        FromPort = '22',
        ToPort = '22',
        CidrIp = '0.0.0.0/0'
    ),
    ec2.SecurityGroupRule(
        IpProtocol = 'tcp',
        FromPort = '80',
        ToPort = '80',
        CidrIp = Join('/', [Ref(ip_address), "32"])
    )
]


# Launch config
launch_config = template.add_resource(auto.LaunchConfiguration('MyLaunchConfig',
    ImageId = FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType  = Ref(instance_type),
    KeyName = Ref(keyname),
    SecurityGroups = [Ref(sg)],
    IamInstanceProfile = Ref(instance_profile)
))

# Autoscaling Group
asg = template.add_resource(auto.AutoScalingGroup('MyASG',
    AvailabilityZones = GetAZs(''),
    Cooldown = 120,
    LaunchConfigurationName = Ref(launch_config),
    MaxSize = '1',
    MinSize = '1',
    Tags = [
        {'Key': 'Name',
        'Value': 'Eureka',
        'PropagateAtLaunch': 'true'}
    ]
))

# Add generic output
template.add_output(Output(
    'Eureka',
    Description = 'Please go to the EC2 page in the AWS Web Console',
    Value = 'Look for the instance named Eureka and assign it an Elastic IP'
))

# Print template
print(template.to_json())

#
#import requests
#myip_response = requests.get(url='http://icanhazip.com')
#myip = myip_response.text
#
## Create new CloudFormation Stack from template
#from boto import cloudformation
#try:
#    conn = cloudformation.connect_to_region('us-east-1')
#    stack_id = conn.create_stack(
#        'Eureka', 
#        template_body=template.to_json(), 
#        parameters=[
#            ('KeyPairName', 'answersforaws'),
#            ('YourIpAddress', myip),
#        ]
#    )
#    print 'Created ' + stack_id
#except Exception, e:
#    print e
#    print e.message
