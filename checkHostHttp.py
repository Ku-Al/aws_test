#!/usr/bin/env python3

import urllib3
import boto3
import awsconf

hosts = awsconf.hosts

def checkHostHttp(host):
    http = urllib3.PoolManager()
    try:
        http.request('GET', host, timeout=1)
        return True
    except urllib3.exceptions.HTTPError as err: 
        return False

for host in hosts:
    if checkHostHttp(host): 
        print("Host ", host, " is available by http")
    else:
        print("!!! Host ", host, " is not available by http")
    
