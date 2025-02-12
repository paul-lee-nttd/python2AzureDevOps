import json
import requests
from base64 import b64encode
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def export_classic_pipeline(organization, project, personal_access_token, pipeline_id, output_file):
    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Get the classic pipeline details using the REST API
    try:
        print(f'Getting classic pipeline details for pipeline ID: {pipeline_id}')
        
        url = f'https://dev.azure.com/{organization}/{project}/_apis/build/definitions/{pipeline_id}?api-version=6.0'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.get(url, headers=headers)
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 200:
            pipeline_definition = response.json()
            # Export the pipeline definition to a JSON file
            with open(output_file, 'w') as f:
                json.dump(pipeline_definition, f, indent=4)
            print(f'Classic pipeline definition has been exported to {output_file}')
        else:
            raise Exception(f'Failed to get classic pipeline details. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    # Import the configuration variables
    import config_classic as config_classic
    
    # Call the function to export the classic pipeline
    export_classic_pipeline(
        config_classic.organization, 
        config_classic.project, 
        config_classic.personal_access_token, 
        config_classic.pipeline_id, 
        config_classic.output_file
    )

if __name__ == '__main__':
    main()