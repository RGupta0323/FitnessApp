# this is the lambda that gets triggered when the register form gets submitted
# this inserts user data into the dynamodb table and then ideally logs them in
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FitnessAppUserData')
def handler(event, context):
    # query dynamo db to see if the user is in the database

    # if the user is in the database then display a message indicating that a user with that email has an account and
    # re-direct to login page.

    # if the user is not in the database, then proceed
    # If its the same email - then the lambda should re-direct the user to
    table.put_item(Item=event)

    # redirect user to the login page & log user in
    return {"statuscode": 200 }