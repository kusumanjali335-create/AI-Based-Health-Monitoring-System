import pandas as pd

data = pd.read_csv("ml/datasets/heart.csv")

for column in data.columns:
    print("\n----------------------------")
    print(column)
    print(data[column].unique())