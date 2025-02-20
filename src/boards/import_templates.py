import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_work_item_templates(organization, project, personal_access_token, input_file):
    # Read the exported work item templates from the JSON file
    with open(input_file, 'r') as f:
        work_item_templates = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create work item templates using the REST API
    try:
        for work_item_template in work_item_templates['value']:
            print(f'Creating work item template: {work_item_template["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/templates/{work_item_template["id"]}?api-version=6.0'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.put(url, headers=headers, data=json.dumps(work_item_template))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_work_item_template = response.json()
                print(f'New work item template created with ID: {new_work_item_template["id"]}')
            else:
                raise Exception(f'Failed to create work item template. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the work item templates: {e}')

def main():
    # Import the configuration variables
    import config_import as config
    
    # Call the function to import the work item templates
    import_work_item_templates(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'work_item_templates.json')
    )

if __name__ == '__main__':
    main()