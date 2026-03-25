import argparse
from data import DataManager
from model import FitnessModel

class FitnessCLI:
    def __init__(self):
        self.data_manager = DataManager()
        self.model = FitnessModel()
        self.current_user = None

    def run(self):
        parser = argparse.ArgumentParser(description="Personal Fitness Recommender CLI")
        parser.add_argument('command', choices=['register', 'login', 'set_goal', 'suggest_routine', 'log_workout', 'view_progress', 'help', 'exit'], help="Available commands")
        args = parser.parse_args()

        if args.command == 'register':
            self.register()
        elif args.command == 'login':
            self.login()
        elif args.command == 'set_goal':
            if self.current_user:
                self.set_goal()
            else:
                print("Please login first.")
        elif args.command == 'suggest_routine':
            if self.current_user:
                self.suggest_routine()
            else:
                print("Please login first.")
        elif args.command == 'log_workout':
            if self.current_user:
                self.log_workout()
            else:
                print("Please login first.")
        elif args.command == 'view_progress':
            if self.current_user:
                self.view_progress()
            else:
                print("Please login first.")
        elif args.command == 'help':
            self.show_help()
        elif args.command == 'exit':
            print("Goodbye!")
            exit()

    def register(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        age = int(input("Enter age: "))
        weight = float(input("Enter weight (kg): "))
        height = float(input("Enter height (cm): "))
        fitness_level = input("Enter fitness level (beginner/intermediate/advanced): ").lower()
        goal = input("Enter goal (lose_weight/build_muscle/general_fitness): ").lower()

        if self.data_manager.register_user(username, password, age, weight, height, fitness_level, goal):
            print("Registration successful!")
        else:
            print("Username already exists.")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if self.data_manager.login_user(username, password):
            self.current_user = username
            print(f"Welcome, {username}!")
        else:
            print("Invalid credentials.")

    def set_goal(self):
        goal = input("Enter new goal (lose_weight/build_muscle/general_fitness): ").lower()
        if self.data_manager.update_goal(self.current_user, goal):
            print("Goal updated!")
        else:
            print("Error updating goal.")

    def suggest_routine(self):
        user_data = self.data_manager.get_user_data(self.current_user)
        if user_data:
            routine = self.model.predict_routine(user_data)
            print(f"Recommended routine: {routine}")
            print("Sample workout: 30 mins cardio, 20 mins strength.")
        else:
            print("User data not found.")

    def log_workout(self):
        workout_type = input("Enter workout type (cardio/strength): ").lower()
        duration = int(input("Enter duration (minutes): "))
        self.data_manager.log_workout(self.current_user, workout_type, duration)
        print("Workout logged!")

    def view_progress(self):
        progress = self.data_manager.get_progress(self.current_user)
        print("Your progress:")
        for entry in progress:
            print(f"- {entry['date']}: {entry['workout_type']} for {entry['duration']} mins")

    def show_help(self):
        print("""
Available commands:
- register: Create a new account
- login: Log in to your account
- set_goal: Update your fitness goal
- suggest_routine: Get AI-recommended routine
- log_workout: Log a completed workout
- view_progress: View your workout history
- help: Show this help
- exit: Quit the app
        """)

if __name__ == "__main__":
    cli = FitnessCLI()
    while True:
        cli.run()