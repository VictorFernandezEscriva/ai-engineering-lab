import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix



# ============================================================
# 1. GENERAR DATASET
# ============================================================

torch.manual_seed(42)
np.random.seed(42)

n_images = 1000
image_size = 32

images = []
labels = []

for i in range(n_images):

    image = np.zeros((image_size, image_size), dtype=np.float32)

    x = np.random.randint(8, 24)
    y = np.random.randint(8, 24)

    # 0 = circle
    # 1 = square
    label = np.random.randint(0, 2)

    if label == 0:

        for row in range(image_size):
            for col in range(image_size):

                distance = np.sqrt(
                    (row - y) ** 2 +
                    (col - x) ** 2
                )

                if distance < 6:
                    image[row, col] = 1.0

    else:

        image[
            y - 5:y + 6,
            x - 5:x + 6
        ] = 1.0

    images.append(image)
    labels.append(label)


X = torch.tensor(np.array(images))
y = torch.tensor(labels)

print("Dataset shape:", X.shape)
print("Labels shape:", y.shape)


# ============================================================
# 2. AÑADIR CANAL
# ============================================================

X = X.unsqueeze(1)

print("After adding channel:", X.shape)


# ============================================================
# 3. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training images:", X_train.shape)
print("Test images:", X_test.shape)


# ============================================================
# 4. CNN
# ============================================================

model = nn.Sequential(

    nn.Conv2d(
        in_channels=1,
        out_channels=16,
        kernel_size=3,
        padding=1
    ),

    nn.ReLU(),

    nn.MaxPool2d(
        kernel_size=2
    ),

    nn.Conv2d(
        in_channels=16,
        out_channels=32,
        kernel_size=3,
        padding=1
    ),

    nn.ReLU(),

    nn.MaxPool2d(
        kernel_size=2
    ),

    nn.Flatten(),

    nn.Linear(
        32 * 8 * 8,
        1
    )
)

print()
print(model)


# ============================================================
# 5. LOSS + OPTIMIZER
# ============================================================

loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ============================================================
# 6. TRAINING
# ============================================================

print()
print("Training...")

for epoch in range(1000):

    # Forward pass
    predictions = model(X_train)

    # Calculate loss
    loss = loss_function(
        predictions,
        y_train.float().unsqueeze(1)
    )

    # Backpropagation
    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 100 == 0:

        print(
            f"Epoch {epoch + 1}, "
            f"Loss: {loss.item():.4f}"
        )


# ============================================================
# 7. EVALUATE TRAINING DATA
# ============================================================

with torch.no_grad():

    train_logits = model(X_train)

    train_probabilities = torch.sigmoid(
        train_logits
    )

    train_predictions = (
        train_probabilities >= 0.5
    ).int().squeeze(1)


train_accuracy = accuracy_score(
    y_train.numpy(),
    train_predictions.numpy()
)


# ============================================================
# 8. EVALUATE TEST DATA
# ============================================================

with torch.no_grad():

    test_logits = model(X_test)

    test_probabilities = torch.sigmoid(
        test_logits
    )

    test_predictions = (
        test_probabilities >= 0.5
    ).int().squeeze(1)


test_accuracy = accuracy_score(
    y_test.numpy(),
    test_predictions.numpy()
)


print()
print("Training accuracy:", train_accuracy)
print("Test accuracy:", test_accuracy)


# ============================================================
# 9. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test.numpy(),
    test_predictions.numpy()
)

print()
print("Confusion matrix:")
print(cm)


# ============================================================
# 10. EXAMINAR ALGUNAS PREDICCIONES
# ============================================================

print()
print("Example predictions:")

for i in range(10):

    real = y_test[i].item()

    predicted = test_predictions[i].item()

    probability = test_probabilities[i].item()

    print(
        f"Image {i}: "
        f"Real={real}, "
        f"Predicted={predicted}, "
        f"Probability={probability:.4f}"
    )

print()
print("FIRST CONVOLUTION FILTERS:")

filters = model[0].weight.detach()

print("Filter tensor shape:", filters.shape)

for i in range(16):

    print()
    print(f"Filter {i}:")
    print(filters[i, 0])



# Cogemos una imagen del conjunto de test
image = X_test[0:1]

# Pasamos la imagen solamente por la primera convolución
with torch.no_grad():
    feature_maps = model[0](image)


print()
print("Input shape:", image.shape)
print("Feature maps shape:", feature_maps.shape)


# Dibujar la imagen original
plt.figure(figsize=(4, 4))
plt.imshow(image[0, 0], cmap="gray")
plt.title("Original image")
plt.axis("off")
plt.show()


# Dibujar los 16 feature maps
fig, axes = plt.subplots(4, 4, figsize=(10, 10))

for i, ax in enumerate(axes.flat):

    ax.imshow(
        feature_maps[0, i],
        cmap="gray"
    )

    ax.set_title(f"Filter {i}")
    ax.axis("off")

plt.tight_layout()
plt.show()

# ============================================================
# VISUALIZAR SEGUNDA CONVOLUCIÓN
# ============================================================

# Cogemos una imagen del conjunto de test
image = X_test[0:1]

with torch.no_grad():

    # Primera convolución + ReLU + MaxPool
    x = model[0](image)
    x = model[1](x)
    x = model[2](x)

    # Segunda convolución
    second_feature_maps = model[3](x)


print()
print("After Conv1 + ReLU + MaxPool:", x.shape)
print("After Conv2:", second_feature_maps.shape)


# Mostrar algunos feature maps de la segunda convolución

fig, axes = plt.subplots(4, 4, figsize=(10, 10))

for i, ax in enumerate(axes.flat):

    ax.imshow(
        second_feature_maps[0, i],
        cmap="gray"
    )

    ax.set_title(f"Conv2 Filter {i}")
    ax.axis("off")

plt.tight_layout()
plt.show()