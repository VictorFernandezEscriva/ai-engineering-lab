import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text


data = {
    "temperature": [70, 72, 75, 80, 82, 85, 88, 90, 93, 95],
    "vibration":   [0.2, 0.3, 0.2, 0.4, 0.5, 0.7, 0.9, 1.2, 1.5, 1.7],
    "rpm":         [4500, 4600, 4700, 4800, 4850, 4900, 5000, 5100, 5150, 5200],
    "pressure":    [2.1, 2.2, 2.1, 2.2, 2.2, 2.3, 2.3, 2.4, 2.4, 2.5],
    "failure":     [0, 0, 1, 0, 0, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

print(df)

# Keep the target out of the input features to avoid leaking the answer.
X = df[["temperature", "vibration", "rpm", "pressure"]]
y = df["failure"]

print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(
    criterion="gini",
    random_state=42
)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Test targets:", y_test.to_numpy())
print("Test predictions:", predictions)

accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

new_motor = pd.DataFrame({
    "temperature": [87],
    "vibration": [0.8],
    "rpm": [4950],
    "pressure": [2.3]
})

prediction = model.predict(new_motor)
print("Prediction for additional motor:", prediction)

print(export_text(model, feature_names=list(X.columns)))