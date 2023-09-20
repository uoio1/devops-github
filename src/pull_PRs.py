import requests
import json

def pull_PRs(org_name , token , repo_name):
    api_url = f'https://dssgit.se.scb.co.th/api/v3/repos/{org_name}/{repo_name}/pulls'

    response = requests.get(api_url, headers={'Authorization': f'token {token}'}, verify=False)

    if response.status_code == 200:
        pull_requests = response.json()

        with open('src/'+repo_name+'.json', 'w') as json_file:
            json.dump(pull_requests, json_file, indent=2)
        
        print("บันทึกข้อมูล Pull Request ลงในไฟล์ json สำเร็จ")
    else:
        print(f"การร้องขอล้มเหลว รหัสสถานะ: {response.status_code}")