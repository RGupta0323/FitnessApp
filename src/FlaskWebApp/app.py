from flask import Flask, render_template, request
import serverless_wsgi
from src import register_lambda
from src import login_lambda
import User

app = Flask(__name__)

# User login info (if logged in )
logged_in = False
user_event_info = None
global user

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

        global user
        # TODO
        if user == None:
            # display a message to tell teh user to login and then re-directs them to the login page
            error_message = "User must be logged in to create a workout"
            return render_template()
        user.add_workout(modified_dict) # adding new workout to global user object


        # Now this dictionary will go back to createworkout.html, displaying the created exercise.
        print("[app.py create_workout() line 55] User workouts to be rednered in createworkout.html. User workouts: {}".format(
            user.workouts
        ))
        return render_template("createworkout.html", user_dict = user.workouts)



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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # This is hwere the user puts in email address & password and logs in
        print("[app.py /register login() line 71] inside login() for POST request")
        email, password = request.form.get("email"), request.form.get("password")
        event = {"email":email, "password":password}
        print("[app.py /register login() line 73] event: {}".format(event))

        print("calling login lambda")
        res = login_lambda.handler(event, context=None)
        if( res["statuscode"] == 200):
            login_user(event)
            return render_template("Home.html", event = event)
        else:
            # notify user gets an error
            error_message = "Error has occured while logging you in. "
            return render_template("login.html", error_message=error_message)

        # Verify that teh user email and password
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "POST":
            print("[app.py /register register() line 66] inside /register")
            fname = request.form.get("fname")
            print(fname)
            # getting input with name = lname in HTML form
            lname = request.form.get("lname")
            email = request.form.get("email")
            password = request.form.get("password")
            event={"fname": fname, "lname": lname, "email":email, "password":password}
            print("event: {}".format(event))

            # call register_lambda
            print("calling register lambda")
            response = register_lambda.handler(event=event, context=None)

            if(type(response) == dict and "statuscode" in response.keys() and response["statuscode"] == 400):
                print("[app.py /register line 81] user email and/or password is invalid")
                if(response["type"] == "email"):
                    error_message = "Email {} is invalid. Please use a valid email".format(email)
                    return render_template("register.html", error_message=error_message)
                elif (response["type"] == "password"):
                    error_message = '''Password is invalid. Please make sure the password meets the following requirements. \n 
                     Should have at least one number. \n
                    Should have at least one uppercase and one lowercase character. \n
                    Should have at least one special symbol. \n
                    Should be between 6 to 20 characters long.
                    '''

                    return render_template("register.html", error_message=error_message)

            # re-direct to login page
            return render_template("Home.html", event=event)



        return render_template("register.html")
@app.route("/usercreatesworkout", methods=["GET", "POST"])
def usercreatesworkout(workout):
    print("[app.py usercreateworkout line 138] user workout: {}".format(workout))
    # When the user clicks the below button, then the workout will be created for the user.
    #         It gets into a dynamodb table that has the user's fitness data
    #         It gets re-directed to the homepage with that workout (the homepage gets it from dynamodb
    #         Once at teh home page they can create another workout or they can just log the workout.
    return render_template("Home.html", workout=workout)


# function to set variables to log in user
def login_user(event):
    print("[app.py login_user() line 131] login_user() function has been entered")
    global user
    user = User(user_event_info=event)
    print("[app.py login_user() line 139] User object event info: {}".format(user.event))
    print("[app.py login_user() line 140] User logged in")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

if __name__ == "__main__":
    app.run(host='0.0.0.0')