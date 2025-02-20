import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def export_work_item_types(organization, project, personal_access_token, output_directory):
    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Get the list of work item types using the REST API
    try:
        print(f'Getting list of work item types for project: {project}')
        
        url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitemtypes?api-version=6.0'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.get(url, headers=headers)
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 200:
            work_item_types = response.json()
            # Export the work item types to a JSON file
            output_file = os.path.join(output_directory, 'work_item_types.json')
            with open(output_file, 'w') as f:
                json.dump(work_item_types, f, indent=4)
            print(f'Work item types have been exported to {output_file}')
        else:
            raise Exception(f'Failed to get work item types. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    # Import the configuration variables
    import config_import as config
    
    # Call the function to export the work item types
    export_work_item_types(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        config.output_directory
    )

if __name__ == '__main__':
    main()