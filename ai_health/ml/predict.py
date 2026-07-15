import joblib
import pandas as pd

# Load Models
heart_model = joblib.load("ml/models/heart_model.pkl")
diabetes_model = joblib.load("ml/models/diabetes_model.pkl")
kidney_model = joblib.load("ml/models/kidney_model.pkl")
stroke_model = joblib.load("ml/models/stroke_model.pkl")


def predict_heart(data):
    prediction = heart_model.predict(data)
    return prediction[0]


def predict_diabetes(data):
    prediction = diabetes_model.predict(data)
    return prediction[0]


def predict_kidney(data):
    prediction = kidney_model.predict(data)
    return prediction[0]


def predict_stroke(data):
    prediction = stroke_model.predict(data)
    return prediction[0]