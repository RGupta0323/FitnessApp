from flask import Flask, render_template, request
import serverless_wsgi
import boto3
from src.FlaskWebApp.cognito_utils import create_user, sign_up_user

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("Home.html")

@app.route("/createworkout", methods=["GET", "POST"])
def createworkout():
    return render_template("createworkout.html")

@app.route("/createexercise", methods=["GET"])
def createexercise():
    return render_template("createexercise.html")

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
        cognito_user_pool_id = "us-east-1_DH6Sb4sSO"
        # response = create_user(client, cognito_user_pool_id, email)
        # print(response)
        sign_up_user(client, ClientID="3hui7kpemv308dfnnfmon81hi2", username=email, password=password)

        print("line 32 - successful!")

        # check if successful

        # re-direct to login page



    return render_template("register.html")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)