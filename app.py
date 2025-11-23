from flask import Flask, request, jsonify, render_template
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from scipy.spatial import cKDTree
import pickle
import json
import numpy as np
import os

app = Flask(__name__)

# --- Load Assets ---
print("Loading assets...")

# 1. Shapefile
districts = gpd.read_file("TN_districts.shp")

# 2. District NPK Data
npk_df = pd.read_csv("district_npk.csv")

# 3. Soil Dataset & KDTree
# Read compressed file to save space/bandwidth
soil_df = pd.read_csv("TN_soil_dataset.csv.gz")
tree = cKDTree(soil_df[["lat", "lon"]].values)

# 4. Weather Data
with open("weather_data.json", "r") as f:
    weather_data = json.load(f)

# 5. ML Model
model_path = "crop_recommendation_model.pkl"
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    print("WARNING: Model not found. Predictions will fail.")
    model = None

print("Assets loaded.")

@app.route("/")
def home():
    return render_template("index.html")

def get_weather(district_name):
    # Fuzzy match or direct lookup could be better, but for now direct
    # Normalize keys in weather_data to title case just in case
    
    # Try exact match
    if district_name in weather_data:
        return weather_data[district_name]
    
    # Try removing "District" or extra spaces
    clean_name = district_name.replace(" District", "").strip()
    if clean_name in weather_data:
        return weather_data[clean_name]
        
    # Fallback to a generic average if not found
    return {"temperature": 28.0, "humidity": 70.0, "rainfall": 900.0}

def predict_crop(N, P, K, temp, hum, ph, rain):
    if model:
        # Feature order must match training: N, P, K, temperature, humidity, ph, rainfall
        # Feature order must match training: N, P, K, temperature, humidity, ph, rainfall
        features = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], 
                              columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        
        # Get probabilities for all classes
        probs = model.predict_proba(features)[0]
        
        # Get indices of top 3 probabilities
        top_3_idx = np.argsort(probs)[-3:][::-1]
        
        # Get class names
        classes = model.classes_
        top_3_crops = classes[top_3_idx]
        
        return top_3_crops.tolist()
    return ["Model Error"]

@app.route("/predict_auto", methods=["POST"])
def predict_auto():
    try:
        data = request.get_json()
        lat = float(data["lat"])
        lon = float(data["lon"])

        # 1. Find nearest soil data point
        dist, idx = tree.query([lat, lon], k=1)
        soil_row = soil_df.iloc[idx].to_dict()
        
        # Helper to handle NaN
        def clean_val(val, default=0):
            if pd.isna(val):
                return default
            return val

        # Extract Soil pH
        ph = clean_val(soil_row.get("PH_TN_0cm.tif"), 6.5)
        
        # 2. Get District
        point = gpd.GeoDataFrame([{"geometry": Point(lon, lat)}], crs=districts.crs)
        # Spatial join
        joined = gpd.sjoin(point, districts, how="left")
        if joined.empty or pd.isna(joined.iloc[0]["NAME_2"]):
            return jsonify({"error": "Location not in Tamil Nadu districts"}), 400
            
        district_name = joined.iloc[0]["NAME_2"]

        # 3. Get NPK for District
        npk_row = npk_df[npk_df["district_name"].str.lower() == district_name.lower()]
        if not npk_row.empty:
            row = npk_row.iloc[0]
            total = row["total"]
            if total == 0: total = 1 # Avoid division by zero
            
            # Calculate weighted averages based on standard ranges
            # N: Low(<280), Med(280-560), High(>560) -> Midpoints: 140, 420, 700
            N = (row["n_low"] * 140 + row["n_med"] * 420 + row["n_high"] * 700) / total
            
            # P: Low(<11), Med(11-22), High(>22) -> Midpoints: 5.5, 16.5, 30
            P = (row["p_low"] * 5.5 + row["p_med"] * 16.5 + row["p_high"] * 30) / total
            
            # K: Low(<120), Med(120-280), High(>280) -> Midpoints: 60, 200, 350
            # Note: CSV has k_low, k_med, k_high (assuming column names match)
            # Let's check column names from file view: k_low, k_med, k_high are present
            K = (row["k_low"] * 60 + row["k_med"] * 200 + row["k_high"] * 350) / total
            
            # Round to 2 decimal places
            N = round(N, 2)
            P = round(P, 2)
            K = round(K, 2)
        else:
            # Fallback defaults
            N, P, K = 50, 50, 50

        # 4. Get Weather for District
        weather = get_weather(district_name)
        temp = weather["temperature"]
        hum = weather["humidity"]
        rain = weather["rainfall"]

        # 5. Predict
        prediction = predict_crop(N, P, K, temp, hum, ph, rain)

        return jsonify({
            "district": district_name,
            "soil": {
                "N": N, "P": P, "K": K, "pH": ph,
                "OC": clean_val(soil_row.get("OC_TN_0cm.tif")),
                "Texture": soil_row.get("TEX_TN_0cm.tif", "Unknown")
            },
            "weather": weather,
            "prediction": prediction
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/predict_manual", methods=["POST"])
def predict_manual():
    try:
        data = request.get_json()
        
        # Required fields
        N = float(data.get("N"))
        P = float(data.get("P"))
        K = float(data.get("K"))
        ph = float(data.get("ph"))
        district_name = data.get("district")

        # Get Weather based on district
        weather = get_weather(district_name)
        temp = weather["temperature"]
        hum = weather["humidity"]
        rain = weather["rainfall"]

        # Predict
        prediction = predict_crop(N, P, K, temp, hum, ph, rain)

        return jsonify({
            "district": district_name,
            "weather_used": weather,
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
