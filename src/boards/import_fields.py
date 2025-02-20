import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_work_item_fields(organization, project, personal_access_token, input_file):
    # Read the exported work item fields from the JSON file
    with open(input_file, 'r') as f:
        work_item_fields = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create work item fields using the REST API
    try:
        for work_item_field in work_item_fields['value']:
            print(f'Creating work item field: {work_item_field["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/fields/{work_item_field["name"]}?api-version=6.0'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.put(url, headers=headers, data=json.dumps(work_item_field))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_work_item_field = response.json()
                print(f'New work item field created with ID: {new_work_item_field["id"]}')
            else:
                raise Exception(f'Failed to create work item field. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the work item fields: {e}')

def main():
    # Import the configuration variables
    import config_import as config
    
    # Call the function to import the work item fields
    import_work_item_fields(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'work_item_fields.json')
    )

if __name__ == '__main__':
    main()