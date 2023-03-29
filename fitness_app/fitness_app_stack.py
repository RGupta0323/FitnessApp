from constructs import Construct
import boto3
import os
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito,
    RemovalPolicy,
    aws_lightsail as lightsail
)


class FitnessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        flask_lambda = _lambda.Function(self, id="FlaskHandler", function_name="FitnessApp_FlaskHandler",
                                        runtime=_lambda.Runtime.PYTHON_3_7,
                                        code=_lambda.Code.from_asset("src"), handler="app.handler")

        dynamo_lambda = _lambda.Function(self, id="DynamoLambda", function_name="FitnessApp_DynamoLambda", runtime=_lambda.Runtime.PYTHON_3_7,
                                                       code=_lambda.Code.from_asset("src"),
                                                       handler="dynamo_lambda.handler")

        register_lambda = _lambda.Function(self, id="register_lambda", function_name="FitnessApp_RegisterLambda",
                                           runtime=_lambda.Runtime.PYTHON_3_7,
                                           code=_lambda.Code.from_asset("src"),
                                           handler="register_lambda.handler")



        # lightsail instance - for hosting web app
        user_data = """
        sudo su
        sudo apt-get -y update
        sudo apt-get -y install python3 python3-venv python3-dev
        sudo apt-get -y install  nginx supervisor git
        apt install binutils 
        apt install python3-flask
        git clone https://github.com/RGupta0323/FitnessApp
        cd FitnessApp
        python3 -m venv venv 
        source venv/bin/activate
        pip install -r requirements.txt 
        pip install -r requirements-dev.txt
        pip install -r requirements-infra.txt 
        pip install gunicorn flask flask_bootstrap pandas numpy flask_WTF
        apt install pipenv
        pipenv shell
        apt install python3-flask
        pip install -U --no-cache-dir -v -v -v mod_wsgi-standalone
        """


        web_instance = lightsail.CfnInstance(
            self, "FitnessAppLightSailInstance",
            blueprint_id="ubuntu_20_04",
            bundle_id="nano_2_0",
            instance_name="FitnessAppLightSailInstance",
            user_data=user_data
        )



        # route53 - domain name stuff to give cognito


        # dynamodb table for user data - this contains First Name, Last Name, Email, & Passwords
        # This is to be used to login users in and to register users
        # partition key is to be a randomly generated string id (this will tie users to other dynamodb tables with fitness data)
        user_data_table = dynamodb.Table(self, "FitnessAppUserData",
                               partition_key=dynamodb.Attribute(name="email", type=dynamodb.AttributeType.STRING),
                               encryption=dynamodb.TableEncryption.AWS_MANAGED
                               )

        dynamo_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["dynamodb:*"],
            resources=[str(user_data_table.table_arn)]
        ))

        # containerize flask app & create ecs cluster from here.
        # tie it into a load balancer in a private subnet
        # (TODO LATER)



