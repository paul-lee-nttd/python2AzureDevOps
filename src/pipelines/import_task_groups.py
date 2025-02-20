import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_task_groups(organization, project, personal_access_token, input_file):
    # Read the exported task groups from the JSON file
    with open(input_file, 'r') as f:
        task_groups = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create task groups using the REST API
    try:
        for task_group in task_groups['value']:
            print(f'Creating task group: {task_group["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/distributedtask/taskgroups?api-version=6.0-preview.1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.post(url, headers=headers, data=json.dumps(task_group))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_task_group = response.json()
                print(f'New task group created with ID: {new_task_group["id"]}')
            else:
                raise Exception(f'Failed to create task group. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the task groups: {e}')

def main():
    # Import the configuration variables
    import src.boards.config_import as config
    
    # Call the function to import the task groups
    import_task_groups(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'task_groups.json')
    )

if __name__ == '__main__':
    main()