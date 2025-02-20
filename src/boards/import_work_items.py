import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_work_items(organization, project, personal_access_token, input_file):
    # Read the exported work items from the JSON file
    with open(input_file, 'r') as f:
        work_items = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create work items using the REST API
    try:
        for work_item in work_items:
            print(f'Creating work item: {work_item["fields"]["System.Title"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${work_item["fields"]["System.WorkItemType"]}?api-version=6.0'
            headers = {
                'Content-Type': 'application/json-patch+json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            # Prepare the data for the work item creation
            work_item_data = [
                {
                    "op": "add",
                    "path": "/fields/System.Title",
                    "value": work_item["fields"]["System.Title"]
                },
                {
                    "op": "add",
                    "path": "/fields/System.Description",
                    "value": work_item["fields"].get("System.Description", "")
                }
                # Add more fields as needed
            ]
            
            response = requests.post(url, headers=headers, data=json.dumps(work_item_data))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_work_item = response.json()
                print(f'New work item created with ID: {new_work_item["id"]}')
            else:
                raise Exception(f'Failed to create work item. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the work items: {e}')

def main():
    # Import the configuration variables
    import src.boards.config_import as config
    
    # Call the function to import the work items
    import_work_items(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'work_items.json')
    )

if __name__ == '__main__':
    main()