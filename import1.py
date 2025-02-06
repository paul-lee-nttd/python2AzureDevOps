from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

# Define variables
organization = '177204'
project = 'spacegamewebapp'
personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'
repository_name = 'Space Game - web'  # Use repository name instead of ID
yaml_path = 'azure-pipelines.yml'

# Create a connection to the organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

# Get the pipeline client
pipelines_client = connection.clients.get_pipelines_client()
git_client = connection.clients.get_git_client()

# Import the pipeline definition from a JSON file
try:
    with open('pipeline_definition.json', 'r') as f:
        pipeline_definition = json.load(f)

    # Extract the YAML content
    yaml_content = pipeline_definition.pop('yaml_content', None)
    if yaml_content is None:
        raise Exception('YAML content is missing in the pipeline definition.')

    # Get the repository ID using the repository name
    print(f'Getting repository ID for repository name: {repository_name}')
    repositories = git_client.get_repositories(project=project)
    repository_id = None
    for repo in repositories:
        if repo.name == repository_name:
            repository_id = repo.id
            break

    if not repository_id:
        raise Exception(f'Repository with name {repository_name} not found.')

    print(f'Repository ID: {repository_id}')

    # Create a new pipeline using the imported definition
    new_pipeline_definition = {
        "folder": pipeline_definition['folder'],
        "name": pipeline_definition['name'],
        "configuration": {
            "type": "yaml",
            "path": yaml_path,
            "repository": {
                "id": repository_id,
                "name": repository_name,
                "type": "azureReposGit"
            },
            "yaml_content": yaml_content
        }
    }

    new_pipeline = pipelines_client.create_pipeline(new_pipeline_definition, project=project)
    print(f'New pipeline created with ID: {new_pipeline.id}')

except Exception as e:
    print(f'An error occurred: {e}')
