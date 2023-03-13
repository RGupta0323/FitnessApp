from flask import Flask, render_template, request
import serverless_wsgi
import boto3
import json

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("Home.html")


@app.route("/createworkout", methods=["GET", "POST"])
def createworkout():
    # This if statement will be hit if someone has created an exercise and that should be shown on the createworkout page
    # so the user can create more exercises
    if(request.method == 'POST'):
        req_form = request.form
        print(req_form)
        keys = req_form.keys()
        values = req_form.values()
        print("keys: {}".format(keys))
        print("values: {}".format(values))

        # this is a didctionary based on the users response
        # it will look like this: {'set1weight': '200', 'set1reps': '3', 'set2weight':"", 'set3reps':''}
        user_dict = {element:req_form.get(element) for element in req_form}
        print("[/creatworkout endpoint app.py line 30] user_Dict: {}".format(user_dict))

        # Transform dictionary to look like this {"1": {'weight': '200", 'reps': "4"} "2":{'weight':'200', 'reps':'5'}}
        print(" [/createworkout endpoint] transforming user_Dict ")
        num_sets = int(max([letter for element in user_dict.keys() for letter in element if (letter.isdigit())]))
        modified_dict = {i + 1: {'weight': user_dict["set{}weight".format(i + 1)], 'reps': user_dict["set{}reps".format(i + 1)]} for i
                         in range(num_sets)}
        modified_dict["exercise"] = user_dict["exercise"]

        print("modified_dict: {}".format(modified_dict))


        # Now this dictionary will go back to createworkout.html, displaying the created exercise.
        return render_template("createworkout.html", user_dict = modified_dict)



    return render_template("createworkout.html")

@app.route("/createexercise", methods=["GET", "POST"])
def createexercise():
    return render_template("createexercise.html")

@app.route("/modifyexercise/<exercise>", methods=["GET", "POST"])
def modifyexercise(exercise):
    exercise_dict = {"BBP" : "Barbell Bench Press", "BS": "Barbell Squat", "BIBP": "Barbell Incline Bench Press",
                     "BR":"Barbell Rows", "PU":"Pull-Ups", "CD":"Chest Dips", "BD":"Barbell Deadlift", "BOP":"Barbell Overhead Press"
                     }
    exercise = exercise_dict[exercise]
    return render_template("modifyexercise.html", exercise=exercise)

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

        # call register_lambda using boto3



        # check if successful

        # re-direct to login page



    return render_template("register.html")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

if __name__ == "__main__":
    app.run(host='0.0.0.0')