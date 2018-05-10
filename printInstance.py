#!/usr/bin/env python3

import boto3
import awsconf
import json
import pprint

ec2 = boto3.resource('ec2')
instances = ec2.instances.all()

aInstance = []

for instance in instances:
    if instance.state['Name'] == 'stopped':
        st = 'STOPPED'
    else:
        st = instance.state['Name']
    dt = str(instance.launch_time)
    aInstance.append({
        'InstanceID' : instance.id,
        'Architecture' : instance.architecture,
        'Type': instance.instance_type,
        'State': st,
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': dt,
        'Security Group' : instance.security_groups,
        'Tags': instance.tags
     })

jInstance = json.dumps(aInstance)    

#print(json.dumps(json.loads(jInstance), sort_keys=False))
#print(json.dumps(json.loads(jInstance), sort_keys=False, indent=5, security_ascii=True))
#pprint.pprint(jInstance, depth=3, width=80)
print(json.dumps(json.loads(jInstance), sort_keys=False, indent=5, separators=(',',':')))

