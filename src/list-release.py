import json
import requests
from base64 import b64encode

# Define variables
organization = '177204'
project = 'DynamicsDeployment'
personal_access_token = 'G2JAC9cbPJqH6y7albiNkRwapB13gaQLtyWixOFeaS31h5kAQzwjJQQJ99BBACAAAAAe37ZBAAASAZDO1aX7'

# Encode the personal access token
encoded_pat = b64encode(f':{personal_access_token}'.encode()).decode()

# Get the list of release definitions using the REST API
try:
    print(f'Getting list of release definitions for project: {project}')
    
    url = f'https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions?api-version=6.0'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_pat}'
    }
    
    response = requests.get(url, headers=headers)
    
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    
    if response.status_code == 200:
        release_definitions = response.json()
        print('List of release definitions:')
        for definition in release_definitions['value']:
            print(f"Name: {definition['name']}, ID: {definition['id']}")
    else:
        raise Exception(f'Failed to get list of release definitions. Status code: {response.status_code}, Response: {response.text}')
except Exception as e:
    print(f'An error occurred: {e}')
