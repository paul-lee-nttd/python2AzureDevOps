import json
import requests
from base64 import b64encode
import config_import_yaml

def import_yaml_pipeline(organization, project, personal_access_token, new_pipeline_name, repository_id, input_file):
    # Read the exported pipeline definition from the JSON file
    with open(input_file, 'r') as f:
        pipeline_definition = json.load(f)

    # Ensure the YAML path and repository are included in the configuration
    pipeline_definition['configuration'] = {
        "type": "yaml",
        "path": "azure-pipelines.yml",
        "repository": {
            "id": repository_id,
            "name": repository_id,  # Use the repository ID here
            "type": "azureReposGit"
        }
    }

    # Set the new pipeline name in the definition
    pipeline_definition['name'] = new_pipeline_name

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create a new pipeline using the REST API
    try:
        print(f'Creating new pipeline with name: {new_pipeline_name}')
        
        url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines?api-version=6.0-preview.1'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(pipeline_definition))
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code in [200, 201]:
            new_pipeline = response.json()
            new_pipeline_id = new_pipeline['id']
            print(f'New pipeline created with ID: {new_pipeline_id}')
        else:
            raise Exception(f'Failed to create new pipeline. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the new pipeline: {e}')

def main():
    # Import the configuration variables
    import config_import_yaml
    
    # Call the function to import the YAML pipeline
    import_yaml_pipeline(
        config_import_yaml.organization, 
        config_import_yaml.project, 
        config_import_yaml.personal_access_token, 
        config_import_yaml.new_pipeline_name, 
        config_import_yaml.repository_id, 
        config_import_yaml.input_file
    )

if __name__ == '__main__':
    main()