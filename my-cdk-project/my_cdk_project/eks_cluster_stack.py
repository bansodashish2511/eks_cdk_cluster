import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2
)
from constructs import Construct

class EksClusterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        # Call the parent constructor first
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(
            self, "EksVpc",
            max_azs=3,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Private",
                    cidr_mask=24
                )
            ]
        )

        # Create EKS Cluster
        self.cluster = eks.Cluster(  # Change this to self.cluster
            self, "MyEksCluster",
            vpc=vpc,
            cluster_name="swiscomm-demo-cluster",
            version=eks.KubernetesVersion.V1_27,
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUDIT,
                eks.ClusterLoggingTypes.AUTHENTICATOR
            ]
        )

        # Add Managed Node Group
        self.cluster.add_nodegroup_capacity(
            "standard-nodes",
            instance_types=[
                ec2.InstanceType.of(
                    ec2.InstanceClass.T3, 
                    ec2.InstanceSize.MEDIUM
                )
            ],
            min_size=1,
            max_size=3,
            desired_size=2
        )

        # Outputs
        cdk.CfnOutput(
            self, "ClusterName", 
            value=self.cluster.cluster_name
        )

        cdk.CfnOutput(
            self, "ClusterEndpoint", 
            value=self.cluster.cluster_endpoint
        )

        cdk.CfnOutput(self,"kubectl_role_arn",
            value= self.cluster.kubectl_role.role_arn
        )
        cdk.CfnOutput(self,"kubectl_lambda_role",
            value= self.cluster.kubectl_lambda_role.role_arn
        )