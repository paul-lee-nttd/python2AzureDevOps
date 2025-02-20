import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_library(organization, project, personal_access_token, input_file):
    # Read the exported variable groups from the JSON file
    with open(input_file, 'r') as f:
        variable_groups = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create variable groups using the REST API
    try:
        for variable_group in variable_groups['value']:
            print(f'Creating variable group: {variable_group["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/distributedtask/variablegroups?api-version=6.0-preview.1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(variable_group))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_variable_group = response.json()
                print(f'New variable group created with ID: {new_variable_group["id"]}')
            else:
                raise Exception(f'Failed to create variable group. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the variable groups: {e}')

def main():
    # Import the configuration variables
    import src.boards.config_import as config
    
    # Call the function to import the variable groups
    import_library(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'variable_groups.json')
    )

if __name__ == '__main__':
    main()