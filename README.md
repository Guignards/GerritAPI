# GerritAPI
https://gerrit.zebra.com/Documentation/rest-api.html

# Features

Currently only good for downloading a list of active users from Gerrit and comparing it to a list of Zebra employees.
In the future the plan is to abstract each API call into a python function, plus additional features as requested


## List_Zebra_Users

1. Clone the Repo
2. Ensure you have the list of zebra employees in the same directory as repo `zebra_employees_latest.csv`
3. Make sure you have created an HTTP Credential from within Gerrit
4. Run the tool `python main.py`

A sample [csv extracted in Sept 2024](./zebra_employees_092024.csv) has been provided

# Gerrit Users Comparison Script

This Python script is designed to interact with a Gerrit server to retrieve a list of active users and compare it against a provided CSV file of users. The script outputs the results to a new CSV file indicating which users exist in both sources.

## Prerequisites

- Python 3.x
- The following Python libraries:
  - requests
  - json
  - csv

You can install the required library using pip:

pip install requests

## Usage

1. Clone or download this repository to your local machine.

2. Navigate to the directory containing the script.

3. Run the script by executing the following command:

   python script_name.py

   Replace `script_name.py` with the actual name of your Python script.

4. When prompted, provide the following information:
   - Gerrit URL: The base URL of your Gerrit server (e.g., http://z61sp-gitapp01a.zebra.lan:8080).
   - Username: Your Gerrit username.
   - Gerrit API Token: Your Gerrit HTTP API token. You can find it in your Gerrit settings under HTTP Credentials.
   - Path to Zebra Employee list as CSV: The file path to the CSV file containing the list of users you want to compare against.

5. The script will perform the following actions:
   - Retrieve a list of all active users from the Gerrit server.
   - Save this list to a JSON file named `gerrit_users_<date>.json`.
   - Load the provided CSV file for comparison.
   - Compare the users in the JSON file against the CSV file.
   - Save the comparison results to a CSV file named `real_gerrit_users_<date>.csv`.

## Output

- `gerrit_users_<date>.json`: Contains the list of active users from the Gerrit server.
- `real_gerrit_users_<date>.csv`: Contains the comparison results, indicating which users exist in both the JSON and CSV files.

## Notes

- Ensure your Gerrit server URL and credentials are correct to avoid authentication errors.
- The CSV file should have a column named 'User Account' containing the usernames.

## Troubleshooting

- If you encounter a "Failed to retrieve users" error, check your network connection and verify the Gerrit URL and credentials.
- Ensure the CSV file is correctly formatted with the required column for comparison.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
