import json
import requests
from base64 import b64encode
import config_release

def export_release_pipeline(organization, project, personal_access_token, pipeline_id, output_file):
    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Get the release definition using the REST API
    try:
        print(f'Getting release definition for pipeline ID: {pipeline_id}')
        
        url = f'https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions/{pipeline_id}?api-version=6.0'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.get(url, headers=headers)
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code == 200:
            release_pipeline_definition = response.json()
            # Export the pipeline definition to a JSON file
            with open(output_file, 'w') as f:
                json.dump(release_pipeline_definition, f, indent=4)
            print(f'Release pipeline definition has been exported to {output_file}')
        else:
            raise Exception(f'Failed to get release pipeline details. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    # Import the configuration variables
    import config_release
    
    # Call the function to export the release pipeline
    export_release_pipeline(
        config_release.organization, 
        config_release.project, 
        config_release.personal_access_token, 
        config_release.pipeline_id, 
        config_release.output_file
    )

if __name__ == '__main__':
    main()