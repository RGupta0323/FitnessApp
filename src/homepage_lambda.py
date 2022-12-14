# Displays home page
import os
def handler(event, context):
    print(os.getcwd())
    f = open("web/index.html", "r")
    html = f.readlines()
    f.close()
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type":"text/html"
            },
            'body': html
    }


