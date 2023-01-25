# this is the lambda that gets triggered when the register form gets submitted
# this inserts user data into the dynamodb table and then ideally logs them in
import json
import boto3
from boto3.dynamodb.conditions import Key

def handler(event, context):
    print("register_submit_form_lambda triggered")
    print("Event: {}".format(event))
    # query dynamo db to see if the user is in the database
    query_response= None
    try:
        client = boto3.client('dynamodb', region_name="us-east-1")
        query_response = client.query(TableName="FitnessAppUserData", KeyConditionExpression=Key("email").eq(event["email"]))
        print(query_response)
    # if the user is in the database then display a message indicating that a user with that email has an account and
    # re-direct to login page.
    except Exception as ex:
        print("Error in register_submit_form_lambda function")
        print("Error during querying dynamo db to check if the user is in the database")
        print("Error message: {}".format(ex))

    # if the user is not in the database, then proceed
    # If its the same email - then the lambda should re-direct the user to
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FitnessAppUserData')
    # table.put_item(Item=event)

    # redirect user to the login page & log user in
    return {"statuscode": 200 }

