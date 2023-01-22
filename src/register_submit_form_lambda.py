# this is the lambda that gets triggered when the register form gets submitted
# this inserts user data into the dynamodb table and then ideally logs them in
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FitnessAppUserData')
def handler(event, context):
    table.put_item(Item=event)

    # redirect user to the login page & log user in
    return {"statuscode": 200 }