# Personal Fitness Recommender (CLI)

A command‑line, AI‑based fitness assistant that recommends **personalized full‑body workout routines** and tracks your training history.  
The system combines a simple machine learning model with rule‑based logic to adapt workouts to:

- Your **goal**: `build_muscle`, `lose_weight`, or `general_fitness`
- Your **fitness level**: `beginner`, `intermediate`, or `advanced`

It is designed as a complete **CLI application** with user accounts, data persistence, and basic analytics.

# Personal Fitness Recommender (CLI)

A command‑line, AI‑based fitness assistant that recommends **personalized full‑body workout routines** and tracks your training history.  
The system combines a simple machine learning model with rule‑based logic to adapt workouts to:

- Your **goal**: `build_muscle`, `lose_weight`, or `general_fitness`
- Your **fitness level**: `beginner`, `intermediate`, or `advanced`

It is designed as a complete **CLI application** with user accounts, data persistence, and basic analytics for the BYOP project.

---

## 1. Repository

GitHub repository (public):

```text
https://github.com/Aviralsahu960/Personal-Fitness-Recommender

---


2. **Install required Python libraries**

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` includes:

   - `scikit-learn`
   - `pandas`
   - `numpy`
   - (plus Python standard libraries used in the code)

3. **First run**

   On the first run, the app will automatically create:

   - `users.json` – stores registered users and their profiles
   - `workouts.json` – stores logged workouts
   - `fitness_model.pkl` – serialized decision tree model

---

## 3. Running the Application

This is an **interactive menu‑driven CLI application**.

From the project root, run:

```bash
python main.py
```

You will see a menu similar to:

```text
=== Main Menu ===
Not logged in
1. Register
2. Login
3. Set Goal
4. Suggest Routine
5. Log Workout
6. View Progress
7. Logout
8. Help
9. Exit
10. Workout Summary
Enter your choice (1-10):
```

You interact by entering the number corresponding to the action.

---

## 4. Features and Workflow

### 4.1 User Management

**Register (Menu option 1)**

- Creates a new user account with:
  - Username and password
  - Age, weight (kg), height (cm)
  - Fitness level: `beginner`, `intermediate`, `advanced`
  - Goal: `lose_weight`, `build_muscle`, `general_fitness`
- All inputs are validated (e.g., numeric checks, allowed options only).

**Login / Logout (Menu options 2 and 7)**

- Login uses the stored username and password.
- Only **one user can be logged in at a time**.
- You must logout before logging in as another user.

**Set Goal (Menu option 3)**

- Update the logged‑in user’s long‑term goal:
  - `lose_weight`, `build_muscle`, `general_fitness`

---

### 4.2 AI‑Based Routine Recommendation (Menu option 4)

When you choose **“Suggest Routine”**:

1. The application loads your profile from `users.json`.
2. A small **Decision Tree Classifier** (from `scikit-learn`) predicts a high‑level routine category:
   - `Cardio Focus`
   - `Strength Training`
   - `Balanced`
3. Based on:
   - predicted category,
   - your stored **goal**,
   - your **fitness level** (`beginner` / `intermediate` / `advanced`),
   
   the app prints a **detailed full‑body workout plan**, including:

- Separate suggestions for **home** (bodyweight, dumbbells, resistance bands) and **gym** (machines, barbells).
- Multiple exercises with sets and reps.
- Easier routines for beginners and heavy/complex routines for advanced users.

This logic lives mainly in:

- `model.py` – ML model and prediction
- `main.py` – functions `_print_build_muscle_plan`, `_print_lose_weight_plan`, `_print_general_fitness_plan`

---

### 4.3 Workout Logging (Menu option 5)

The app supports **rich workout logging** for the logged‑in user.  
For each session you log, you enter:

- **Session goal**: `lose_weight` / `build_muscle` / `general_fitness`
- **Location**: `home` / `gym`
- **Short description**: e.g. `Squats, bench, rows – advanced gym day`
- **Duration** (in minutes)

