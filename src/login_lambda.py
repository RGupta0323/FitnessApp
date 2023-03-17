import boto3
def handler(event, context):
    pass

def verify_login(email, password):
    dynamodb_client = boto3.client("dynamodb", region_name="us-east-1")
    response = dynamodb_client.query(
        TableName='fitness-app-dev-stack-FitnessAppUserData5D9F0F31-LF1ZCEL9ATRW',
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={
            ':email': {'S': '{}'.format(email)},
        }
    )
    print("[login_lambda.py verify_login() line 14] dyanmodb response: {}".format(response))
