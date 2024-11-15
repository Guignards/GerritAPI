import requests
from requests.auth import HTTPBasicAuth
import csv, os, json


# Define the API endpoint
# &o=CURRENT_REVISION&o=CURRENT_COMMIT&o=CURRENT_FILES&o=DOWNLOAD_COMMANDS HTTP/1.0"
count = 0
gerrit_url = f"http://z61sp-gitapp01a.zebra.lan:8080"

# Export Credentials to Environment Vars
# set GERRIT_USERNAME=your_username
# set GERRIT_PASSWORD=your_password

username = input("Username: ") #'sg6714'
password = input("Gerrit API Token: ") # https://gerrit.zebra.com/settings/#HTTPCredentials

query = f"/a/changes/?q=is:open&start={count}&limit=500&o=ALL_COMMITS"
# Authenticate
response = requests.get(gerrit_url+query, auth=HTTPBasicAuth(username, password))

def clean_json(content):
    data = content.replace(")]}'\n", "")
    data = data.replace('\n', '')
    data = data.replace("'", "")
    data = data.replace('\\"', '')
    return json.loads(data)


# Check if the request was successful
if response.status_code == 200:
    
    # Handle the response content
    json_data = clean_json(response.text)

    change_list = []
    while json_data[-1].get('_more_changes'):
        count += len(json_data)
        change_list.append(json_data)
        query = f"/a/changes/?q=is:open&start={count}&limit=500&o=ALL_COMMITS"
        print(f"More Changes Found: {len(json_data)}: {count} \n {json_data[-1]}")
        response = requests.get(gerrit_url+query, auth=HTTPBasicAuth(username, password))
        json_data = clean_json(response.text)
    print(f"No More: {len(json_data)}: {count} \n {json_data[-1]}")


    # Open a CSV file for writing
    with open('changes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Project Name', 'Parent Project', 'Insertions', 'Commit Subject', 'Commit Date'])

        # Iterate over each change item in the data
        for changes in change_list:
            for change in changes:
                project_name = change.get('project').split('/')[-1]
                parent_project = change.get('project').split('/')[0]
                commit_subject = change.get('subject')
                commit_date = change.get('updated')
                insertions = change.get('insertions')
                # Write the data row
                writer.writerow([project_name, parent_project, insertions, commit_subject, commit_date])

    print("CSV file 'changes.csv' created successfully.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)