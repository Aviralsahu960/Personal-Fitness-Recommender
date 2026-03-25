import json
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.workouts_file = 'workouts.json'

        # Ensure files exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

        if not os.path.exists(self.workouts_file):
            with open(self.workouts_file, 'w') as f:
                json.dump({}, f)

    # ---------- USER MANAGEMENT ----------

    def register_user(self, username, password, age, weight, height, fitness_level, goal):
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username in users:
            return False

        users[username] = {
            'password': password,
            'age': age,
            'weight': weight,
            'height': height,
            'fitness_level': fitness_level,
            'goal': goal
        }

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

        return True

    def login_user(self, username, password):
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        return username in users and users[username]['password'] == password

    def get_user_data(self, username):
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        return users.get(username)

    def update_goal(self, username, goal):
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username in users:
            users[username]['goal'] = goal
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            return True

        return False

    # ---------- WORKOUT LOGGING ----------

    def log_workout(self, username, goal, location, description, duration):
        """
        Store a rich workout entry for the given user.

        Fields:
        - date: timestamp
        - goal: lose_weight / build_muscle / general_fitness
        - location: home / gym
        - description: free text (what exercises were done)
        - duration: minutes (int)
        """
        with open(self.workouts_file, 'r') as f:
            workouts = json.load(f)

        if username not in workouts:
            workouts[username] = []

        workouts[username].append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'goal': goal,
            'location': location,
            'description': description,
            'duration': duration
        })

        with open(self.workouts_file, 'w') as f:
            json.dump(workouts, f, indent=2)

    def get_progress(self, username):
        with open(self.workouts_file, 'r') as f:
            workouts = json.load(f)

        return workouts.get(username, [])