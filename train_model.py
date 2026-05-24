import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# SAMPLE DATA

data = {
    'marks': [90, 40, 70, 30, 80],
    'attendance': [90, 50, 80, 40, 95],
    'study_hours': [5, 1, 4, 1, 6],
    'previous_score': [85, 35, 65, 30, 88],
    'result': [1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df[['marks', 'attendance', 'study_hours', 'previous_score']]
y = df['result']

model = LogisticRegression()
model.fit(X, y)

pickle.dump(model, open('model.pkl', 'wb'))

print("Model saved successfully!")