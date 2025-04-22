from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
import pandas as pd
import numpy as np
import json
from datetime import datetime

app = Flask(__name__)

MODEL_PATH = './model/model.pkl'
SCALER_PATH = './model/scaler.pkl'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# Feature descriptions for tooltips
FEATURE_DESCRIPTIONS = {
    'age': 'Age in years',
    'sex': 'Sex (1 = male; 0 = female)',
    'cp': 'Chest pain type (0 = typical angina; 1 = atypical angina; 2 = non-anginal pain; 3 = asymptomatic)',
    'trestbps': 'Resting blood pressure (mm Hg)',
    'chol': 'Serum cholesterol (mg/dl)',
    'fbs': 'Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)',
    'restecg': 'Resting electrocardiographic results (0 = normal; 1 = ST-T wave abnormality; 2 = probable or definite left ventricular hypertrophy)',
    'thalach': 'Maximum heart rate achieved during exercise',
    'exang': 'Exercise induced angina (1 = yes; 0 = no)',
    'oldpeak': 'ST depression induced by exercise relative to rest',
    'slope': 'Slope of the peak exercise ST segment (0 = upsloping; 1 = flat; 2 = downsloping)',
    'ca': 'Number of major vessels (0-3) colored by fluoroscopy',
    'thal': 'Thalassemia (3 = normal; 6 = fixed defect; 7 = reversible defect)'
}

# Risk factor information
RISK_FACTORS = [
    {
        'title': 'High Blood Pressure',
        'description': 'Hypertension forces your heart to work harder to pump blood, which can lead to heart disease.',
        'icon': 'fa-heartbeat',
        'image': 'risk-factors.jpg'
    },
    {
        'title': 'High Cholesterol',
        'description': 'Excess cholesterol can build up in your arteries, narrowing them and increasing heart disease risk.',
        'icon': 'fa-chart-line',
        'image': 'risk-factors.jpg'
    },
    {
        'title': 'Diabetes',
        'description': 'High blood sugar levels can damage blood vessels and nerves that control your heart.',
        'icon': 'fa-syringe',
        'image': 'risk-factors.jpg'
    },
    {
        'title': 'Obesity',
        'description': 'Excess weight increases strain on your heart and is linked to other risk factors.',
        'icon': 'fa-weight',
        'image': 'risk-factors.jpg'
    }
]

PREVENTION_TIPS = [
    {
        'title': 'Healthy Diet',
        'description': 'Eat plenty of fruits, vegetables, whole grains, and lean proteins. Limit saturated fats and sodium.',
        'icon': 'fa-apple-alt',
        'image': 'prevention.jpg'
    },
    {
        'title': 'Regular Exercise',
        'description': 'Aim for at least 150 minutes of moderate exercise per week to strengthen your heart.',
        'icon': 'fa-running',
        'image': 'prevention.jpg'
    },
    {
        'title': 'No Smoking',
        'description': 'Smoking damages blood vessels and significantly increases heart disease risk.',
        'icon': 'fa-smoking-ban',
        'image': 'prevention.jpg'
    },
    {
        'title': 'Stress Management',
        'description': 'Chronic stress may contribute to heart disease. Practice relaxation techniques.',
        'icon': 'fa-spa',
        'image': 'prevention.jpg'
    }
]

@app.route('/')
def home():
    return redirect(url_for('predict'))

@app.route('/about')
def about():
    return render_template('about.html', 
                         feature_descriptions=FEATURE_DESCRIPTIONS,
                         risk_factors=RISK_FACTORS,
                         prevention_tips=PREVENTION_TIPS)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            features = [
                float(request.form['age']),
                float(request.form['sex']),
                float(request.form['cp']),
                float(request.form['trestbps']),
                float(request.form['chol']),
                float(request.form['fbs']),
                float(request.form['restecg']),
                float(request.form['thalach']),
                float(request.form['exang']),
                float(request.form['oldpeak']),
                float(request.form['slope']),
                float(request.form['ca']),
                float(request.form['thal']),
            ]

            # Scale the input features
            scaled_features = scaler.transform([features])

            # Get both prediction and probability
            prob = model.predict_proba(scaled_features)
            prediction = model.predict(scaled_features)[0]
            probability = prob[0][1] * 100  # Convert to percentage

            # Prepare data for visualization
            feature_names = ['Age', 'Sex', 'Chest Pain', 'Blood Pressure', 'Cholesterol', 
                           'Blood Sugar', 'ECG', 'Max HR', 'Exercise Angina', 'ST Depression', 
                           'Slope', 'Vessels', 'Thalassemia']
            
            # Get feature importance if available
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
            else:
                importance = [1/len(feature_names)] * len(feature_names)
            
            feature_data = list(zip(feature_names, features, importance))
            feature_data.sort(key=lambda x: x[2], reverse=True)

            result_data = {
                'prediction': int(prediction),
                'probability': round(probability, 2),
                'features': [
                    {'name': name, 'value': val, 'importance': imp} 
                    for name, val, imp in feature_data
                ],
                'timestamp': datetime.now().strftime("%B %d, %Y at %H:%M")
            }

            return render_template('predict.html', 
                                 result=result_data,
                                 feature_descriptions=FEATURE_DESCRIPTIONS,
                                 risk_factors=RISK_FACTORS,
                                 prevention_tips=PREVENTION_TIPS)
        
        except Exception as e:
            return render_template('predict.html', 
                                 error=f"An error occurred: {str(e)}",
                                 feature_descriptions=FEATURE_DESCRIPTIONS,
                                 risk_factors=RISK_FACTORS,
                                 prevention_tips=PREVENTION_TIPS)

    return render_template('predict.html', 
                         feature_descriptions=FEATURE_DESCRIPTIONS,
                         risk_factors=RISK_FACTORS,
                         prevention_tips=PREVENTION_TIPS)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        features = [
            float(data['age']),
            float(data['sex']),
            float(data['cp']),
            float(data['trestbps']),
            float(data['chol']),
            float(data['fbs']),
            float(data['restecg']),
            float(data['thalach']),
            float(data['exang']),
            float(data['oldpeak']),
            float(data['slope']),
            float(data['ca']),
            float(data['thal']),
        ]
        
        scaled_features = scaler.transform([features])
        prob = model.predict_proba(scaled_features)
        
        return jsonify({
            'prediction': int(model.predict(scaled_features)[0]),
            'probability': float(prob[0][1]),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        })

if __name__ == '__main__':
    app.run(debug=True)