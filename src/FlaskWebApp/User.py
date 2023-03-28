class User:
    def __init__(self, user_event_info):
        self.logged_in = True
        self.event = user_event_info
        self.workouts = []

    # workout format = {1: {'weight': '100', 'reps': '5'}, 'exercise': 'Barbell Deadlift'}
    def add_workout(self, workout):
        print("[User.py add_workout() line 9] Adding workout to user object. Entered add_workout() method")
        if("exercise" not in list(workout.keys())):
            print("[User.py add_workout() line 11] ERROR Occured. Input workout doesn't have 'exercise' key in it. Workout: {}".format(workout))

        if("1" not in list(workout.keys()) and 1 not in list(workout.keys())):
            print("[User.py add_workout() line 14] ERROR Occured. Input workout doesn't have a set# (1,2,etc) as a key in it.\n "
             + "Workout: {}".format(workout))

        print("[User.py add_workout() line 17] Input workout verified! Adding workout, {}, to user workouts".format(workout))
        self.workouts.append(workout)