import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
data = pd.read_csv("ml/datasets/heart.csv")

print("Dataset Loaded Successfully\n")

# Remove missing values
data = data.dropna()

# Store encoders
label_encoders = {}

# Encode only categorical columns
for column in data.columns:

    if data[column].dtype == "object" or str(data[column].dtype) == "string":

        encoder = LabelEncoder()

        data[column] = encoder.fit_transform(
            data[column].astype(str).str.strip()
        )

        label_encoders[column] = encoder

print("Dataset Ready\n")

# ===========================
# ONLY BASIC FEATURES
# ===========================

X = data[
    [
        "age",
        "resting_blood_pressure",
        "Max_heart_rate"
    ]
]

y = data["target"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Train Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
prediction = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, prediction)

print(f"Accuracy : {accuracy*100:.2f}%")

# Save Model
joblib.dump(model, "ml/models/heart_model.pkl")

# Save Encoders
joblib.dump(label_encoders, "ml/models/heart_encoders.pkl")

print("\nHeart Model Saved Successfully!")
print("Heart Encoders Saved Successfully!")