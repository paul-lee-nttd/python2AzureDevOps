import json
import requests
from base64 import b64encode
import config_import_release

def import_release_pipeline(organization, project, personal_access_token, new_pipeline_name, input_file):
    # Read the exported release pipeline definition from the JSON file
    with open(input_file, 'r') as f:
        release_pipeline_definition = json.load(f)

    # Modify the pipeline definition to set the new pipeline name
    release_pipeline_definition['name'] = new_pipeline_name

    # Ensure the pipeline definition has at least one stage
    if 'environments' not in release_pipeline_definition or not release_pipeline_definition['environments']:
        release_pipeline_definition['environments'] = [
            {
                "name": "Stage 1",
                "variables": {},
                "deployPhases": [
                    {
                        "name": "Agent phase",
                        "phaseType": "agentBasedDeployment",
                        "rank": 1,
                        "deploymentInput": {
                            "parallelExecution": {
                                "parallelExecutionType": "none"
                            },
                            "skipArtifactsDownload": False,
                            "artifactsDownloadInput": {},
                            "queueId": 0,
                            "demands": [],
                            "enableAccessToken": False,
                            "timeoutInMinutes": 0,
                            "jobCancelTimeoutInMinutes": 1,
                            "condition": "succeeded()",
                            "overrideInputs": {}
                        },
                        "workflowTasks": [
                            {
                                "taskId": "00000000-0000-0000-0000-000000000000",
                                "version": "1.*",
                                "name": "Task 1",
                                "refName": "Task_1",
                                "enabled": True,
                                "alwaysRun": False,
                                "continueOnError": False,
                                "timeoutInMinutes": 0,
                                "definitionType": "metaTask",
                                "inputs": {}
                            }
                        ]
                    }
                ]
            }
        ]

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create a new release pipeline using the REST API
    try:
        print(f'Creating new release pipeline with name: {new_pipeline_name}')
        
        url = f'https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions?api-version=6.0'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_pat}'
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(release_pipeline_definition))
        
        print(f'Status Code: {response.status_code}')
        print(f'Response Text: {response.text}')
        
        if response.status_code in [200, 201]:
            new_pipeline = response.json()
            new_pipeline_id = new_pipeline['id']
            print(f'New release pipeline created with ID: {new_pipeline_id}')
        else:
            raise Exception(f'Failed to create new release pipeline. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the new release pipeline: {e}')

def main():
    # Import the configuration variables
    import config_import_release
    
    # Call the function to import the release pipeline
    import_release_pipeline(
        config_import_release.organization, 
        config_import_release.project, 
        config_import_release.personal_access_token, 
        config_import_release.new_pipeline_name, 
        config_import_release.input_file
    )

if __name__ == '__main__':
    main()