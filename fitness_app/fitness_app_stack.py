from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_logs as logs
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


        api = apigateway.LambdaRestApi(self, "FitnessAppAPIGateway", handler=home_lambda,
                                       deploy_options=None
                                       )

        register_endpoint = api.root.add_resource("register") # adding endpiont in api gateway for register



