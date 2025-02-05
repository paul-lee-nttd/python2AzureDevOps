from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

# Personal Access Token (PAT) and organization URL
personal_access_token = 'COfh8bljIyz9xLXtZsj27h6ark10Cp6RQc4MuP6pWUJjEZ01qHsXJQQJ99BAACAAAAAAAAAAAAASAZDOj5ds'
organization_url = 'https://paulyonghee.visualstudio.com/'

# Create a connection to the Azure DevOps organization
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client to interact with the Core API
core_client = connection.clients.get_core_client()

# Function to create a new project
def create_project(project_name, project_description):
    try:
        project_params = {
            "name": project_name,
            "description": project_description,
            "capabilities": {
                "versioncontrol": {
                    "sourceControlType": "Git"
                },
                "processTemplate": {
                    "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"  # Agile process template
                }
            }
        }
        core_client.queue_create_project(project_params)
        print(f"Project '{project_name}' creation initiated.")
    except Exception as ex:
        print(f"Error creating project: {ex}")

# Function to list all projects
def list_projects():
    try:
        projects = core_client.get_projects()
        for project in projects:
            print(f"Name: {project.name}, Description: {project.description}")
    except Exception as ex:
        print(f"Error listing projects: {ex}")

# Function to get the project ID by name
def get_project_id(project_name):
    try:
        projects = core_client.get_projects()
        for project in projects:
            if project.name == project_name:
                return project.id
    except Exception as ex:
        print(f"Error getting project ID: {ex}")
    return None

# Function to update a project's description
def update_project_description(project_name, new_description):
    try:
        project_id = get_project_id(project_name)
        if not project_id:
            print(f"Project '{project_name}' does not exist.")
            return
        
        project = core_client.get_project(project_id)
        project.description = new_description
        core_client.update_project(project, project_id)
        print(f"Project '{project.name}' description updated.")
    except Exception as ex:
        print(f"Error updating project description: {ex}")

# Example usage
create_project("NewProject", "This is a new project created via the API.")
list_projects()
update_project_description("NewProject", "Updated project description.")
