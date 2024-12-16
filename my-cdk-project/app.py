#!/usr/bin/env python3
import aws_cdk as cdk
from my_cdk_project.eks_cluster_stack import PyBucket
from ssm_stack import SsmParameterStack

# Create the CDK App
app = cdk.App()

# Deploy EKS Cluster Stack
eks_cluster_stack = PyBucket(
    app,
    "PyBucket",
)

app.synth()