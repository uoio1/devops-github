import requests
import os

github_enterprise_url = os.environ.get('GITHUB_ENTERPRISE_URL')
access_token = os.environ.get('ACCESS_TOKEN')
headers = {'Authorization': f'Bearer {access_token}'}

user_url = f"{github_enterprise_url}/user"

# Create a dictionary to store the data
my_json = {'organizations': []}

response = requests.get(user_url, headers=headers, verify=False)
if response.status_code == 200:
    user_data = response.json()
    user_login = user_data['login']

    orgs_url = f"{github_enterprise_url}/user/orgs"
    orgs_response = requests.get(orgs_url, headers=headers, verify=False)

    if orgs_response.status_code == 200:
        orgs_data = orgs_response.json()
        for org in orgs_data:
            org_name = org['login']
            organization = {'name': org_name, 'repos': []}

            repos_url = f"{github_enterprise_url}/orgs/{org_name}/repos"
            repos_response = requests.get(repos_url, headers=headers, verify=False)

            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                for repo in repos_data:
                    repo_name = repo['name']
                    repo_ssh_url = repo['ssh_url']
                    repository = {'name': repo_name, 'ssh_url': repo_ssh_url, 'state': 'False'}
                    organization['repos'].append(repository)
            else:
                print(f"Error fetching repos from Organization: {org_name}")

            my_json['organizations'].append(organization)
    else:
        print("Error fetching organizations")
else:
    print("Error fetching user data")

# Print the JSON data
import json
print(json.dumps(my_json, indent=4))
