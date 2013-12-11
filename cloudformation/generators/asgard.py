#!/usr/bin/python

# Asgard CloudFormation template

from troposphere import Template, Parameter, Join, Ref, FindInMap, Output, GetAtt
import troposphere.ec2 as ec2


template = Template()
template.add_description('NetflixOSS Asgard 1.3.1 - Template by Answers for AWS')

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
    "us-east-1":      {"AMI": "ami-4d755a24"},
    "us-west-1":      {"AMI": "ami-0c251549"},
    "us-west-2":      {"AMI": "ami-d0ceabe0"},
    "eu-west-1":      {"AMI": "ami-44bf5633"},
    "sa-east-1":      {"AMI": "ami-9394358e"},
    "ap-southeast-1": {"AMI": "ami-fea1f5ac"},
    "ap-southeast-2": {"AMI": "ami-d3a33ce9"},
    "ap-northeast-1": {"AMI": "ami-616e0d60"}
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
    SecurityGroups=[Ref(sg)]
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
