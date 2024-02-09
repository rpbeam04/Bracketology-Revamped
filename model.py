from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd

# Sample data (replace this with your own data)
data = pd.read_csv("Model/full-training.csv")
X = [[0], [1], [2], [3], [4]]
y = [0, 1, 2, 3, 4]

# Initialize the MLPRegressor
mlp_regressor = MLPRegressor(hidden_layer_sizes=(100,), activation='relu', solver='adam', max_iter=1000, random_state=42)

# Train the MLPRegressor
mlp_regressor.fit(X, y)

# Predict on the test set
y_pred = mlp_regressor.predict(X)

# Calculate the mean squared error (MSE)
mse = mean_squared_error(y, y_pred)
print("Mean Squared Error:", mse)