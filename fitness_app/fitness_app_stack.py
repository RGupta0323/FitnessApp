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

        dev_log_group = logs.LogGroup(self, "DevLogs")
        api = apigateway.LambdaRestApi(self, "FitnessAppAPIGateway", handler=home_lambda,
                                       deploy_options=None
                                       )
        deployment = apigateway.Deployment(self, "Deployment", api=api)
        apigateway.Stage(self, "dev",
                         deployment=deployment,
                         access_log_destination=apigateway.LogGroupLogDestination(dev_log_group),
                         access_log_format=apigateway.AccessLogFormat.json_with_standard_fields(
                             caller=False,
                             http_method=True,
                             ip=True,
                             protocol=True,
                             request_time=True,
                             resource_path=True,
                             response_length=True,
                             status=True,
                             user=True
                         )
                         )

