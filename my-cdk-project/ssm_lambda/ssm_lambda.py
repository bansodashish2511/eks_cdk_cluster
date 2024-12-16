import boto3
import json
import os

def handler(event, context):
    try:
        # Initialize the SSM client
        ssm_client = boto3.client('ssm')

        # Retrieve the SSM parameter name from the environment variable
        ssm_parameter_name = os.environ.get('SSM_PARAMETER_NAME')
        if not ssm_parameter_name:
            raise ValueError("Environment variable 'SSM_PARAMETER_NAME' is not set.")

        # Fetch the SSM parameter value
        response = ssm_client.get_parameter(Name=ssm_parameter_name)
        environment = response['Parameter']['Value']

        # Determine the replica count based on the environment
        if environment == 'development':
            replica_count = 1
        elif environment in ['staging', 'production']:
            replica_count = 2
        else:
            raise ValueError(f"Unexpected environment value: {environment}")

        # Prepare the Helm values to return
        helm_values = {
            'controller': {
                'replicaCount': replica_count
            }
        }

        # Return the HelmValues as part of the response
        return {
            #'Status': 'SUCCESS',
            "Data": {
                #'HelmValues': json.dumps(helm_values) 
                "controller-replica_count":replica_count
            },
            "PhysicalResourceId": "1234"

        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'Status': 'FAILED',
            'Reason': str(e),
        }