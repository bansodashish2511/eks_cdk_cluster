import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_eks as eks,
    aws_ec2 as ec2,
    Duration,
)
from aws_cdk.aws_cloudformation import CfnCustomResource
from aws_cdk.custom_resources import Provider
from constructs import Construct


class EksHelmStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get environment context
        environment = self.node.try_get_context("environment")
        if not environment:
            raise ValueError("Environment context is required!")

        # Define SSM parameter name
        ssm_parameter_name = {
            "development": "/platform/account/env/development",
            "staging": "/platform/account/env/staging",
            "production": "/platform/account/env/production",
        }.get(environment)

        if not ssm_parameter_name:
            raise ValueError(f"Invalid environment: {environment}")

        # Lambda function for custom resource
        lambda_function = _lambda.Function(
            self,
            "HelmValuesLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="ssm_lambda.handler",
            code=_lambda.Code.from_asset("./ssm_lambda"),
            timeout=Duration.seconds(60),
            environment={
                "SSM_PARAMETER_NAME": ssm_parameter_name,
            },
        )

        # Grant Lambda permissions to access SSM parameter
        lambda_function.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=[
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter{ssm_parameter_name}"
                ],
            )
        )

        # Create CustomResource Provider
        custom_resource_provider = Provider(
            self, "CustomResourceProvider", on_event_handler=lambda_function
        )

        # Create the CustomResource
        custom_resource = CfnCustomResource(
            self,
            "HelmValuesCustomResource",
            service_token=custom_resource_provider.service_token,
        )

        # Add environment as a property
        custom_resource.add_property_override("Environment", environment)

        # Retrieve the HelmValues from the custom resource
        helm_values = custom_resource.get_att("controller-replica_count").to_string()

        # Import the existing EKS cluster
        eks_cluster = eks.Cluster.from_cluster_attributes(
            self,
            "ExistingEksCluster",
            cluster_name="swiscomm-demo-cluster",
            kubectl_role_arn="arn:aws:iam::585008046798:role/PyBucket-MyEksClusterCreationRoleA5BECEC3-TYeZ9LV4F5sG",
            kubectl_lambda_role=iam.Role.from_role_arn(self,"importedrole","arn:aws:iam::585008046798:role/PyBucket-MyEksClusterKubectlHandlerRole1BA3B-OxFoLgd15FvY"),
            vpc=ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id="vpc-02efba471111965f2"),
        )

        # Add a Helm chart to the EKS cluster using the CustomResource values
        eks_cluster.add_helm_chart(
            "IngressNginxChart",
            chart="ingress-nginx",
            release="ingress-nginx",
            repository="https://kubernetes.github.io/ingress-nginx",
            namespace="ingress-nginx",
            values={
                "controller.replicaCount": helm_values,
            },
        )

        # Output Helm values
        cdk.CfnOutput(self, "HelmValues", value=helm_values)
