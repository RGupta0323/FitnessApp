# Displays home page
import os
print(os.getcwd())
from lambda_utils import get_contents_s3_obj
def handler(event, context):
    print("homepage_lambda handler called")
    html = get_contents_s3_obj(bucket_name="fitness-app-dev-stack-fitnessappstaticwebfiles659-1c9bv2im68wv0", object_key="index.html")
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type":"text/html"
            },
            'body': html.decode()
    }




