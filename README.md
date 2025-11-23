# 🌱 AgriSmart - Intelligent Crop Recommendation System

AgriSmart is a Flask-based web application that uses Machine Learning (Random Forest) and Geospatial Data to recommend the best crops for farmers in Tamil Nadu.

## 🚀 Features
*   **Auto Prediction**: Automatically detects your location (District) and fetches soil/weather data to suggest crops.
*   **Farmer Mode**: Manual input for Soil Health Card (SHC) parameters (N, P, K, pH).
*   **Top 3 Recommendations**: Suggests the best 3 crops with alternatives.
*   **Real Data**: Trained on standard agricultural datasets.
*   **Modern UI**: Glassmorphism design, fully responsive for mobile.

## 🛠️ Prerequisites
*   **Python 3.8+** installed on your system.
*   **Git** (optional, for cloning).

## 📥 Installation

1.  **Clone the Repository** (or download the zip):
    ```bash
    git clone https://github.com/JabezMatthewS/AgriSmart.git
    cd AgriSmart
    ```

2.  **Create a Virtual Environment** (Recommended):
    *   **Windows**:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **Mac/Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Running the App

1.  **Start the Server**:
    ```bash
    python app.py
    ```

2.  **Open in Browser**:
    *   Go to: `http://127.0.0.1:5000`

## 📂 Project Structure
*   `app.py`: Main Flask application logic.
*   `train_model.py`: Script to retrain the ML model.
*   `templates/index.html`: Frontend UI.
*   `static/style.css`: Styling.
*   `TN_soil_dataset.csv.gz`: Compressed soil data.
*   `TN_districts.shp`: Shapefile for district detection.

## 🤖 ML Model
The model uses a **Random Forest Classifier** trained on `Crop_recommendation.csv` (Kaggle dataset).
*   **Accuracy**: ~99%
*   **Inputs**: N, P, K, Temperature, Humidity, pH, Rainfall.

---
*Built for Sem 5 Project.*
