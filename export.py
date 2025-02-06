from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

# Define variables
organization = '177204'
project = 'azure-devops-kubernetes-terraform'
personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'
pipeline_id = 11

# Create a connection to the organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

# Get the pipeline client
pipelines_client = connection.clients.get_pipelines_client()

# Export the pipeline definition
try:
    pipeline = pipelines_client.get_pipeline(project=project, pipeline_id=pipeline_id)
    pipeline_definition = pipeline.as_dict()

    # Export the pipeline definition to a JSON file
    with open('pipeline_definition.json', 'w') as f:
        json.dump(pipeline_definition, f, indent=4)

    print('Pipeline definition has been exported to pipeline_definition.json')

except Exception as e:
    print(f'An error occurred: {e}')
