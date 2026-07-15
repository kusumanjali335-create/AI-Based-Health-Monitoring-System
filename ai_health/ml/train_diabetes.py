import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
data = pd.read_csv("ml/datasets/diabetes.csv")

print("Dataset Loaded Successfully\n")

print(data.dtypes)

# Remove Missing Values
data = data.dropna()

# Convert Categorical Columns
for column in data.columns:

    data[column] = data[column].astype(str).str.strip()

    try:
        data[column] = pd.to_numeric(data[column])

    except:

        encoder = LabelEncoder()

        data[column] = encoder.fit_transform(data[column])

# Features
X = data.drop("Outcome", axis=1)

# Target
y = data["Outcome"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print(f"\nAccuracy : {accuracy*100:.2f}%")

joblib.dump(model, "ml/models/diabetes_model.pkl")

print("\nDiabetes Model Saved Successfully!")