import boto3
import json
import urllib3
import paramiko
import sys
import time
from datetime import datetime, timedelta

import awsconf

hosts = awsconf.hosts
pKey = awsconf.pKey
user = awsconf.user
tagkey = awsconf.tagkey
tagvalue = awsconf.tagvalue
region = awsconf.region


def createAMI(tagkey, tagvalue):
    
    ec2 = boto3.resource('ec2')
    #for stopped instance 
    instances = ec2.instances.filter(Filters=[
            {
                'Name': 'tag:' + tagkey,
                'Values': [tagvalue]
            }
        ]
    )
    for instance in instances:
        if instance.state['Name'] == 'stopped':
            #create data stamp
            currentDatetime = datetime.now()
            dateStamp = currentDatetime.strftime("%Y-%m-%d-%H:%M:%S")
            newTag = instance.id + "-" + dateStamp
            #create image
            idAMI = instance.create_image(
                Name = 'Kubov_Alex',
                NoReboot = True,
                DryRun = False,
                Description= newTag
            )
            print("Created AMI id ", idAMI)
            #create for new image tag with data stamp
            image = ec2.Image(idAMI.id)
            tag = image.create_tags(
            DryRun = False,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': newTag
                },
            ]
            )
            #terminate instance after make image
            #response = instance.terminate(DryRun=True)
            print("Terminate instance with ID", instance.id)


def checkHostHttp(host):
    http = urllib3.PoolManager()
    try:
        http.request('GET', host, timeout=1)
        print("Host ", host, " is available by http")
    except urllib3.exceptions.HTTPError as err:
        print("!!! Host ", host, " is not available by http")


def checkHostSsh(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privKey = paramiko.RSAKey.from_private_key_file(pKey)
    try:
        ff = ssh.connect(host, username = user, pkey = privKey, timeout = 5)
        time.sleep(1)
        ssh.exec_command('uname -n\n')
        time.sleep(1)
        ssh.close()
        print("Host", host, "is available by tcp")
    except :
        print("!!! Host", host, "is not available by tcp")


def clearOlderAMI(region, day, tag):
    
    today = datetime.now() + timedelta(days=1)
    delta = timedelta(days = day)
    delDate = today - delta
    ec2 = boto3.resource('ec2', region_name=region)
    #filter by owner, but not in this account
    #images = ec2.images.filter(Owners=['self'])
    vl = tag + '*'
    filters = [{'Name':'name', 'Values':[vl]}]
    images = ec2.images.filter(Filters=filters).all()
    for image in images:
        createdDate = datetime.strptime(
                    image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
        if createdDate < delDate:
        #image.deregister()
            print('Delete imageID', image.id, 'create date', createdDate, 'IDowner', image.owner_id)   


def printInstance(tagkey, tagvalue):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[
            {
                'Name': 'tag:' + tagkey,
                'Values': [tagvalue]
            }
        ]
    )

    aInstance = []

    for instance in instances:
        #add the necessary attributes to the list
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
    #make json
    jInstance = json.dumps(aInstance)
    #print json
    print('\nPrint all instance')
    print(json.dumps(json.loads(jInstance), sort_keys=False, indent=5, separators=(',',':')))



for host in hosts:
    checkHostHttp(host)
    checkHostSsh(host)
createAMI(tagkey, tagvalue)
clearOlderAMI(region, 7, 'i-0a9b37fd502f72bf2')
printInstance(tagkey, tagvalue)
