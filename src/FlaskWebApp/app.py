from flask import Flask, render_template, request
import serverless_wsgi
import boto3
from src.FlaskWebApp.cognito_utils import create_user, sign_up_user

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("line 11 - inside /register")
        fname = request.form.get("fname")
        print(fname)
        # getting input with name = lname in HTML form
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        event={"fname": fname, "lname": lname, "email":email, "password":password}
        print("event: {}".format(event))

        # using cognito to create user, & sign in user
        client = boto3.client('cognito-idp', region_name="us-east-1")
        cognito_user_pool_id = "us-east-1_QLQL2ORW0"
        response = create_user(client, cognito_user_pool_id, email)
        print(response)
        clientID = response["User"]["Username"]
        sign_up_user(client, ClientID=clientID, username=email, password=password)

        # check if successful

        # re-direct to login page



    return render_template("register.html")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)