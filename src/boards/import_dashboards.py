import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_dashboards(organization, project, personal_access_token, input_file):
    # Read the exported dashboards from the JSON file
    with open(input_file, 'r') as f:
        dashboards = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create dashboards using the REST API
    try:
        for dashboard in dashboards['dashboardEntries']:
            print(f'Creating dashboard: {dashboard["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/dashboard/dashboards?api-version=6.0-preview.2'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(dashboard))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_dashboard = response.json()
                print(f'New dashboard created with ID: {new_dashboard["id"]}')
            else:
                raise Exception(f'Failed to create dashboard. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the dashboards: {e}')

def main():
    # Import the configuration variables
    import config_import as config
    
    # Call the function to import the dashboards
    import_dashboards(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'dashboards.json')
    )

if __name__ == '__main__':
    main()