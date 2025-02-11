import json
import requests
from base64 import b64encode

def import_classic_pipeline(organization, project, personal_access_token, new_pipeline_name, input_file):
    # Read the exported classic pipeline definition from the JSON file
    with open(input_file, 'r') as f:
        pipeline_definition = json.load(f)

    # Modify the pipeline definition to set the new pipeline name
    pipeline_definition['name'] = new_pipeline_name

    # Encode the personal access token
    encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

    # Create a new classic pipeline using the REST API
    try:
        print(f'Creating new classic pipeline with name: {new_pipeline_name}')
        
        url = f'https://dev.azure.com/{organization}/{project}/_apis/build/definitions?api-version=6.0'
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
            print(f'New classic pipeline created with ID: {new_pipeline_id}')
        else:
            raise Exception(f'Failed to create new classic pipeline. Status code: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'An error occurred while creating the new classic pipeline: {e}')

def main():
    # Define variables
    organization = '177204'
    project = 'PSRemoting-Test'
    personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'
    new_pipeline_name = 'NewClassicPipeline2'
    input_file = 'outputs/classic_pipeline_definition.json'

    import_classic_pipeline(organization, project, personal_access_token, new_pipeline_name, input_file)

if __name__ == '__main__':
    main()