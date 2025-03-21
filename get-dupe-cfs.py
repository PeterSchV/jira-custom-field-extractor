import sys
import requests
import csv
from requests.auth import HTTPBasicAuth

# Function to get Jira credentials from user input
def get_credentials():
    jira_url = input("Enter your Jira instance URL (e.g., https://your-jira-instance.atlassian.net): ")
    username = input("Enter your Jira username or email address: ")
    api_token = input("Enter your Jira API token: ")
    return jira_url, username, api_token

# Function to get Jira credentials from command-line arguments
def get_credentials_from_args():
    if len(sys.argv) != 4:
        print("Usage: python script.py <jira_url> <username> <api_token>")
        sys.exit(1)

    return sys.argv[1], sys.argv[2], sys.argv[3]

# Jira Cloud details
jira_url, username, api_token = get_credentials_from_args()
api_url_custom_fields = "{}/rest/api/3/field/search".format(jira_url)
api_url_search = "{}/rest/api/3/search".format(jira_url)

# Set up authentication
auth = HTTPBasicAuth(username, api_token)

# Additional parameters for the API call to get custom fields
params_custom_fields = {'expand': 'key,lastUsed,screensCount,isLocked,searcherKey', 'startAt': 0, 'maxResults': 100}

# Initialize variables
all_custom_fields = []

# Make requests until all custom fields are retrieved
while True:
    response_custom_fields = requests.get(api_url_custom_fields, auth=auth, params=params_custom_fields)
    if response_custom_fields.status_code == 200:
        custom_fields = response_custom_fields.json()['values']
        if not custom_fields:
            break  # No more results, exit the loop

        all_custom_fields.extend(custom_fields)
        params_custom_fields['startAt'] += len(custom_fields)
    else:
        print("Failed to retrieve custom fields. Status code: {}".format(response_custom_fields.status_code))
        print(response_custom_fields.text)
        sys.exit(1)  # Exit the script on error

# Specify the CSV file name
csv_file_name = "custom_fields_details.csv"

# Write data to CSV file using the standard csv module
with open(csv_file_name, 'w', encoding='utf-8', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(['ID', 'Name', 'Type', 'Key', 'LastUsed', 'ScreensCount', 'IsLocked', 'SearcherKey', 'Used in Issues'])

    # Write data
    for field in all_custom_fields:
        field_id = field.get('id', 'N/A')
        field_name = field.get('name', 'N/A')
        field_type = field.get('schema', {}).get('type', 'N/A')

        # Additional fields from the 'expand' parameter
        key = field.get('key', 'N/A')
        last_used = field.get('lastUsed', 'N/A')
        screens_count = field.get('screensCount', 'N/A')
        is_locked = field.get('isLocked', 'N/A')
        searcher_key = field.get('searcherKey', 'N/A')

        # Make API request to get the count of issues where the field is not empty
        jql_field_id = field_id.split('_')[-1] if '_' in field_id else field_id
        jql = '{} is not empty'.format('cf[{}]'.format(jql_field_id) if '_' in field_id else field_id)
        params_search = {'jql': jql, 'fields': 'key', 'maxResults': 1}
        response_search = requests.get(api_url_search, auth=auth, params=params_search)

        if response_search.status_code == 200:
            total_issues = response_search.json().get('total', 0)
        elif response_search.status_code == 400:
            total_issues = 'N/A'
        else:
            print("Failed to retrieve issue count for custom field {}. Status code: {}".format(field_name, response_search.status_code))
            total_issues = 'N/A'

        # Ensure Unicode characters are correctly handled
        row_data = [
            field_id,
            field_name,
            field_type,
            key,
            last_used,
            screens_count,
            is_locked,
            searcher_key,
            total_issues
        ]

        # Write data to CSV using the standard csv module
        csv_writer.writerow(row_data)

print("CSV file '{}' created successfully.".format(csv_file_name))
