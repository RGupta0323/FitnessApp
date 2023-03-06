import os
import sys
from jinja2 import Environment, FileSystemLoader
from lambda_utils import get_contents_s3_obj


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


def handler2(event, context):
    print("register_lambda handler called")
    html = get_contents_s3_obj(bucket_name="fitness-app-dev-stack-fitnessappstaticwebfiles659-1c9bv2im68wv0",
                               object_key="register.html")
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/html"
        },
        'body': html.decode()
    }

