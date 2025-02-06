import json
import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Define variables
organization = '177204'
project = 'spacegamewebapp'
personal_access_token = '5IvXIruuXeNsxn4G7lTzhMQ0f5nfI21Y29noYWaY9xBoxVULn2KCJQQJ99BBACAAAAAe37ZBAAASAZDO7bWH'
new_pipeline_name = 'NewPipelineName'

# Create a connection to the organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

# Read the exported pipeline definition from the JSON file
with open('pipeline_definition.json', 'r') as f:
    pipeline_definition = json.load(f)

# Set the new pipeline name in the definition
pipeline_definition['name'] = new_pipeline_name

# Create a new pipeline using the REST API
try:
    print(f'Creating new pipeline with name: {new_pipeline_name}')
    
    url = f'https://dev.azure.com/{organization}/{project}/_apis/pipelines?api-version=7.0'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {personal_access_token}'
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(pipeline_definition))
    
    if response.status_code == 200:
        new_pipeline = response.json()
        new_pipeline_id = new_pipeline['id']
        print(f'New pipeline created with ID: {new_pipeline_id}')
    else:
        raise Exception(f'Failed to create new pipeline. Status code: {response.status_code}, Response: {response.text}')
except Exception as e:
    print(f'An error occurred while creating the new pipeline: {e}')
