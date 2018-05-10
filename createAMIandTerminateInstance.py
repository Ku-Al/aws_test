#!/usr/bin/env python3

import sys
import boto3
import awsconf
from datetime import datetime


if len(sys.argv) != 2:
    print("You need to specify a ID instance: {0} ID".format(sys.argv[0]))
    exit(0)

tagkey = awsconf.tagkey
tagvalue = awsconf.tagvalue
id = sys.argv[1]

#create data stamp
currentDatetime = datetime.now()
dateStamp = currentDatetime.strftime("%Y-%m-%d-%H:%M:%S")
newTag = id + "-" + dateStamp

ec2 = boto3.resource('ec2')
#for instance with id and if it is stopped
try:
    instance = ec2.Instance(id)
    if instance.state['Name'] == 'stopped':
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
        response = instance.terminate(DryRun=True)    
except: #error handling is skipped
    print('Something went wrong')   