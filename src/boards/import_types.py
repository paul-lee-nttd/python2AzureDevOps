import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_work_item_types(organization, project, personal_access_token, input_file):
    # Read the exported work item types from the JSON file
    with open(input_file, 'r') as f:
        work_item_types = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create work item types using the REST API
    try:
        for work_item_type in work_item_types['value']:
            print(f'Creating work item type: {work_item_type["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitemtypes/{work_item_type["name"]}?api-version=6.0'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.put(url, headers=headers, data=json.dumps(work_item_type))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_work_item_type = response.json()
                print(f'New work item type created with ID: {new_work_item_type["id"]}')
            else:
                raise Exception(f'Failed to create work item type. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the work item types: {e}')

def main():
    # Import the configuration variables
    import config_import as config
    
    # Call the function to import the work item types
    import_work_item_types(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'work_item_types.json')
    )

if __name__ == '__main__':
    main()