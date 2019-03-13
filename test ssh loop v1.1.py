import paramiko
import json
import re

filename = "users2.json"
myfile = open(filename, mode='w', encoding='utf-8') 

def jsonDefault(o):
    return o.decode('utf-8') #JSON serializable

def rev_var ():
    rev_var = stdout.read() + stderr.read()
    rev_var = rev_var.decode('utf-8')
    rev_var = str(rev_var)
    rev_var = rev_var.replace("\n","")
    servers[user]['revision'] = rev_var

def branch_var ():
    branch_var = stdout.read() + stderr.read()
    branch_var = branch_var.decode('utf-8') #remove b from print 
    branch_var = str(branch_var)
    branch_var = branch_var.replace("\n","") #remove \n from print
    servers[user]['branch'] = branch_var

servers = {
    'wiki' :
            {'host' : "192.168.30.191",
             'auth' : "Password",
             'vcs_type' : "",
             'user' : "wiki",
             'branch' : "",
             'revision' : ""
             },
    'ec2-user' :
            {'host' : "ec2-18-191-132-222.us-east-2.compute.amazonaws.com",
             'auth' : "Key",
             'key' : "test_aws.pem",
             'user' : "ec2-user",
             'vcs_type' : "",
             'branch' : "",
             'revision' : ""             
             },
    'ec2-user2' :
            {'host' : "ec2-18-216-192-91.us-east-2.compute.amazonaws.com",
             'auth' : "Key",
             'key' : "test_aws.pem",
             'user' : "ec2-user",
             'vcs_type' : "",
             'branch' : "",
             'revision' : ""
             }    
    }
        

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for user in servers:

    if servers[user]['auth'] == "Password":
        secret = "ChekoP2245%/%"
        client.connect(hostname=servers[user]['host'], username=servers[user]['user'], password=secret, port=22)
    else:
        
        client.connect(hostname=servers[user]['host'], username=servers[user]['user'], key_filename=servers[user]['key'], port=22)
        
    stdin, stdout, stderr = client.exec_command('find ~/repo2/ -name .git')
    data = stdout.read() + stderr.read()
    
    if re.search(r'.git', str(data)):
        servers[user]['vcs_type'] = "git"
        stdin, stdout, stderr = client.exec_command('cd ~/repo2/ && git symbolic-ref --short HEAD')
        branch_var ()
        stdin, stdout, stderr = client.exec_command('cd ~/repo2/ && git log --oneline -1')
        rev_var()
    else:
        servers[user]['vcs_type'] = " svn"
        stdin, stdout, stderr = client.exec_command('cd ~/svn_loc/svn && svn info | grep "Relative URL"')
        branch_var ()
        stdin, stdout, stderr = client.exec_command('cd ~/svn_loc/svn &&  svn info --show-item last-changed-revision')
        rev_var()
   
  
client.close()    
json.dump(servers, myfile, default = jsonDefault, indent=4, sort_keys=True)

myfile.close()

