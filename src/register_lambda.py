import os
import sys
from jinja2 import Environment, FileSystemLoader
from lambda_utils import get_contents_s3_obj
def handler(event, context):
    print("register_lambda handler called")
    '''env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "web"), encoding="utf8"))
    template = env.get_template("register.html")
    html = template.render()
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type":"text/html"
            },
            'body': html
    }'''
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

