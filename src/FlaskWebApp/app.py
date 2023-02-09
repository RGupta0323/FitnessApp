from flask import Flask
import serverless_wsgi
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)