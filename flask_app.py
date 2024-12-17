from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

MODEL_PATH = './model/model.pkl'
SCALER_PATH = './model/scaler.pkl'

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)


@app.route('/')
def home():
    return redirect(url_for('predict'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
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
        prob = model.predict_proba(scaled_features)  # This returns probabilities for each class
        prediction = model.predict(scaled_features)[0]  # This returns the final prediction (0 or 1)
        probability = prob[0][1]  # This is the probability of the positive class (1)

        # Determine the result message
        result = "Positive for Heart Disease" if prediction == 1 else "Negative for Heart Disease"

        # Render the page with the prediction and probability
        return render_template('predict.html', result=result, probability=probability * 100)  # Multiply by 100 to get percentage

    # Render the form initially
    return render_template('predict.html', result=None, probability=None)




if __name__ == '__main__':
    app.run(debug=True)
