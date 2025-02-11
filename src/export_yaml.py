import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json

def export_yaml_pipeline(organization, project, personal_access_token, pipeline_id, repository_name, yaml_path, branch_name, output_file):
    # Create a connection to the organization
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

    # Get the pipeline client
    pipelines_client = connection.clients.get_pipelines_client()

    # Export the pipeline definition including YAML content
    try:
        # Get the pipeline definition
        print(f'Getting pipeline definition for pipeline ID: {pipeline_id}')
        pipeline = pipelines_client.get_pipeline(project=project, pipeline_id=pipeline_id)
        pipeline_definition = pipeline.as_dict()

        # Get the repository ID using the repository name
        print(f'Getting repository ID for repository name: {repository_name}')
        repositories = requests.get(
            f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=7.0',
            auth=('', personal_access_token)
        ).json()

        repository_id = None
        for repo in repositories['value']:
            print(f'Found repository: {repo["name"]}, ID: {repo["id"]}')
            if repo["name"] == repository_name:
                repository_id = repo["id"]
                break

        if not repository_id:
            raise Exception(f'Repository with name {repository_name} not found.')

        print(f'Repository ID: {repository_id}')

        # Get the YAML content from the repository using the REST API
        print(f'Getting YAML content from path: {yaml_path} in branch: {branch_name}')
        response = requests.get(
            f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository_id}/items?path={yaml_path}&versionDescriptor.version={branch_name}&api-version=7.0',
            auth=('', personal_access_token)
        )

        if response.status_code == 200:
            yaml_content = response.text
            print(f'YAML Content: {yaml_content}')
        else:
            raise Exception('Failed to retrieve YAML content. Status code: ' + str(response.status_code))

        # Add the YAML content to the pipeline definition
        pipeline_definition['yaml_content'] = yaml_content

        # Export the complete pipeline definition to a JSON file
        with open(output_file, 'w') as f:
            json.dump(pipeline_definition, f, indent=4)

        print(f'Pipeline definition has been exported to {output_file}')

    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    # Import the configuration variables
    import config_yaml
    
    # Call the function to export the YAML pipeline
    export_yaml_pipeline(
        config_yaml.organization, 
        config_yaml.project, 
        config_yaml.personal_access_token, 
        config_yaml.pipeline_id, 
        config_yaml.repository_name, 
        config_yaml.yaml_path, 
        config_yaml.branch_name, 
        config_yaml.output_file
    )

if __name__ == '__main__':
    main()