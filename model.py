import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

class FitnessModel:
    def __init__(self):
        self.model = None
        self.encoder = LabelEncoder()
        self.train_model()

    def train_model(self):
        # Sample dataset: age, weight, height, fitness_level, goal -> routine
        data = {
            'age': [20, 30, 40, 25, 35, 45, 22, 28, 50, 33],
            'weight': [70, 80, 90, 60, 75, 85, 65, 78, 95, 82],
            'height': [170, 175, 180, 165, 172, 178, 168, 173, 182, 177],
            'fitness_level': ['beginner', 'intermediate', 'advanced', 'beginner', 'intermediate', 'advanced', 'beginner', 'intermediate', 'advanced', 'intermediate'],
            'goal': ['lose_weight', 'build_muscle', 'general_fitness', 'lose_weight', 'build_muscle', 'general_fitness', 'lose_weight', 'build_muscle', 'general_fitness', 'general_fitness'],
            'routine': ['Cardio Focus', 'Strength Training', 'Balanced', 'Cardio Focus', 'Strength Training', 'Balanced', 'Cardio Focus', 'Strength Training', 'Balanced', 'Balanced']
        }
        df = pd.DataFrame(data)
        df['fitness_level'] = self.encoder.fit_transform(df['fitness_level'])
        df['goal'] = self.encoder.fit_transform(df['goal'])
        X = df[['age', 'weight', 'height', 'fitness_level', 'goal']]
        y = df['routine']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)
        # Save model for persistence
        joblib.dump(self.model, 'fitness_model.pkl')

    def predict_routine(self, user_data):
        # Load model if needed
        if self.model is None:
            self.model = joblib.load('fitness_model.pkl')
        # Encode user inputs
        user_df = pd.DataFrame([user_data])
        user_df['fitness_level'] = self.encoder.transform(user_df['fitness_level'])
        user_df['goal'] = self.encoder.transform(user_df['goal'])
        prediction = self.model.predict(user_df[['age', 'weight', 'height', 'fitness_level', 'goal']])
        return prediction[0]