import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_work_item_ids(organization, project, personal_access_token):
    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Define the WIQL query to get all work item IDs
    wiql_query = {
        "query": f"SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '{project}'"
    }

    # Execute the WIQL query using the REST API
    try:
        print(f'Executing WIQL query to get work item IDs for project: {project}')
        
        url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(wiql_query))
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 200:
            work_item_ids = [item['id'] for item in response.json()['workItems']]
            return work_item_ids
        else:
            raise Exception(f'Failed to execute WIQL query. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while executing the WIQL query: {e}')
        return []

def export_work_items(organization, project, personal_access_token, output_directory):
    # Get the work item IDs
    work_item_ids = get_work_item_ids(organization, project, personal_access_token)
    
    if not work_item_ids:
        print('No work items found.')
        return

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Get the details of each work item using the REST API
    try:
        work_items = []
        for work_item_id in work_item_ids:
            print(f'Getting details for work item ID: {work_item_id}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=6.0'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.get(url, headers=headers)
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code == 200:
                work_items.append(response.json())
            else:
                raise Exception(f'Failed to get work item details. Status code: {response.status_code}, Response: {response.text}')
        
        # Export the work items to a JSON file
        output_file = os.path.join(output_directory, 'work_items.json')
        with open(output_file, 'w') as f:
            json.dump(work_items, f, indent=4)
        print(f'Work items have been exported to {output_file}')
    except Exception as e:
        print(f'An error occurred while getting the work item details: {e}')

def main():
    # Import the configuration variables
    import src.boards.config_export as config
    
    # Call the function to export the work items
    export_work_items(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        config.output_directory
    )

if __name__ == '__main__':
    main()