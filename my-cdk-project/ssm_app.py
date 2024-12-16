import aws_cdk as cdk
from ssm_stack import SsmParameterStack

# Create the CDK App
app = cdk.App()
ssm_parameter_stack = SsmParameterStack(
    app,
    "SsmParameterStack",
)

app.synth()