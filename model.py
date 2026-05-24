from sklearn.linear_model import LogisticRegression
import numpy as np

# Dummy training data
X = np.array([
    [80, 90, 5, 75],
    [30, 40, 1, 35],
    [60, 70, 3, 55],
    [20, 30, 1, 25],
    [90, 95, 6, 85]
])

y = np.array([1, 0, 1, 0, 1])  # 1 = Pass, 0 = Fail

# Train model
model = LogisticRegression()
model.fit(X, y)