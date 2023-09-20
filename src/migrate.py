import subprocess
import os
from createRepo import createNewRepos
from pushRepo import push_repository
from  pull_PRs import pull_PRs
from push_PRs import push_PRs
import json


def migrate_repositories(file_path,username,old_repo_token,token,data,org_name_migrate, select_organizations, clone_directory,repos,ignore_repos):
    count_success = 0
    count_failed = 0
    for org in data["organizations"]:
        # print(f"Organization Name: {org['name']}")
        org_name = org["name"]
        
        if org_name in select_organizations:
            for repo in org["repos"]:
                repo_name = repo["name"]
                repo_check = f'{org_name}/{repo_name}'
                if repo_check not in ignore_repos: 
                    if repo_name in repos:
                        print(f"Organization Name: {org['name']}")
                        repo_url = repo["ssh_url"]
                        repo_directory = f"{clone_directory}/{org_name}-{repo_name}"
        
                        # Run the git clone command
                        clone_command = ["git", "clone", "--mirror", repo_url, repo_directory]
                        
                        if not os.path.exists(os.path.join(repo_directory)):
                            try:
                                print("... CLONE ...")
                                subprocess.check_call(clone_command)
                                print(f"Cloned repository '{repo_name}' successfully.")
                                pull_PRs(org_name,old_repo_token,repo_name)
                                print("export pr successfully")

                                repo_name_create = org_name+"-"+repo_name
                                print("... CREATE ...")
                                createNewRepos(username, token, org_name_migrate, repo_name_create)
                                print("... PUSH ...")
                                push_status = push_repository(repo_name_create, org_name_migrate, clone_directory)
                                push_PRs(org_name_migrate,token,repo_name_create, repo_name+'json')
                                print("import pr successfully")

                                file_path = file_path
                                for org in data["organizations"]:
                                    if org_name in select_organizations:
                                        for repo in org["repos"]:
                                            repo_name = repo["name"]
                                            repo_check = f'{org_name}/{repo_name}'
                                            if repo_check not in ignore_repos: 
                                                if repo_name in repos and push_status is True:
                                                    repo["state"] = "True"
                                            else:
                                                repo["state"] = "False"
            
                                    # เขียน JSON กลับไปยังไฟล์ (หรือทำอย่างอื่นตามที่คุณต้องการ)
                                    with open(file_path, 'w') as file:
                                         json.dump(data, file, indent=4) 
                                count_success = count_success+1
            
                            except subprocess.CalledProcessError as e:
                                print(f"Error cloning repository '{repo_name}': {e}")
                                count_failed = count_failed+1
                        else:
                            print("... CLONE ...")
                            print("Skip")
                            # pull_PRs(org_name,old_repo_token,repo_name)
                            # print("export pr successfully")
                            repo_name_create = org_name+"-"+repo_name
                            print("... CREATE ...")
                            createNewRepos(username, token, org_name_migrate, repo_name_create)
                            print("... PUSH ...")
                            push_status = push_repository(repo_name_create, org_name_migrate, clone_directory)
                            push_PRs(org_name_migrate,token,repo_name_create,'src/'+repo_name+'.json')
                            print("import pr successfully")
                            file_path = file_path
                            for org in data["organizations"]:
                                    if org_name in select_organizations:
                                        for repo in org["repos"]:
                                            repo_name = repo["name"]
                                            repo_check = f'{org_name}/{repo_name}'
                                            if repo_check not in ignore_repos: 
                                                if repo_name in repos and push_status is True:
                                                    repo["state"] = "True"
                                            else:
                                                repo["state"] = "False"
            
                            # เขียน JSON กลับไปยังไฟล์ (หรือทำอย่างอื่นตามที่คุณต้องการ)
                            with open(file_path, 'w') as file:
                                json.dump(data, file, indent=4) 
                                count_success = count_success+1
            
                        print('***')
                    
                    # continue
                    else:
                        print(f'{repo_name} exist already')
                        print('***')
    print('\n')                
    print('----------------------------')
    print(f'{count_success} success, {count_failed} failed')
    
    
