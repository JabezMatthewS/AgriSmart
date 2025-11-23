import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Define the target file
DATA_FILE = "Crop_recommendation.csv"
MODEL_FILE = "crop_recommendation_model.pkl"

def train_model():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found. Please download it.")
        return
    
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    print("Training Random Forest Model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X_train, y_train)
    
    acc = model.score(X_test, y_test)
    print(f"Model Accuracy: {acc * 100:.2f}%")
    
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
