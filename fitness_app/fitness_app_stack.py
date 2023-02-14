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
    RemovalPolicy
)


class FitnessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        flask_lambda = _lambda.Function(self, "FlaskHandler", runtime=_lambda.Runtime.PYTHON_3_7,
                                        code=_lambda.Code.from_asset("src"), handler="flask_lambda.handler")

        dynamo_lambda = _lambda.Function(self, id="DynamoLambda", runtime=_lambda.Runtime.PYTHON_3_7,
                                                       code=_lambda.Code.from_asset("src"),
                                                       handler="dynamo_lambda.handler")



        # cognito - for user auth
        cognito_user_pool = cognito.UserPool(self, "awesome-user-pool",
                                             user_pool_name="awesome-user-pool",
                                             sign_in_aliases=cognito.SignInAliases(
                                                 email=True
                                             ),
                                             self_sign_up_enabled=True,
                                             auto_verify=cognito.AutoVerifiedAttrs(
                                                 email=True
                                                 # This is True by default if email is defined in SignInAliases
                                             ),
                                             user_verification=cognito.UserVerificationConfig(
                                                 email_subject="You need to verify your email",
                                                 email_body="Thanks for signing up Your verification code is {####}",
                                                 # This placeholder is a must if code is selected as preferred verification method
                                                 email_style=cognito.VerificationEmailStyle.CODE
                                             ),
                                             standard_attributes=cognito.StandardAttributes(
                                                 fullname=cognito.StandardAttribute(
                                                     required=True,
                                                     mutable=True,
                                                 )
                                             ),
                                             custom_attributes={
                                                 "tenant_id": cognito.StringAttribute(min_len=10, max_len=15,
                                                                                      mutable=False),
                                                 "created_at": cognito.DateTimeAttribute(),
                                                 "employee_id": cognito.NumberAttribute(min=1, max=100, mutable=False),
                                                 "is_admin": cognito.BooleanAttribute(mutable=True),
                                             },
                                             password_policy=cognito.PasswordPolicy(
                                                 min_length=8,
                                                 require_lowercase=True,
                                                 require_uppercase=True,
                                                 require_digits=True,
                                                 require_symbols=True
                                             ),
                                             account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
                                             removal_policy=RemovalPolicy.DESTROY
                                             )

        app_client = cognito_user_pool.add_client(
            "fitness-app-client",
            user_pool_client_name="awesome-app-client",
            auth_flows=cognito.AuthFlow(
                user_password=True
            )
        )


        # dynamodb table for user data - this contains First Name, Last Name, Email, & Passwords
        # This is to be used to login users in and to register users
        # partition key is to be a randomly generated string id (this will tie users to other dynamodb tables with fitness data)
        user_data_table = dynamodb.Table(self, "FitnessAppUserData",
                               partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                               encryption=dynamodb.TableEncryption.AWS_MANAGED
                               )

        dynamo_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["dynamodb:PutItem"],
            resources=[str(user_data_table.table_arn)]
        ))


