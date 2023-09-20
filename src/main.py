import json
import requests
import subprocess
import os
from migrate import migrate_repositories 

#clone repo from ghes
file_path = os.environ.get('FILE_PATH')
clone_directory = os.environ.get('CLONE_DIRECTORY')
select_organizations = os.environ.get('SELECT_ORGANIZATIONS')  
# 'org/repo'
ignore_repos = os.environ.get('IGNORE_REPOS')
#ignore_repos = [ ]

#create repo in ghec
org_name_migrate = os.environ.get('ORG_NAME_MIGRATE')
username = os.environ.get('USERNAME')
old_repo_token = os.environ.get('OLD_REPO_TOKEN')
token = os.environ.get('TOKEN')


f = open(file_path)
data = json.load(f)
json_string = json.dumps(data)

        
data = json.loads(json_string)

print("--------- PLAN -----------")
count = 0
repos = []
for org in data["organizations"]:
    org_name = org["name"]
    if org_name in select_organizations:
        for repo in org["repos"]:
            repo_name = repo["name"]
            repo_state = repo["state"]
            repo_check = f'{org_name}/{repo_name}'
            if repo_check not in ignore_repos:     
                if repo_state.lower() == 'true':
                     count = count+0
                     print(f'{org_name}/{repo_name} exist already')
                elif repo_state.lower() == 'false': 
                    count = count+1
                    print(f'Add {org_name}/{repo_name}')
                    repos.append(f'{repo_name}')
                
                continue
    count = count+0
    
    
        
print('\t')
print(f'Plan: {count} to add')
print('\t')

if count>0:
    print('Do you want to perform these actions?')
    ans = input(' Enter a value: ')
   
    if ans.lower() == 'yes': 
        print('----------------------------')
        migrate_repositories(file_path,username,old_repo_token,token,data,org_name_migrate, select_organizations, clone_directory,repos,ignore_repos)

    else:
        print('--------- END -----------')
else:
    print('--------- END -----------')


