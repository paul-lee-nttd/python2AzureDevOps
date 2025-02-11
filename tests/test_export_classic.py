import unittest
from unittest.mock import patch, MagicMock
import src.export_classic
from base64 import b64encode
import json
import src.config_classic as config_classic

class TestExportClassic(unittest.TestCase):
    @patch('src.export_classic.requests.get')
    def test_export_classic_pipeline(self, mock_get):
        # Load the mock response data from the JSON file
        with open('tests/mock_response_data.json', 'r') as f:
            mock_response_data = json.load(f)
        
        # Configure the mock to return a response with the mock data
        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response_data, text=json.dumps(mock_response_data))
        
        # Define variables
        organization = config_classic.organization
        project = config_classic.project
        personal_access_token = config_classic.personal_access_token
        pipeline_id = config_classic.pipeline_id
        output_file = config_classic.output_file
        
        # Call the function to export the classic pipeline
        src.export_classic.export_classic_pipeline(organization, project, personal_access_token, pipeline_id, output_file)
        
        # Verify that the requests.get method was called with the correct URL and headers
        mock_get.assert_called_with(
            f'https://dev.azure.com/{organization}/{project}/_apis/build/definitions/{pipeline_id}?api-version=6.0',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Basic {b64encode(f":{personal_access_token}".encode()).decode()}'
            }
        )
        
        # Verify that the JSON file was created with the correct content
        with open(output_file, 'r') as f:
            exported_data = json.load(f)
            self.assertEqual(exported_data, mock_response_data)

if __name__ == '__main__':
    unittest.main()