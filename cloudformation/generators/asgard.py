#!/usr/bin/python

# Asgard CloudFormation template

from troposphere import Template, Parameter, Join, Ref, FindInMap, Output, GetAtt
import troposphere.ec2 as ec2


template = Template()
template.add_description('NetflixOSS Asgard 1.4.1 - Template by Answers for AWS')

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

java_license = template.add_parameter(Parameter(
    "OracleJava",
    Description = "Type 'yes' to accept the Oracle Java license found here: http://www.oracle.com/technetwork/java/javase/terms/license/index.html",
    Type = "String",
    AllowedValues = [ "yes", "YES", "'yes'", "Yes" ],
    ConstraintDescription = "Type 'yes' to agree to the license"
))

template.add_mapping('RegionMap', {
    "us-east-1":      {"AMI": "ami-7724131e"},
    "us-west-1":      {"AMI": "ami-3cdcef79"},
    "us-west-2":      {"AMI": "ami-a86f0998"},
    "eu-west-1":      {"AMI": "ami-a8e10bdf"},
    "sa-east-1":      {"AMI": "ami-4bf85856"},
    "ap-southeast-1": {"AMI": "ami-149fc846"},
    "ap-southeast-2": {"AMI": "ami-e5d749df"},
    "ap-northeast-1": {"AMI": "ami-8f39568e"}
})

# Create a security group
sg = template.add_resource(ec2.SecurityGroup('AsgardSecurityGroup'))
sg.GroupDescription = 'Access to Asgard Instance'
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

ec2_instance = template.add_resource(ec2.Instance(
    "AsgardInstance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType=Ref(instance_type),
    KeyName=Ref(keyname),
    SecurityGroups=[Ref(sg)],
    Tags = [
        {'Key': 'Name', 'Value': 'Asgard'}
    ]
))

template.add_output([
    Output(
        "PublicIP",
        Description="Public IP address of the Asgard instance",
        Value=GetAtt(ec2_instance, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the Asgard instance",
        Value=GetAtt(ec2_instance, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the Asgard instance",
        Value=GetAtt(ec2_instance, "PublicDnsName"),
    )
])

print template.to_json()


#import requests
#myip_response = requests.get(url='http://icanhazip.com')
#myip = myip_response.text
#
## Create new CloudFormation Stack from template
#from boto import cloudformation
#try:
#    conn = cloudformation.connect_to_region('us-west-2')
#    stack_id = conn.create_stack(
#        'Asgard', 
#        template_body=template.to_json(), 
#        parameters=[
#            ('KeyPairName', 'answersforaws'),
#            ('YourIpAddress', myip)
#        ]
#    )
#    print 'Created ' + stack_id
#except Exception, e:
#    print e
#    print e.message
