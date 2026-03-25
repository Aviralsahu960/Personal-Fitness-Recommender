# Personal Fitness Recommender CLI
# Author: Aviral Sahu
# Course: Fundamentals of AI & ML (CSA2001) - BYOP
# Note: Designed as a simple terminal tool I can actually use for my own workouts.

from data import DataManager
from model import FitnessModel

class FitnessCLI:
    def __init__(self):
        self.data_manager = DataManager()
        self.model = FitnessModel()
        self.current_user = None

    def run(self):
        print("Welcome to the Personal Fitness Recommender CLI")
        while True:
            print("\n=== Main Menu ===")
            if self.current_user:
                print(f"Logged in as: {self.current_user}")
            else:
                print("Not logged in")

            print("1. Register")
            print("2. Login")
            print("3. Set Goal")
            print("4. Suggest Routine")
            print("5. Log Workout")
            print("6. View Progress")
            print("7. Logout")
            print("8. Help")
            print("9. Exit")
            print("10. Workout Summary")  # NEW

            choice = input("Enter your choice (1-10): ").strip()

            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                if self.current_user:
                    self.set_goal()
                else:
                    print("Please login first.")
            elif choice == "4":
                if self.current_user:
                    self.suggest_routine()
                else:
                    print("Please login first.")
            elif choice == "5":
                if self.current_user:
                    self.log_workout()
                else:
                    print("Please login first.")
            elif choice == "6":
                if self.current_user:
                    self.view_progress()
                else:
                    print("Please login first.")
            elif choice == "7":
                self.logout()
            elif choice == "8":
                self.show_help()
            elif choice == "9":
                print("Goodbye!")
                break
            elif choice == "10":
                if self.current_user:
                    self.show_summary()
                else:
                    print("Please login first.")
            else:
                print("Invalid choice. Please enter a number from 1 to 10.")

    def register(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        # age
        while True:
            try:
                age = int(input("Enter age: "))
                if age <= 0:
                    print("Age must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid age. Please enter a number (e.g., 25).")

        # weight
        while True:
            try:
                weight = float(input("Enter weight (kg): "))
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid weight. Please enter a number (e.g., 70.5).")

        # height
        while True:
            try:
                height = float(input("Enter height (cm): "))
                if height <= 0:
                    print("Height must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid height. Please enter a number (e.g., 170).")

        # VALIDATE fitness level
        valid_fitness_levels = ["beginner", "intermediate", "advanced"]
        while True:
            fitness_level = input(
                "Enter fitness level (beginner/intermediate/advanced): "
            ).lower().strip()
            if fitness_level in valid_fitness_levels:
                break
            else:
                print("Invalid choice. Please type exactly: beginner, intermediate, or advanced.")

        # VALIDATE goal
        valid_goals = ["lose_weight", "build_muscle", "general_fitness"]
        while True:
            goal = input(
                "Enter goal (lose_weight/build_muscle/general_fitness): "
            ).lower().strip()
            if goal in valid_goals:
                break
            else:
                print("Invalid choice. Please type exactly: lose_weight, build_muscle, or general_fitness.")

        if self.data_manager.register_user(username, password, age, weight, height, fitness_level, goal):
            print("Registration successful!")
        else:
            print("Username already exists.")

    def login(self):
        # prevent logging in another account while one is active
        if self.current_user:
            print(f"Already logged in as {self.current_user}. Please logout first to switch accounts.")
            return

        username = input("Enter username: ")
        password = input("Enter password: ")
        if self.data_manager.login_user(username, password):
            self.current_user = username
            print(f"Welcome, {username}! Remember: consistency beats perfection.")
        else:
            print("Invalid credentials.")

    def logout(self):
        if self.current_user:
            print(f"Logging out {self.current_user}...")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def set_goal(self):
        valid_goals = ["lose_weight", "build_muscle", "general_fitness"]
        while True:
            goal = input(
                "Enter new goal (lose_weight/build_muscle/general_fitness): "
            ).lower().strip()
            if goal in valid_goals:
                break
            else:
                print("Invalid choice. Please type exactly: lose_weight, build_muscle, or general_fitness.")

        if self.data_manager.update_goal(self.current_user, goal):
            print("Goal updated!")
        else:
            print("Error updating goal.")

    # ---------- ADVANCED ROUTINE GENERATION ----------
    def suggest_routine(self):
        user_data = self.data_manager.get_user_data(self.current_user)
        if not user_data:
            print("User data not found.")
            return

        # Ask model for high-level routine type
        routine_type = self.model.predict_routine(user_data)  # "Cardio Focus" / "Strength Training" / "Balanced"

        fitness_level = user_data.get("fitness_level", "beginner").lower()
        goal = user_data.get("goal", "general_fitness").lower()

        print("\n=== AI Routine Recommendation ===")
        print(f"Goal           : {goal}")
        print(f"Fitness level  : {fitness_level}")
        print(f"Routine focus  : {routine_type}\n")

        # Decide detailed plan based on routine_type + goal + fitness_level
        if goal == "build_muscle":
            self._print_build_muscle_plan(fitness_level)
        elif goal == "lose_weight":
            self._print_lose_weight_plan(fitness_level)
        else:  # general_fitness
            self._print_general_fitness_plan(fitness_level)

    def _print_build_muscle_plan(self, fitness_level: str):
        print("Today's Recommended Build-Muscle Full-Body Routine:")
        print("Tip: If you can easily finish all sets, increase weight slightly next week.")

        if fitness_level == "beginner":
            print("\nHome (Dumbbells / Bands / Bodyweight):")
            print("1. Goblet Squat           – 3 sets x 10–12 reps")
            print("2. Push-Ups (kneeling if needed) – 3 sets x 8–10 reps")
            print("3. One-Arm Dumbbell Row   – 3 sets x 10–12 reps / side")
            print("4. Glute Bridge           – 3 sets x 12–15 reps")
            print("5. Resistance Band Bicep Curls – 3 sets x 12 reps")
            print("6. Plank                  – 3 sets x 20–30 seconds")

            print("\nGym (Machines / Free Weights):")
            print("1. Leg Press              – 3 sets x 10–12 reps")
            print("2. Chest Press Machine    – 3 sets x 10–12 reps")
            print("3. Lat Pulldown           – 3 sets x 10–12 reps")
            print("4. Seated Row Machine     – 3 sets x 10–12 reps")
            print("5. Dumbbell Shoulder Press– 3 sets x 10 reps")
            print("6. Ab Crunch Machine      – 3 sets x 15 reps")

        elif fitness_level == "intermediate":
            print("\nHome (Dumbbells / Bands):")
            print("1. Bulgarian Split Squat      – 3 sets x 8–10 reps / leg")
            print("2. Push-Ups (standard)        – 4 sets x 10–12 reps")
            print("3. Bent-Over Dumbbell Row     – 4 sets x 8–10 reps")
            print("4. Romanian Deadlift (DB)     – 3 sets x 8–10 reps")
            print("5. Dumbbell Shoulder Press    – 3 sets x 8–10 reps")
            print("6. DB Curl + Tricep Extension superset – 3 sets x 10 reps each")
            print("7. Side Plank                 – 3 sets x 30 seconds / side")

            print("\nGym (Free Weights / Machines):")
            print("1. Back Squat or Hack Squat   – 4 sets x 6–8 reps")
            print("2. Bench Press (Barbell/DB)   – 4 sets x 6–8 reps")
            print("3. Deadlift (Romanian/Conventional) – 3 sets x 5–6 reps")
            print("4. Seated Row / T‑bar Row     – 3 sets x 8–10 reps")
            print("5. Overhead Press             – 3 sets x 6–8 reps")
            print("6. Leg Curl                   – 3 sets x 10–12 reps")
            print("7. Hanging Leg Raises         – 3 sets x 10–12 reps")

        else:  # advanced
            print("\nHome (Heavy Dumbbells / Bands – Advanced Split):")
            print("1. Front Squat with Dumbbells        – 4 sets x 6–8 reps")
            print("2. Weighted / Deficit Push-Ups       – 4 sets x 8–10 reps")
            print("3. Single-Leg Romanian Deadlift (DB) – 4 sets x 6–8 reps / leg")
            print("4. One-Arm Dumbbell Row (heavy)      – 4 sets x 6–8 reps / side")
            print("5. Standing Overhead Dumbbell Press  – 4 sets x 6–8 reps")
            print("6. Pull-Ups / Chin-Ups (weighted)    – 4 sets x 6–8 reps")
            print("7. Core: Ab Wheel / Hard Planks      – 4 sets x 10 reps or 45 sec")

            print("\nGym (Heavy Full-Body / Push-Pull-Legs Style):")
            print("A) Lower Body / Strength:")
            print("   1. Back Squat (heavy)           – 5 sets x 3–5 reps")
            print("   2. Romanian Deadlift            – 4 sets x 5–6 reps")
            print("   3. Walking Lunges (DB)          – 3 sets x 10–12 steps / leg")
            print("   4. Standing Calf Raise          – 4 sets x 10–15 reps")
            print("\nB) Upper Push:")
            print("   1. Bench Press (Barbell)        – 5 sets x 4–6 reps")
            print("   2. Incline Dumbbell Press       – 4 sets x 6–8 reps")
            print("   3. Overhead Press (Barbell/DB)  – 4 sets x 6–8 reps")
            print("   4. Cable Lateral Raises         – 3 sets x 12–15 reps")
            print("\nC) Upper Pull:")
            print("   1. Weighted Pull-Ups            – 4 sets x 6–8 reps")
            print("   2. Barbell Row / T‑Bar Row      – 4 sets x 6–8 reps")
            print("   3. Face Pulls                   – 3 sets x 12–15 reps")
            print("   4. Barbell or EZ‑bar Curls      – 3 sets x 8–10 reps")
            print("\nNOTE: For advanced lifters, rotate A/B/C days across the week (e.g., 4–6 days).")

    def _print_lose_weight_plan(self, fitness_level: str):
        print("Today's Recommended Fat-Loss / Conditioning Routine:")

        if fitness_level == "beginner":
            print("\nHome / Outdoor:")
            print("1. Brisk Walking                 – 20–30 minutes")
            print("2. Step-Ups on a stair or bench  – 3 sets x 12 reps / leg")
            print("3. Bodyweight Squats             – 3 sets x 12–15 reps")
            print("4. Wall Push-Ups                 – 3 sets x 10–12 reps")
            print("5. Glute Bridges                 – 3 sets x 12–15 reps")
            print("6. Marching in Place / Low-Impact Cardio – 5–10 minutes")

            print("\nGym (Cardio + Light Weights):")
            print("1. Treadmill or Cycle            – 20 minutes @ easy pace")
            print("2. Leg Press (light)             – 3 sets x 15 reps")
            print("3. Chest Press Machine (light)   – 3 sets x 12–15 reps")
            print("4. Lat Pulldown (light)          – 3 sets x 12 reps")

        elif fitness_level == "intermediate":
            print("\nHome / Outdoor (Intervals + Strength):")
            print("1. Jog/Run Intervals             – 5 x 2 minutes run, 2 minutes walk")
            print("2. Bodyweight Circuit (3 rounds):")
            print("   - Squats x 15")
            print("   - Push-Ups x 10–12")
            print("   - Reverse Lunges x 10 / leg")
            print("   - Mountain Climbers x 20 total")
            print("3. Plank                          – 3 sets x 30–40 sec")

            print("\nGym:")
            print("1. 10 min warm-up (treadmill / rower)")
            print("2. Full-body circuit (3–4 rounds, minimal rest):")
            print("   - Goblet Squat x 12")
            print("   - Dumbbell Bench Press x 10")
            print("   - Seated Row x 12")
            print("   - Kettlebell Swings x 15")
            print("3. 10–15 min moderate cardio (elliptical or bike)")

        else:  # advanced
            print("\nHome / Outdoor (High-Intensity):")
            print("1. HIIT Running:")
            print("   - 10 min warm-up jog")
            print("   - 8–10 x 30 sec sprint, 60–90 sec walk/jog")
            print("   - 5–10 min cool-down")
            print("2. Strength Circuit (4–5 rounds):")
            print("   - Jump Squats x 15")
            print("   - Burpees x 10–12")
            print("   - Push-Ups x 15–20")
            print("   - Alternating Lunges x 12 / leg")
            print("   - Plank or Hollow Hold x 30–45 sec")

            print("\nGym (Conditioning + Weights):")
            print("1. 10 min warm-up")
            print("2. Barbell Complex (4 rounds, 4–6 reps each):")
            print("   - Deadlift")
            print("   - Bent-Over Row")
            print("   - Hang Clean")
            print("   - Front Squat")
            print("   - Overhead Press")
            print("3. Finish with 15–20 min incline treadmill walk or stair climber.")

    def _print_general_fitness_plan(self, fitness_level: str):
        print("Today's Recommended General Fitness Full-Body Routine:")

        if fitness_level == "beginner":
            print("\nHome:")
            print("1. Bodyweight Squats         – 3 sets x 10–12 reps")
            print("2. Incline / Wall Push-Ups   – 3 sets x 8–10 reps")
            print("3. Dumbbell or Band Row      – 3 sets x 10–12 reps")
            print("4. Hip Hinge / Good Mornings – 3 sets x 12 reps")
            print("5. Standing Band Press       – 3 sets x 10–12 reps")
            print("6. Plank                     – 3 sets x 20–30 sec")
            print("7. Walk                      – 20 minutes easy pace")

            print("\nGym:")
            print("1. Treadmill / Bike warm-up  – 10 minutes")
            print("2. Machine Circuit (2–3 rounds):")
            print("   - Leg Press x 12")
            print("   - Chest Press x 12")
            print("   - Lat Pulldown x 12")
            print("   - Seated Row x 12")
            print("   - Shoulder Press x 12")

        elif fitness_level == "intermediate":
            print("\nHome (Balanced Strength + Cardio):")
            print("1. Goblet Squats              – 3 sets x 10–12 reps")
            print("2. Push-Ups                   – 3 sets x 10–15 reps")
            print("3. One-Arm DB Row             – 3 sets x 10 reps / side")
            print("4. Hip Thrusts / Glute Bridge – 3 sets x 12 reps")
            print("5. Dumbbell Shoulder Press    – 3 sets x 10 reps")
            print("6. Plank + Side Plank         – 3 sets x 30 sec each")
            print("7. 15–20 min light jog / cycle")

            print("\nGym:")
            print("1. Squat or Leg Press         – 3 sets x 8–10 reps")
            print("2. Bench Press (DB/Barbell)   – 3 sets x 8–10 reps")
            print("3. Lat Pulldown / Pull-Ups    – 3 sets x 8–10 reps")
            print("4. Seated Row                 – 3 sets x 10–12 reps")
            print("5. Dumbbell Shoulder Press    – 3 sets x 8–10 reps")
            print("6. Core circuit (3 rounds):")
            print("   - Hanging Knee Raises x 10–12")
            print("   - Cable Woodchoppers x 12 / side")

        else:  # advanced
            print("\nHome (Athletic Full-Body):")
            print("1. Jump Squats or Squat + Calf Raise – 4 sets x 8–10 reps")
            print("2. Decline or Weighted Push-Ups      – 4 sets x 10–12 reps")
            print("3. Single-Leg Romanian Deadlift (DB) – 3 sets x 8–10 reps / leg")
            print("4. Renegade Rows                     – 3 sets x 8–10 reps / side")
            print("5. Push Press (DB)                   – 3 sets x 6–8 reps")
            print("6. Core: Russian Twists + Leg Raises – 3 sets x 15–20 reps")
            print("7. 20–25 min moderate cardio (run, cycle, row).")

            print("\nGym (Performance-Oriented):")
            print("1. Power Clean or Kettlebell Swing – 4 sets x 4–6 reps")
            print("2. Front Squat                     – 4 sets x 6–8 reps")
            print("3. Bench Press                      – 4 sets x 6–8 reps")
            print("4. Pull-Ups / Lat Pulldown         – 4 sets x 8–10 reps")
            print("5. Walking Lunges (DB)             – 3 sets x 12 steps / leg")
            print("6. Farmer’s Walk                   – 3 rounds x 30–40 meters")

    # ---------- IMPROVED LOGGING ----------
    def log_workout(self):
        print("\nLog Workout")

        # Goal type for this session
        valid_goals = ["lose_weight", "build_muscle", "general_fitness"]
        while True:
            session_goal = input(
                "Session goal (lose_weight/build_muscle/general_fitness): "
            ).lower().strip()
            if session_goal in valid_goals:
                break
            else:
                print("Invalid choice. Please type exactly: lose_weight, build_muscle, or general_fitness.")

        # Location
        valid_locations = ["home", "gym"]
        while True:
            location = input("Location (home/gym): ").lower().strip()
            if location in valid_locations:
                break
            else:
                print("Invalid choice. Please type exactly: home or gym.")

        # Short description of what you did
        description = input(
            "Short description of workout (e.g., 'Squats, bench, rows – advanced gym day'): "
        ).strip()
        if not description:
            description = "No description provided."

        # Duration
        while True:
            try:
                duration = int(input("Enter duration (minutes): "))
                if duration <= 0:
                    print("Duration must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid duration. Please enter a number (e.g., 45).")

        # Store full details
        self.data_manager.log_workout(
            self.current_user,
            goal=session_goal,
            location=location,
            description=description,
            duration=duration,
        )

        print("Workout logged!")

    def view_progress(self):
        progress = self.data_manager.get_progress(self.current_user)
        if not progress:
            print("No workouts logged yet.")
            return

        print("Your progress:")
        for entry in progress:
            date = entry.get("date", "N/A")
            goal = entry.get("goal", "N/A")
            location = entry.get("location", "N/A")
            description = entry.get("description", "N/A")
            duration = entry.get("duration", "N/A")
            print(f"- {date} | goal={goal}, location={location}, duration={duration} mins")
            print(f"  description: {description}")

    # ---------- NEW: SUMMARY / ANALYTICS ----------
    def show_summary(self):
        progress = self.data_manager.get_progress(self.current_user)
        if not progress:
            print("No workouts logged yet. Log a few sessions first.")
            return

        total_sessions = len(progress)
        total_minutes = sum(e.get("duration", 0) for e in progress)

        # Count by goal
        goals_count = {}
        for e in progress:
            g = e.get("goal", "unknown")
            goals_count[g] = goals_count.get(g, 0) + 1

        # Count by location
        locations_count = {}
        for e in progress:
            loc = e.get("location", "unknown")
            locations_count[loc] = locations_count.get(loc, 0) + 1

        avg_duration = total_minutes / total_sessions if total_sessions > 0 else 0

        print("\n=== Workout Summary ===")
        print(f"Total sessions : {total_sessions}")
        print(f"Total minutes  : {total_minutes} min")
        print(f"Average length : {avg_duration:.1f} min/session")

        print("\nSessions by goal:")
        for g, c in goals_count.items():
            print(f"- {g}: {c} session(s)")

        print("\nSessions by location:")
        for loc, c in locations_count.items():
            print(f"- {loc}: {c} session(s)")

        print("\n")

    def show_help(self):
        print("""
Available actions in the menu:
1. Register         - Create a new account
2. Login            - Log in to your account
3. Set Goal         - Update your fitness goal
4. Suggest Routine  - Get AI-recommended detailed routine
5. Log Workout      - Log a completed workout (goal, location, description, duration)
6. View Progress    - View your workout history
7. Logout           - Logout from the current account
8. Help             - Show this help
9. Exit             - Quit the app
10. Workout Summary - View analytics for your logged workouts
        """)

if __name__ == "__main__":
    cli = FitnessCLI()
    cli.run()
