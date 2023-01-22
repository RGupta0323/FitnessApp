from constructs import Construct
import boto3
import os
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_dynamodb as dynamodb
)


class FitnessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        home_lambda = _lambda.Function(self, id="HomeLambda",
                                   runtime=_lambda.Runtime.PYTHON_3_7,
                                   code=_lambda.Code.from_asset("src"),
                                   handler="homepage_lambda.handler")

        register_lambda = _lambda.Function(self, id="RegisterLambda", runtime=_lambda.Runtime.PYTHON_3_7,
                                           code=_lambda.Code.from_asset("src"),
                                           handler="register_lambda.handler")

        register_submit_form_lambda = _lambda.Function(self, id="RegisterSubmitFormLambda", runtime=_lambda.Runtime.PYTHON_3_7,
                                                       code=_lambda.Code.from_asset("src"),
                                                       handler="register_submit_form_lambda.handler")


        api = apigateway.LambdaRestApi(self, "FitnessAppAPIGateway", handler=home_lambda,
                                       deploy_options=None
                                       )

        register_endpoint = api.root.add_resource("register") # adding endpiont in api gateway for register
        register_endpoint.add_method("GET", apigateway.LambdaIntegration(register_lambda))

        register_submit_form_endpoint = api.root.add_resource("register_form_submit")
        register_submit_form_endpoint.add_method("PUT", apigateway.LambdaIntegration(register_submit_form_lambda))

        # creating s3 bucket for static web pages
        web_files_bucket = s3.Bucket(self, "FitnessAppStaticWebFiles", encryption=s3.BucketEncryption.KMS_MANAGED,
                                     enforce_ssl=True, versioned=True)

        # uploading web files to s3 bucket
        s3_client = boto3.resource('s3')
        wfb_bucket = s3_client.Bucket("fitness-app-dev-stack-fitnessappstaticwebfiles659-1c9bv2im68wv0")

        home_lambda.add_to_role_policy(iam.PolicyStatement(actions=["s3:GetObject"], resources=["*"]))
        register_lambda.add_to_role_policy(iam.PolicyStatement(actions=["s3:GetObject"], resources=["*"]))
        for file in os.listdir("./src/web/"):
            wfb_bucket.upload_file("./src/web/" + file, file)

        # dynamodb table for user data - this contains First Name, Last Name, Email, & Passwords
        # This is to be used to login users in and to register users
        # partition key is to be a randomly generated string id (this will tie users to other dynamodb tables with fitness data)
        user_data_table = dynamodb.Table(self, "FitnessAppUserData",
                               partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                               encryption=dynamodb.TableEncryption.AWS_MANAGED
                               )


