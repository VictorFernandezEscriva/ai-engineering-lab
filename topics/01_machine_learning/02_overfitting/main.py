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
# ---------------------------------------------------------------------------
# Model 1: depth-limited tree
# ---------------------------------------------------------------------------

limited_model = DecisionTreeClassifier(
    random_state=42,
    max_depth=2
)

limited_model.fit(X_train, y_train)

limited_train_predictions = limited_model.predict(X_train)
limited_test_predictions = limited_model.predict(X_test)

limited_train_accuracy = accuracy_score(
    y_train,
    limited_train_predictions
)

limited_test_accuracy = accuracy_score(
    y_test,
    limited_test_predictions
)

limited_gap = limited_train_accuracy - limited_test_accuracy


# ---------------------------------------------------------------------------
# Model 2: unrestricted tree
# ---------------------------------------------------------------------------

unrestricted_model = DecisionTreeClassifier(
    random_state=42,
    max_depth=None
)

unrestricted_model.fit(X_train, y_train)

unrestricted_train_predictions = unrestricted_model.predict(X_train)
unrestricted_test_predictions = unrestricted_model.predict(X_test)

unrestricted_train_accuracy = accuracy_score(
    y_train,
    unrestricted_train_predictions
)

unrestricted_test_accuracy = accuracy_score(
    y_test,
    unrestricted_test_predictions
)

unrestricted_gap = (
    unrestricted_train_accuracy -
    unrestricted_test_accuracy
)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

print("Realized label noise:", noise.sum(), "/", n)

print("\nLIMITED TREE")
print("Max depth:", limited_model.get_depth())
print("Number of leaves:", limited_model.get_n_leaves())
print("Training accuracy:", limited_train_accuracy)
print("Test accuracy:", limited_test_accuracy)
print("Generalization gap:", limited_gap)

print("\nUNRESTRICTED TREE")
print("Max depth:", unrestricted_model.get_depth())
print("Number of leaves:", unrestricted_model.get_n_leaves())
print("Training accuracy:", unrestricted_train_accuracy)
print("Test accuracy:", unrestricted_test_accuracy)
print("Generalization gap:", unrestricted_gap)