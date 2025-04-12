import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
df = pd.read_csv('chronic_kidney_disease.csv')

# Handle missing values
df.ffill(inplace=True)

# Ensure there are no NaN values in the target variable
df = df.dropna(subset=['EventCKD35'])

# Split the data
X = df.drop('EventCKD35', axis=1)
y = df['EventCKD35']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Create the directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Save the model
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model training completed and saved to 'model/model.pkl'")