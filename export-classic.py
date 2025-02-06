import json
import requests
from base64 import b64encode

# Define variables
organization = '177204'
project = 'DynamicsDeployment'
personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'
pipeline_id = 4

# Encode the personal access token
encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

# Get the classic pipeline details using the REST API
try:
    print(f'Getting classic pipeline details for pipeline ID: {pipeline_id}')
    
    url = f'https://dev.azure.com/{organization}/{project}/_apis/build/definitions/{pipeline_id}?api-version=6.0'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_pat}'
    }
    
    response = requests.get(url, headers=headers)
    
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    
    if response.status_code == 200:
        pipeline_definition = response.json()
        # Export the pipeline definition to a JSON file
        with open('classic_pipeline_definition.json', 'w') as f:
            json.dump(pipeline_definition, f, indent=4)
        print('Classic pipeline definition has been exported to classic_pipeline_definition.json')
    else:
        raise Exception(f'Failed to get classic pipeline details. Status code: {response.status_code}, Response: {response.text}')
except Exception as e:
    print(f'An error occurred: {e}')
