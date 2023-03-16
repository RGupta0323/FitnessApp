import os
import sys
from jinja2 import Environment, FileSystemLoader
from src.lambda_utils import get_contents_s3_obj, get_all_items_from_dynamodb_table
import re
import boto3


'''
This lambda is going to be handling when a user register. 

Use Case: 
User goes to /register endpoint, fills out the form, submits his information. 
Then this function is getting triggered. 

INput: event will look like this: 

event = {
    'fname':"user_first_name", 
    "lname":"user_last_name", 
    "email":"User_email_address" 
    "password":"User_password"
    }
'''
def handler(event, context):
    print("register lambda triggered.")
    print("Event: {}".format(event))

    # Need to validate email address & password
    if(validate_email(event["email"]) == False or  validate_password(event["password"]) == False):
        return {"statuscode": 400, "body":"Error ocured. Input event doesn't have a valid email or password. Event: {}".format(event)}

    print("email and password validated")
    # Query dyanmo to make sure that it doesn't exist
    if(validate_new_user(event["email"]) == False ):
        # display an image on teh web UI that notifies the user that the email isnt' valid.
        return {"statuscode": 400, "body":"Error occured. Email isn't valid. User email: {}".format(event["email"])}

    # if all checks pass, insert it into dynamodb; at this point the lambda function ends and the /register endpoint is
    # re-directed to login page

    print("create new user")
    create_new_user(event)
    print("register lambda successful!")


def validate_email(email):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False

'''
Passwords Requirements: 
    Should have at least one number.
    Should have at least one uppercase and one lowercase character.
    Should have at least one special symbol.
    Should be between 6 to 20 characters long.
'''
def validate_password(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    # compiling regex
    pat = re.compile(reg)

    # searching regex
    mat = re.search(pat, password)

    # validating conditions
    if mat:
        return True
    else:
        return False

# function that queries dynamo to see if the email exists in dynamodb
def validate_new_user(email):
    dynamodb_client = boto3.client("dynamodb", region_name="us-east-1")
    response = dynamodb_client.query(
        TableName='fitness-app-dev-stack-FitnessAppUserData5D9F0F31-LF1ZCEL9ATRW',
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={
            ':email': {'S': '{}'.format(email)},
        }
    )
    print(response)
    if(response["ResponseMetadata"]["HTTPStatusCode"] == 200):
        return True
    return False

def create_new_user(event):
    print("[register_lambda create_new_user() line 104] create_new_user() entered")
    fname,lname,email,password = event["fname"], event["lname"], event["email"], event["password"]
    try:
        # get the latest id from the dynamo table so you can increment it
        table_name = "fitness-app-dev-stack-FitnessAppUserData5D9F0F31-LF1ZCEL9ATRW"
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'fname':fname,
                'lname':lname,
                "email":email,
                "password":password
            }
        )
        print("[register_lambda.py create_new_user() line 108] Finished putting dynamodb. Response: {}".format(response))
        return response

    except Exception as ex:
        print("[register_lambda.py create_new_user() line 110] Error occured. Exception message: {}".format(ex))
        return None