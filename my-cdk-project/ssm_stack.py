from aws_cdk import (
    Stack,
    aws_ssm as ssm
)
from constructs import Construct

class SsmParameterStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Define allowed environments
        environments = ['development', 'staging', 'production']
        
        # Create SSM Parameters for each environment
        for env in environments:
            ssm.StringParameter(self, f"{env.capitalize()}EnvironmentParameter",
                parameter_name=f"/platform/account/env/{env}",
                string_value=env,
                description=f"Environment type for the {env} platform"
            )
        
        # Optional: Create a default/current environment parameter
        ssm.StringParameter(self, "CurrentEnvironmentParameter",
            parameter_name="/platform/account/env",
            string_value="development",  # Default to development
            description="Current active environment for the platform"
        )