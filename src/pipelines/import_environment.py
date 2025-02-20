import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_environments(organization, project, personal_access_token, input_file):
    # Read the exported environments from the JSON file
    with open(input_file, 'r') as f:
        environments = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create environments using the REST API
    try:
        for environment in environments['value']:
            print(f'Creating environment: {environment["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/distributedtask/environments?api-version=6.0-preview.1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(environment))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_environment = response.json()
                print(f'New environment created with ID: {new_environment["id"]}')
            else:
                raise Exception(f'Failed to create environment. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the environments: {e}')

def main():
    # Import the configuration variables
    import src.boards.config_import as config
    
    # Call the function to import the environments
    import_environments(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'environments.json')
    )

if __name__ == '__main__':
    main()