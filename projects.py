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

query = f"/a/projects/?d"
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

    # Open a CSV file for writing
    with open('projects.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Project Name', 'Parent Project', 'Insertions', 'Commit Subject', 'Commit Date'])

        # Iterate over each change item in the data
        for project in json_data:
            project_name = project.key().split('/')[-1]
            parent_project = project.key().split('/')[0]
            project_id = project.get('id')
            description = project.get('description')
            # Write the data row
            writer.writerow([project_id, parent_project, project_name,description])

    print("CSV file 'changes.csv' created successfully.")
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)