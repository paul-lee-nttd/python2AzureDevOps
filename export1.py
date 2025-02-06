from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

# Define variables
organization = '177204'
project = 'spacegamewebapp'
personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'
pipeline_id = 8
repository_name = 'Space Game - web'  # Use repository name instead of ID
yaml_path = 'azure-pipelines.yml'

# Create a connection to the organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

# Get the pipeline and Git clients
pipelines_client = connection.clients.get_pipelines_client()
git_client = connection.clients.get_git_client()

# Export the pipeline definition including YAML content
try:
    # Get the pipeline definition
    pipeline = pipelines_client.get_pipeline(project=project, pipeline_id=pipeline_id)
    pipeline_definition = pipeline.as_dict()

    # Get the repository ID using the repository name
    repositories = git_client.get_repositories(project=project)
    repository_id = None
    for repo in repositories:
        if repo.name == repository_name:
            repository_id = repo.id
            break

    if not repository_id:
        raise Exception(f'Repository with name {repository_name} not found.')

    # Get the YAML content from the repository
    item = git_client.get_item(repository_id, path=yaml_path, project=project, download=True)
    yaml_content = item.content

    # Add the YAML content to the pipeline definition
    pipeline_definition['yaml_content'] = yaml_content

    # Export the complete pipeline definition to a JSON file
    with open('pipeline_definition.json', 'w') as f:
        json.dump(pipeline_definition, f, indent=4)

    print('Pipeline definition has been exported to pipeline_definition.json')

except Exception as e:
    print(f'An error occurred: {e}')
