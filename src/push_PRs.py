import requests
import json

def push_PRs(org_name , token , repo_name , Json_File):
    with open(Json_File,"r") as PRs:
        data = json.load(PRs)

    for index in range(len(data)):
        # Create a new pull request on the target repository
        target_pr_url = f"https://api.github.com/repos/{org_name}/{repo_name}/pulls"

        headers = {
            'Accept'        : 'application/vnd.github+json', 
            'Authorization' : 'Bearer '+ token,  
            'X-GitHub-Api-Version': '2022-11-28'  
        }
        pr_data = {
            "title" :   data[index]['title'],
            "body"  :   data[index]['body'],
            "head"  :   data[index]['head']['ref'],
            "base"  :   data[index]['base']['ref']
            }
        response = requests.post(target_pr_url, headers=headers, json=pr_data)

        if response.status_code == 201:
            print('Pull request created successfully.')
            print('Pull request URL:', response.json().get('html_url'))
        else:
            print('Failed to create the pull request.')
            print('Status code:', response.status_code)
            print('Response content:', response.text)