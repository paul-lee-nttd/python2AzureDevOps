import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def import_work_item_queries(organization, project, personal_access_token, input_file):
    # Read the exported work item queries from the JSON file
    with open(input_file, 'r') as f:
        work_item_queries = json.load(f)

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create work item queries using the REST API
    try:
        for query in work_item_queries['value']:
            print(f'Creating work item query: {query["name"]}')
            
            url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/queries/{query["path"]}?api-version=6.0'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {encoded_pat}'
            }
            
            response = requests.put(url, headers=headers, data=json.dumps(query))
            
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
            
            if response.status_code in [200, 201]:
                new_query = response.json()
                print(f'New work item query created with ID: {new_query["id"]}')
            else:
                raise Exception(f'Failed to create work item query. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the work item queries: {e}')

def main():
    # Import the configuration variables
    import config_import as config
    
    # Call the function to import the work item queries
    import_work_item_queries(
        config.organization, 
        config.project, 
        config.personal_access_token, 
        os.path.join(config.output_directory, 'work_item_queries.json')
    )

if __name__ == '__main__':
    main()