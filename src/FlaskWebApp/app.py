from flask import Flask, render_template, request
import serverless_wsgi
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
    return render_template("register.html")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)