This information is stored in `workouts.json` as entries like:

```json
{
  "username": [
    {
      "date": "2026-03-25 21:10:32",
      "goal": "build_muscle",
      "location": "gym",
      "description": "Squats, bench, rows – advanced gym day",
      "duration": 75
    }
  ]
}
```

This makes the app usable not just for the project, but also as a simple personal training log.

---

### 4.4 Viewing Progress (Menu option 6)

Displays all logged workouts for the current user in a readable format:

```text
- 2026-03-25 21:10:32 | goal=build_muscle, location=gym, duration=75 mins
  description: Squats, bench, rows – advanced gym day
```

You can use this output as screenshots in the **OUTPUT** and **TESTING AND REFINEMENT** sections of your project report.

---

### 4.5 Workout Summary / Analytics (Menu option 10)

Provides basic **analytics** over the user’s training history, including:

- Total number of sessions
- Total minutes trained
- Average duration per session
- Number of sessions by **goal**
- Number of sessions by **location**

Example:

```text
=== Workout Summary ===
Total sessions : 5
Total minutes  : 320 min
Average length : 64.0 min/session

Sessions by goal:
- build_muscle: 3 session(s)
- lose_weight: 2 session(s)

Sessions by location:
- gym: 4 session(s)
- home: 1 session(s)
```

This is especially useful for:

- **Significant Project Outcomes**
- **Testing and Refinement**
- **Applicability to real‑world use** in your project report.

---

## 5. Internal Design (High-Level)

- **`main.py`**
  - Handles the CLI menu and user interaction.
  - Implements:
    - registration, login/logout, goal setting,
    - AI routine suggestion,
    - workout logging, progress view, and summary analytics.

- **`data.py`**
  - Manages persistent storage using JSON files.
  - Functions:
    - `register_user`, `login_user`, `get_user_data`, `update_goal`
    - `log_workout` (rich entries with goal, location, description, duration)
    - `get_progress` (returns all workouts for a user)

- **`model.py`**
  - Builds a small sample dataset of user profiles and routine labels.
  - Encodes categorical fields manually.
  - Trains a `DecisionTreeClassifier` to map (age, weight, height, fitness_level, goal) → routine type.
  - Saves/loads the model with `joblib` as `fitness_model.pkl`.

---

## 6. Example Usage Flow

1. **Start the app**

   ```bash
   python main.py
   ```

2. **Register a new user** (option 1)  
   Provide age, weight, height, fitness level, and goal.

3. **Login** (option 2)

4. **Get a recommended routine** (option 4)  
   View the detailed workout for your level and goal.

5. **Perform your workout**, then **log it** (option 5)  
   Provide session goal, location, description, and duration.

6. **Check progress** (option 6) and **summary analytics** (option 10).

---

## 7. Project Report

For the formal course submission, refer to `project_report.pdf`.  
The report typically covers:

- Problem statement and motivation  
- Existing methods and their limitations  
- System design and methodology (CLI structure, ML model, data flow)  
- Detailed module descriptions (`main.py`, `data.py`, `model.py`)  
- Screenshots of CLI outputs (routines, logs, summary)  
- Testing strategy, limitations, and future enhancements

---

## 8. Possible Future Enhancements

Some ideas for extending this project:

- Store and analyze **weekly or monthly** trends (e.g., volume per muscle group).
- Add progression logic (e.g., automatically increasing sets/reps or weights).
- Support export of logs to CSV for further analysis.
- Incorporate real user feedback to adapt difficulty over time.
- Use a larger real dataset to train a more accurate recommendation model.

---

## Screenshots

Example CLI outputs are available in the `screenshots/` folder, including:
- Main menu (`MainMenu.png`)
- AI routine recommendation (`suggest_routine.png`)
- Workout logging and history (`log_workout.png`, `view_progress.png`)
- Workout analytics summary (`workout_summary.png`)

If you follow the steps above, an evaluator with no prior context should be able to install, run, and understand the project entirely from the command line.  
