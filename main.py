import json
import csv
import requests, json
from requests.auth import HTTPBasicAuth
from datetime import date

# https://gerrit.zebra.com/Documentation/rest-api.html

gerrit_url = input("Please enter Gerrit URL: ") #'http://z61sp-gitapp01a.zebra.lan:8080'
username = input("Username: ") #'sg6714'
password = input("Gerrit API Token: ") # https://gerrit.zebra.com/settings/#HTTPCredentials

def list_all_active_users():
    count = 0
    api_endpoint = f'{gerrit_url}/a/accounts/?q=is:active&start={count}&limit=500&o=DETAILS'
    response = requests.get(api_endpoint, auth=HTTPBasicAuth(username, password))
    print(f"URL: {api_endpoint}")

    if response.status_code == 200:
        content = json.loads((response.text).split("'")[1])
     
        print(content[-1])
        user_list = []
        while "_more_accounts" in content[-1]:
            count += len(content)
            user_list.append(content)
            print("More Users Found")
            api_endpoint = f'{gerrit_url}/a/accounts/?q=is:active&start={count}&limit=500&o=DETAILS'
            print(f"URL: {api_endpoint}")
            response = requests.get(api_endpoint, auth=HTTPBasicAuth(username, password))
            content = json.loads((response.text).split("'")[1][0])
            
            print(content[-1])
            
        print("No More Users")
        return user_list 
    else:
        print(f'Failed to retrieve users: {response.status_code} {response.reason}')
        return None

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_csv(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

 
def check_users(json_users, csv_users):
    results = []
    csv_user_set = {user['User Account']: user for user in csv_users}
    for json_user in json_users:
        try:
            username = json_user['username'].upper()
            if username in csv_user_set:
                json_user['status'] = "exists in both JSON and CSV."
            else:
                json_user['status'] = "does NOT exist in CSV."    
        except Exception as e:
            json_user['status'] = f"Unknown {e}"
        
        results.append(json_user)
    return results

def write_results_to_csv(results, file_path):
    fieldnames = ['_account_id', 'username', 'name', 'email','status','_more_accounts']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def compareToCSV():
    d = date.today()
    json_file_path = f"gerrit_users_{d}.json"
    csv_file_path = input("Path to Zebra Employee list as CSV: ")
    results_file_path = f"real_gerrit_users_{d}.csv"

    users = list_all_active_users()

    with open(json_file_path, "w") as file:
        json.dump(users, file)


    json_users = load_json(json_file_path)
    csv_users = load_csv(csv_file_path)

    results = check_users(json_users, csv_users)
    write_results_to_csv(results, results_file_path)

if __name__ == "__main__":
    compareToCSV()
