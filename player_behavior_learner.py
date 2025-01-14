import json
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class PlayerBehaviorLearner:
    def __init__(self):
        self.data = []
        self.model = RandomForestClassifier(n_estimators=100)
        self.load_data()

    def load_data(self):
        if os.path.exists("player_behavior_data.json"):
            with open("player_behavior_data.json", "r") as f:
                self.data = json.load(f)

    def save_data(self):
        with open("player_behavior_data.json", "w") as f:
            json.dump(self.data, f, indent=4)

    def collect_data(self, player_action, game_state):
        self.data.append({"player_action": player_action, "game_state": game_state})
        self.save_data()

    def train_model(self):
        X = []
        y = []
        for data_point in self.data:
            X.append(data_point["game_state"])
            y.append(data_point["player_action"])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_player_action(self, game_state):
        return self.model.predict([game_state])[0]

    def evaluate_model(self):
        X = []
        y = []
        for data_point in self.data:
            X.append(data_point["game_state"])
            y.append(data_point["player_action"])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        y_pred = self.model.predict(X_test)
        accuracy = np.mean(y_pred == y_test)
        print(f"Model accuracy: {accuracy:.2f}")

    def update_model(self):
        self.train_model()
        self.evaluate_model()

    def get_player_action(self, game_state):
        return self.predict_player_action(game_state)

    def add_data_point(self, player_action, game_state):
        self.collect_data(player_action, game_state)
        self.update_model()