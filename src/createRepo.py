import requests
def createNewRepos(username, token, org_name, repo_name):
    # Replace with your GitHub username and Personal Access Token
    USERNAME = username
    TOKEN = token
    # Replace with the organization's name where you want to create the repository
    ORG_NAME = org_name
    # Set the repository name and optional description
    REPO_NAME = repo_name
    DESCRIPTION = 'This is a new repository created from CloudNC.'

    # Create a new GitHub repository in the organization
    url = f'https://api.github.com/orgs/{ORG_NAME}/repos'
    data = {
        'name': REPO_NAME,
        'description': DESCRIPTION,
        'private': True,  # Set to True if you want a private repository
    }
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Repository '{REPO_NAME}' created successfully in '{ORG_NAME}'!")
        # Optionally, you can clone the repository with HTTPS URL
        repo_url = response.json()['clone_url']
        #print(f"Clone this repository with: {repo_url}")
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(response.json())