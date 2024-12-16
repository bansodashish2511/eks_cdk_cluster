#!/usr/bin/env python3
import aws_cdk as cdk
from my_cdk_project.eks_helm_stack import EksHelmStack

# Create the CDK App
app = cdk.App()

# Deploy Helm Chart Stack
EksHelmStack(
    app,
    "EksHelmStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"), 
        region=app.node.try_get_context("region")
    )
)

app.synth()