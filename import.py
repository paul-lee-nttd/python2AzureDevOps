from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

# Define variables
organization = '177204'
project = 'azure-devops-kubernetes-terraform'
personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'

# Create a connection to the organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

# Get the pipeline client
pipelines_client = connection.clients.get_pipelines_client()

# Import the pipeline definition from a JSON file
try:
    with open('pipeline_definition.json', 'r') as f:
        pipeline_definition = json.load(f)

    # Create a new pipeline using the imported definition
    new_pipeline = pipelines_client.create_pipeline(pipeline_definition, project=project)
    print(f'New pipeline created with ID: {new_pipeline.id}')

except Exception as e:
    print(f'An error occurred: {e}')
