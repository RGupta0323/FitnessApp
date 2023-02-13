from flask import Flask, render_template, request
import serverless_wsgi
import boto3

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

        # add user data to dynamo - use congito for user verification!??
        client = boto3.client('cognito-idp')
        cognito_user_pool_id = "us-east-1_QLQL2ORW0"

        try:
            response = client.admin_create_user(
                UserPoolId=cognito_user_pool_id,
                Username=email,
                UserAttributes=[
                    {"Name": "fname", "Value":str(fname)},
                    {"Name": "lname", "Value": str(lname)},
                    {"Name":"email", "Value":str(email)},
                    {"Name":"password", "Value": str(password)}
                ]
            )


            print(response)

        except Exception as ex:
            print("Error has occured when trying to create user via cognito.")
            print("Error: {}".format(ex))
    return render_template("register.html")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)