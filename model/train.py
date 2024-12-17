import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

DATASET_PATH = './data/heart.csv'  
data = pd.read_csv(DATASET_PATH)

FEATURES = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
TARGET = 'target'


X = data[FEATURES]
y = data[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

MODEL_PATH = './model/model.pkl'
SCALER_PATH = './model/scaler.pkl'

with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)

with open(SCALER_PATH, 'wb') as f:
    pickle.dump(scaler, f)

print(f"Model saved to {MODEL_PATH}")
print(f"Scaler saved to {SCALER_PATH}")
