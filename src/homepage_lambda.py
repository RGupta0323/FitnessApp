# Displays home page
import os
import sys
from jinja2 import Environment, FileSystemLoader
def handler(event, context):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "web"), encoding="utf8"))
    template = env.get_template("index.html")
    html = template.render()
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type":"text/html"
            },
            'body': html
    }


