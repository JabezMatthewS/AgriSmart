import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Define the target file
DATA_FILE = "Crop_recommendation.csv"
MODEL_FILE = "crop_recommendation_model.pkl"

def generate_synthetic_data(filename):
    print(f"Generating synthetic dataset: {filename}...")
    # Crops and their typical ranges (approximate)
    # N, P, K, temperature, humidity, ph, rainfall
    crops_data = {
        "Rice":       {"N": (60, 90), "P": (35, 60), "K": (35, 45), "temp": (20, 27), "hum": (80, 90), "ph": (5.5, 7.2), "rain": (200, 300)},
        "Maize":      {"N": (60, 100), "P": (40, 60), "K": (15, 25), "temp": (18, 27), "hum": (50, 70), "ph": (5.5, 7.0), "rain": (60, 100)},
        "Chickpea":   {"N": (20, 60), "P": (55, 80), "K": (75, 85), "temp": (17, 20), "hum": (15, 20), "ph": (6.0, 8.0), "rain": (60, 90)},
        "Kidneybeans":{"N": (10, 40), "P": (55, 80), "K": (15, 25), "temp": (15, 25), "hum": (18, 25), "ph": (5.5, 6.0), "rain": (60, 150)},
        "Pigeonpeas": {"N": (10, 40), "P": (55, 80), "K": (15, 25), "temp": (18, 35), "hum": (10, 20), "ph": (4.5, 7.0), "rain": (90, 180)},
        "Mothbeans":  {"N": (10, 40), "P": (35, 60), "K": (15, 25), "temp": (24, 32), "hum": (40, 65), "ph": (3.5, 9.5), "rain": (30, 70)},
        "Mungbean":   {"N": (10, 40), "P": (35, 60), "K": (15, 25), "temp": (27, 30), "hum": (60, 70), "ph": (6.2, 7.2), "rain": (30, 60)},
        "Blackgram":  {"N": (30, 60), "P": (55, 80), "K": (15, 25), "temp": (25, 30), "hum": (60, 70), "ph": (6.5, 7.5), "rain": (60, 80)},
        "Lentil":     {"N": (10, 40), "P": (55, 80), "K": (15, 25), "temp": (18, 30), "hum": (60, 70), "ph": (5.9, 7.8), "rain": (35, 55)},
        "Pomegranate":{"N": (10, 40), "P": (10, 30), "K": (35, 45), "temp": (18, 25), "hum": (85, 95), "ph": (5.5, 7.2), "rain": (100, 120)},
        "Banana":     {"N": (80, 120), "P": (70, 95), "K": (45, 55), "temp": (25, 30), "hum": (75, 85), "ph": (5.5, 6.5), "rain": (90, 120)},
        "Mango":      {"N": (10, 40), "P": (15, 40), "K": (25, 35), "temp": (27, 35), "hum": (45, 55), "ph": (4.5, 7.0), "rain": (85, 100)},
        "Grapes":     {"N": (10, 40), "P": (120, 145), "K": (195, 205), "temp": (10, 40), "hum": (80, 85), "ph": (5.5, 6.5), "rain": (60, 80)},
        "Watermelon": {"N": (80, 120), "P": (5, 30), "K": (45, 55), "temp": (24, 27), "hum": (80, 90), "ph": (6.0, 7.0), "rain": (40, 60)},
        "Muskmelon":  {"N": (80, 120), "P": (5, 30), "K": (45, 55), "temp": (27, 30), "hum": (90, 95), "ph": (6.0, 6.8), "rain": (20, 30)},
        "Apple":      {"N": (10, 40), "P": (120, 145), "K": (195, 205), "temp": (21, 24), "hum": (90, 95), "ph": (5.5, 6.5), "rain": (100, 120)},
        "Orange":     {"N": (10, 40), "P": (5, 30), "K": (5, 15), "temp": (10, 35), "hum": (90, 95), "ph": (6.0, 7.5), "rain": (100, 120)},
        "Papaya":     {"N": (30, 70), "P": (45, 70), "K": (45, 60), "temp": (23, 44), "hum": (90, 95), "ph": (6.5, 7.0), "rain": (40, 250)},
        "Coconut":    {"N": (10, 40), "P": (5, 30), "K": (25, 35), "temp": (25, 29), "hum": (90, 95), "ph": (5.5, 6.5), "rain": (130, 230)},
        "Cotton":     {"N": (100, 140), "P": (35, 60), "K": (15, 25), "temp": (22, 26), "hum": (50, 70), "ph": (6.0, 8.0), "rain": (60, 100)},
        "Jute":       {"N": (60, 100), "P": (35, 60), "K": (35, 45), "temp": (23, 26), "hum": (70, 90), "ph": (6.0, 7.5), "rain": (150, 200)},
        "Coffee":     {"N": (80, 120), "P": (15, 40), "K": (25, 35), "temp": (23, 27), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (110, 200)}
    }

    data = []
    for crop, ranges in crops_data.items():
        for _ in range(100): # 100 samples per crop
            sample = {
                "N": np.random.randint(ranges["N"][0], ranges["N"][1]),
                "P": np.random.randint(ranges["P"][0], ranges["P"][1]),
                "K": np.random.randint(ranges["K"][0], ranges["K"][1]),
                "temperature": np.random.uniform(ranges["temp"][0], ranges["temp"][1]),
                "humidity": np.random.uniform(ranges["hum"][0], ranges["hum"][1]),
                "ph": np.random.uniform(ranges["ph"][0], ranges["ph"][1]),
                "rainfall": np.random.uniform(ranges["rain"][0], ranges["rain"][1]),
                "label": crop
            }
            data.append(sample)
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Created {filename} with {len(df)} samples.")

def train_model():
    if not os.path.exists(DATA_FILE):
        generate_synthetic_data(DATA_FILE)
    
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
