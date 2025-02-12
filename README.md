# python2AzureDevOps


pip install azure-devops
pip install msrest



pip uninstall azure-devops
pip install azure-devops --upgrade
pip show azure-devops



# configure the variables for exporting and imporing pipeline

Update variables from /src/config_classic.py


# Execute exporting or importing

>python src/export_classic.py



# Update the json value from /tests/mock_response_data.json

# Test the exported json with the mock_response_date

>python -m unittest discover -s tests -p "test_export_classic.py"