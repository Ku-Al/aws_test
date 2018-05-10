#!/usr/bin/env python3

import boto3
import sys
import awsconf
from datetime import datetime, timedelta  

if len(sys.argv) != 2:
    print("You need to specify a timedelta in day: {0} timedelta".format(sys.argv[0]))
    exit(0)

tagkey = awsconf.tagkey
tagvalue = awsconf.tagvalue
region = awsconf.region
tDelta = int(sys.argv[1])

#сreate a date with which you to delete the images
today = datetime.now() + timedelta(days=1)
delta = timedelta(days=tDelta)  
delDate = today - delta

ec2 = boto3.resource('ec2',  region_name=region)
#need to use filters to highlight images
#because all the images come here
#but this is not indicated in the task
images = ec2.images.filter()
for image in images:
    createdDate = datetime.strptime(
        image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
    if createdDate < delDate:
         #image.deregister()
         print('Delete imageID', image.id, 'create date', createdDate, 'IDowner', image.owner_id)   