import json
import requests
from base64 import b64encode
import pipelines.config_export_release as config_export_release

def export_release_pipeline(organization, project, personal_access_token, output_file):
    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Get the list of release definitions using the REST API
    try:
        print(f'Getting list of release definitions for project: {project}')
        
        url = f'https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions?api-version=6.0'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.get(url, headers=headers)
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 200:
            release_pipeline_definitions = response.json()
            # Export the pipeline definitions to a JSON file
            with open(output_file, 'w') as f:
                json.dump(release_pipeline_definitions, f, indent=4)
            print(f'Release pipeline definitions have been exported to {output_file}')
        else:
            raise Exception(f'Failed to get release pipeline details. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    # Import the configuration variables
    import pipelines.config_export_release as config_export_release
    
    # Call the function to export the release pipeline
    export_release_pipeline(
        config_export_release.organization, 
        config_export_release.project, 
        config_export_release.personal_access_token, 
        config_export_release.output_file
    )

if __name__ == '__main__':
    main()