import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Dataset
data = {
    "moisture": [20, 30, 60, 80],
    "temperature": [30, 35, 25, 20],
    "irrigation": [1, 1, 0, 0]
}

df = pd.DataFrame(data)

X = df[["moisture", "temperature"]]
y = df["irrigation"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

# Test
prediction = model.predict(pd.DataFrame([[25, 32]], columns=["moisture", "temperature"]))
print("Irrigation Needed:", prediction[0])