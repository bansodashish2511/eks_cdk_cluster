import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2
)
from constructs import Construct

class PyBucket(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        # Call the parent constructor first
        super().__init__(scope, construct_id, **kwargs)

    def __init__(self, scope: Construct, construct_id: str, bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        aws_lambda.Function(self, "PyCoolLambda",
            code=aws_lambda.Code.from_inline(
                "import os\ndef handler(event, context):\n print(os.environ['COOL_BUCKET_ARN'])"),
            handler='index.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            environment={
                "COOL_BUCKET_ARN":bucket.bucket_arn
            }                    
        )
    




        # Outputs
        cdk.CfnOutput(
            self, "ClusterName", 
            value=self.cluster.cluster_name
        )
