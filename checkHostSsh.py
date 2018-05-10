#!/usr/bin/env python3

import paramiko
import boto3
import time
import awsconf

hosts = awsconf.hosts
pKey = awsconf.pKey
user = awsconf.user

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
        return True
    except :
        return False
    
for host in hosts:
    if checkHostSsh(host): 
        print("Host", host, "is available by ssh")
    else:
        print("!!! Host", host, "is not available by ssh")