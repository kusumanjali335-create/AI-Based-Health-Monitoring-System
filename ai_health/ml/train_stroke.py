import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
data = pd.read_csv("ml/datasets/stroke.csv")

print("Dataset Loaded Successfully\n")

print(data.dtypes)

# Remove rows with missing values
data = data.dropna()

# Encode categorical columns
for column in data.columns:

    data[column] = data[column].astype(str).str.strip()

    try:
        data[column] = pd.to_numeric(data[column])

    except:
        encoder = LabelEncoder()
        data[column] = encoder.fit_transform(data[column])

# Remove ID column if present
if "id" in data.columns:
    data = data.drop("id", axis=1)

# Features
X = data.drop("stroke", axis=1)

# Target
y = data["stroke"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print(f"\nAccuracy : {accuracy*100:.2f}%")

joblib.dump(model, "ml/models/stroke_model.pkl")

print("\nStroke Model Saved Successfully!")