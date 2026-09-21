import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


# ============================================================
# 1. GENERATE DATA
# ============================================================

torch.manual_seed(42)

n = 200

temperature = torch.normal(80.0, 8.0, (n,))
vibration = torch.normal(0.6, 0.25, (n,))
rpm = torch.normal(4800.0, 300.0, (n,))
pressure = torch.normal(2.3, 0.15, (n,))

X = torch.column_stack([
    temperature,
    vibration,
    rpm,
    pressure
])


# ============================================================
# 2. GENERATE LABELS
# ============================================================

y = ((temperature > 85) & (vibration > 0.7)).float()
y = y.unsqueeze(1)


# ============================================================
# 3. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

print("Training samples:", len(X_train))
print("Test samples:", len(X_test))


# ============================================================
# 4. SAVE ORIGINAL TEST VALUES
# ============================================================

X_test_original = X_test.clone()


# ============================================================
# 5. NORMALIZATION
# ============================================================

# Reuse training statistics so the held-out samples do not influence preprocessing.
mean = X_train.mean(dim=0)
std = X_train.std(dim=0)

X_train = (X_train - mean) / std
X_test = (X_test - mean) / std


# ============================================================
# 6. CREATE NEURAL NETWORK
# ============================================================

model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)


# ============================================================
# 7. LOSS + OPTIMIZER
# ============================================================

loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)


# ============================================================
# 8. TRAINING
# ============================================================

for epoch in range(1000):

    predictions = model(X_train)

    loss = loss_function(
        predictions,
        y_train
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if epoch % 100 == 0:

        print(
            f"Epoch {epoch}, "
            f"Loss: {loss.item():.4f}"
        )


# ============================================================
# 9. TRAINING ACCURACY
# ============================================================

with torch.no_grad():

    train_output = model(X_train)

    train_probability = torch.sigmoid(
        train_output
    )

    train_prediction = (
        train_probability >= 0.5
    ).float()

    train_accuracy = (
        train_prediction == y_train
    ).float().mean()


# ============================================================
# 10. TEST PROBABILITIES
# ============================================================

with torch.no_grad():

    test_output = model(X_test)

    test_probability = torch.sigmoid(
        test_output
    )


# ============================================================
# 11. TEST WITH DIFFERENT THRESHOLDS
# ============================================================

thresholds = [0.3, 0.5, 0.7]

y_true = y_test.numpy().ravel()

for threshold in thresholds:

    test_prediction = (
        test_probability >= threshold
    ).float()

    y_pred = test_prediction.numpy().ravel()

    print()
    print("=" * 40)
    print(f"THRESHOLD: {threshold}")
    print("=" * 40)

    print("Confusion matrix:")

    print(
        confusion_matrix(
            y_true,
            y_pred
        )
    )

    print(
        "Precision:",
        precision_score(
            y_true,
            y_pred
        )
    )

    print(
        "Recall:",
        recall_score(
            y_true,
            y_pred
        )
    )

    print(
        "F1-score:",
        f1_score(
            y_true,
            y_pred
        )
    )


# ============================================================
# 12. SHOW TRAINING ACCURACY
# ============================================================

print()
print("=" * 60)
print("GENERAL RESULTS")
print("=" * 60)

print(
    "Training accuracy:",
    train_accuracy.item()
)


# ============================================================
# 13. ANALYZE ONE MOTOR STEP BY STEP
# ============================================================

i = 0

x_original = X_test_original[i]

x_normalized = X_test[i]


print()
print("=" * 60)
print("STEP-BY-STEP ANALYSIS OF ONE MOTOR")
print("=" * 60)


# ------------------------------------------------------------
# Original values
# ------------------------------------------------------------

print()
print("1. ORIGINAL VALUES")

print(
    "Temperature:",
    x_original[0].item()
)

print(
    "Vibration:  ",
    x_original[1].item()
)

print(
    "RPM:        ",
    x_original[2].item()
)

print(
    "Pressure:   ",
    x_original[3].item()
)


# ------------------------------------------------------------
# Normalized values
# ------------------------------------------------------------

print()
print("2. NORMALIZED VALUES")

print(x_normalized)


# ------------------------------------------------------------
# First layer
# ------------------------------------------------------------

with torch.no_grad():

    first_layer_output = model[0](
        x_normalized
    )


print()
print("3. FIRST LAYER - BEFORE ReLU")

print(first_layer_output)


# ------------------------------------------------------------
# ReLU
# ------------------------------------------------------------

with torch.no_grad():

    relu_output = model[1](
        first_layer_output
    )


print()
print("4. FIRST LAYER - AFTER ReLU")

print(relu_output)


# ------------------------------------------------------------
# Second layer
# ------------------------------------------------------------

with torch.no_grad():

    second_layer_output = model[2](
        relu_output
    )


print()
print("5. SECOND LAYER OUTPUT - LOGIT")

print(
    second_layer_output.item()
)


# ------------------------------------------------------------
# Sigmoid
# ------------------------------------------------------------

with torch.no_grad():

    probability = torch.sigmoid(
        second_layer_output
    )


print()
print("6. SIGMOID - PROBABILITY")

print(
    probability.item()
)


# ------------------------------------------------------------
# Final decision
# ------------------------------------------------------------

threshold = 0.5

if probability.item() >= threshold:

    prediction = "FAILURE"

else:

    prediction = "NORMAL"


print()
print("7. FINAL DECISION")

print(
    "Threshold:",
    threshold
)

print(
    "Prediction:",
    prediction
)

print(
    "Real value:",
    int(y_test[i].item())
)


# ============================================================
# 14. SHOW THE NETWORK WEIGHTS
# ============================================================

print()
print("=" * 60)
print("NETWORK WEIGHTS")
print("=" * 60)

print()
print("FIRST LAYER WEIGHTS")

print(model[0].weight)

print()
print("FIRST LAYER BIAS")

print(model[0].bias)

print()
print("SECOND LAYER WEIGHTS")

print(model[2].weight)

print()
print("SECOND LAYER BIAS")

print(model[2].bias)
