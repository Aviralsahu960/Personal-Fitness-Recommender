import json
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.workouts_file = 'workouts.json'
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.workouts_file):
            with open(self.workouts_file, 'w') as f:
                json.dump({}, f)

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
            json.dump(users, f)
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
                json.dump(users, f)
            return True
        return False

    def log_workout(self, username, workout_type, duration):
        with open(self.workouts_file, 'r') as f:
            workouts = json.load(f)
        if username not in workouts:
            workouts[username] = []
        workouts[username].append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'workout_type': workout_type,
            'duration': duration
        })
        with open(self.workouts_file, 'w') as f:
            json.dump(workouts, f)

    def get_progress(self, username):
        with open(self.workouts_file, 'r') as f:
            workouts = json.load(f)
        return workouts.get(username, [])