import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def export_task_groups(organization, project, personal_access_token, output_directory):
    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Get the list of task groups using the REST API
    try:
        print(f'Getting list of task groups for project: {project}')
        
        url = f'https://dev.azure.com/{organization}/{project}/_apis/distributedtask/taskgroups?api-version=6.0-preview.1'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.get(url, headers=headers)
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 200:
            task_groups = response.json()
            # Export the task groups to a JSON file
            output_file = os.path.join(output_directory, 'task_groups.json')
            with open(output_file, 'w') as f:
                json.dump(task_groups, f, indent=4)
            print(f'Task groups have been exported to {output_file}')
        else:
            raise Exception(f'Failed to get task groups. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    # Import the configuration variables
    import src.boards.config_export as config
    
    # Call the function to export the task groups
    export_task_groups(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        config.output_directory
    )

if __name__ == '__main__':
    main()