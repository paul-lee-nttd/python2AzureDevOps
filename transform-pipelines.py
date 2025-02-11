import json

# Read the TFS release pipeline definition from the JSON file
with open('release_pipeline_definition.json', 'r') as f:
    tfs_release_pipeline_definition = json.load(f)

# Transform the TFS release pipeline definition to Azure DevOps format
azure_devops_release_pipeline_definition = {
    "name": tfs_release_pipeline_definition[0]['name'],
    "description": tfs_release_pipeline_definition[0].get('description', ''),
    "variables": tfs_release_pipeline_definition[0].get('variables', {}),
    "variableGroups": tfs_release_pipeline_definition[0].get('variableGroups', []),
    "environments": [],
    "artifacts": tfs_release_pipeline_definition[0].get('artifacts', []),
    "triggers": tfs_release_pipeline_definition[0].get('triggers', []),
    "releaseNameFormat": tfs_release_pipeline_definition[0].get('releaseNameFormat', 'Release-$(rev:r)'),
    "tags": tfs_release_pipeline_definition[0].get('tags', []),
    "properties": tfs_release_pipeline_definition[0].get('properties', {}),
}

# Transform environments (stages)
for environment in tfs_release_pipeline_definition[0].get('environments', []):
    azure_devops_environment = {
        "name": environment['name'],
        "variables": environment.get('variables', {}),
        "variableGroups": environment.get('variableGroups', []),
        "preDeployApprovals": environment.get('preDeployApprovals', {}),
        "deployStep": environment.get('deployStep', {}),
        "postDeployApprovals": environment.get('postDeployApprovals', {}),
        "deployPhases": [],
        "environmentOptions": environment.get('environmentOptions', {}),
        "demands": environment.get('demands', []),
        "conditions": environment.get('conditions', []),
        "executionPolicy": environment.get('executionPolicy', {}),
        "schedules": environment.get('schedules', []),
        "retentionPolicy": environment.get('retentionPolicy', {}),
        "processParameters": environment.get('processParameters', {}),
        "properties": environment.get('properties', {}),
        "preDeploymentGates": environment.get('preDeploymentGates', {}),
        "postDeploymentGates": environment.get('postDeploymentGates', {}),
        "environmentTriggers": environment.get('environmentTriggers', []),
    }

    # Transform deploy phases
    for phase in environment.get('deployPhases', []):
        azure_devops_phase = {
            "name": phase['name'],
            "rank": phase['rank'],
            "phaseType": phase['phaseType'],
            "deploymentInput": phase['deploymentInput'],
            "workflowTasks": phase.get('workflowTasks', [])
        }
        azure_devops_environment['deployPhases'].append(azure_devops_phase)

    azure_devops_release_pipeline_definition['environments'].append(azure_devops_environment)

# Export the transformed Azure DevOps release pipeline definition to a JSON file
with open('azure_devops_release_pipeline_definition.json', 'w') as f:
    json.dump(azure_devops_release_pipeline_definition, f, indent=4)

print('Transformed release pipeline definition has been exported to azure_devops_release_pipeline_definition.json')