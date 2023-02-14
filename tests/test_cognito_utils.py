from src.FlaskWebApp.cognito_utils import list_users
import boto3

def test_list_users():
    client = boto3.client("cognito-idp", region_name="us-east-1")
    return list_users(client=client, UserPoolId="us-east-1_QLQL2ORW0")


print(test_list_users())