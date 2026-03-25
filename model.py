import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

class FitnessModel:
    def __init__(self):
        self.model_path = "fitness_model.pkl"
        self.model = None

        # manual encodings instead of LabelEncoder
        self.fitness_level_map = {
            "beginner": 0,
            "intermediate": 1,
            "advanced": 2,
        }
        self.goal_map = {
            "lose_weight": 0,
            "build_muscle": 1,
            "general_fitness": 2,
        }

        # load existing model if present, otherwise train a new one
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.train_model()

    def train_model(self):
        # Sample dataset: age, weight, height, fitness_level, goal -> routine
        data = {
            "age": [20, 30, 40, 25, 35, 45, 22, 28, 50, 33],
            "weight": [70, 80, 90, 60, 75, 85, 65, 78, 95, 82],
            "height": [170, 175, 180, 165, 172, 178, 168, 173, 182, 177],
            "fitness_level": [
                "beginner",
                "intermediate",
                "advanced",
                "beginner",
                "intermediate",
                "advanced",
                "beginner",
                "intermediate",
                "advanced",
                "intermediate",
            ],
            "goal": [
                "lose_weight",
                "build_muscle",
                "general_fitness",
                "lose_weight",
                "build_muscle",
                "general_fitness",
                "lose_weight",
                "build_muscle",
                "general_fitness",
                "general_fitness",
            ],
            "routine": [
                "Cardio Focus",
                "Strength Training",
                "Balanced",
                "Cardio Focus",
                "Strength Training",
                "Balanced",
                "Cardio Focus",
                "Strength Training",
                "Balanced",
                "Balanced",
            ],
        }

        df = pd.DataFrame(data)

        # manual encoding
        df["fitness_level"] = df["fitness_level"].map(self.fitness_level_map)
        df["goal"] = df["goal"].map(self.goal_map)

        X = df[["age", "weight", "height", "fitness_level", "goal"]]
        y = df["routine"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        # Save model for later use
        joblib.dump(self.model, self.model_path)

    def predict_routine(self, user_data: dict) -> str:
        """
        user_data is a dict like:
        {
            "age": 20,
            "weight": 55.0,
            "height": 180.0,
            "fitness_level": "beginner",
            "goal": "build_muscle"
        }
        """

        if self.model is None:
            # should not normally happen, but just in case
            self.train_model()

        # encode using our manual maps
        fitness_level_str = user_data.get("fitness_level", "").lower().strip()
        goal_str = user_data.get("goal", "").lower().strip()

        if fitness_level_str not in self.fitness_level_map:
            raise ValueError(f"Unknown fitness_level: {fitness_level_str}")

        if goal_str not in self.goal_map:
            raise ValueError(f"Unknown goal: {goal_str}")

        fitness_level_encoded = self.fitness_level_map[fitness_level_str]
        goal_encoded = self.goal_map[goal_str]

        row = pd.DataFrame(
            [
                {
                    "age": user_data.get("age", 0),
                    "weight": user_data.get("weight", 0.0),
                    "height": user_data.get("height", 0.0),
                    "fitness_level": fitness_level_encoded,
                    "goal": goal_encoded,
                }
            ]
        )

        prediction = self.model.predict(row)
        return prediction[0]