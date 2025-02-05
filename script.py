from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint

# Replace with your personal access token and organization URL
personal_access_token = 'COfh8bljIyz9xLXtZsj27h6ark10Cp6RQc4MuP6pWUJjEZ01qHsXJQQJ99BAACAAAAAAAAAAAAASAZDOj5ds'
organization_url = 'https://paulyonghee.visualstudio.com/'

# Create a connection to the organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc.)
core_client = connection.clients.get_core_client()

# Get the first page of projects
get_projects_response = core_client.get_projects()

index = 0
for project in get_projects_response:
    pprint.pprint(f"[{index}] {project.name}")
    index += 1
