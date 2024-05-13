import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

class MachineLearn:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.data = None
        self.features = None
        self.target = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions = None

    def load_and_prepare_data(self):
        # Loading and preparing data
        self.data = pd.read_csv(self.data_path)
        self.target = self.data['target']  # assuming 'target' is the column you want to predict
        self.features = self.data.drop('target', axis=1)
        self.split_data()

    def split_data(self):
        # Splitting data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features, self.target, test_size=0.2, random_state=42)

    def train_model(self):
        # Training the model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        # Evaluating the model
        self.predictions = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, self.predictions)
        print(f"Mean Squared Error: {mse}")
        return mse

    def plot_importances(self):
        # Plotting feature importances
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        plt.figure()
        plt.title('Feature Importances')
        plt.bar(range(self.features.shape[1]), importances[indices],
                color="r", align="center")
        plt.xticks(range(self.features.shape[1]), self.features.columns[indices], rotation=90)
        plt.xlim([-1, self.features.shape[1]])
        plt.show()

# Example usage
ml = MachineLearn('path_to_your_data.csv')
ml.load_and_prepare_data()
ml.train_model()
ml.evaluate_model()
ml.plot_importances()

