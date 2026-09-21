import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Para que los resultados sean reproducibles
np.random.seed(42)

# Generamos 200 motores
n = 200

temperature = np.random.normal(80, 8, n)
vibration = np.random.normal(0.6, 0.25, n)
rpm = np.random.normal(4800, 300, n)
pressure = np.random.normal(2.3, 0.15, n)

# Regla "real" que genera los fallos
failure = (
    (temperature > 85) &
    (vibration > 0.7)
).astype(int)

# Añadimos algo de ruido
noise = np.random.random(n) < 0.05
failure[noise] = 1 - failure[noise]

# Crear X e y
X = np.column_stack([
    temperature,
    vibration,
    rpm,
    pressure
])

y = failure

# Train / Test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# Árbol CON LIMITACIONES
model = DecisionTreeClassifier(
    random_state=42,
    max_depth=2
)

model.fit(X_train, y_train)

# Predicciones
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, train_predictions)
test_accuracy = accuracy_score(y_test, test_predictions)

print("Training accuracy:", train_accuracy)
print("Test accuracy:", test_accuracy)