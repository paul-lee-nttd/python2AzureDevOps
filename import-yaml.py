import json
import requests
from base64 import b64encode

# Define variables
organization = '177204'
project = 'DynamicsDeployment'
personal_access_token = '5IvXIruuXeNsxn4G7lTzhMQ0f5nfI21Y29noYWaY9xBoxVULn2KCJQQJ99BBACAAAAAe37ZBAAASAZDO7bWH'
new_pipeline_name = 'NewPipelineName2'
repository_id = 'c0936a89-567c-4c58-b69d-fc25da5b25b7'  # The ID of your repository

# Read the exported pipeline definition from the JSON file
with open('pipeline_definition.json', 'r') as f:
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
