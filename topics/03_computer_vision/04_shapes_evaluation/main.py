import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


# ============================================================
# 1. GENERATE DATASET
# ============================================================

torch.manual_seed(42)
np.random.seed(42)

n_images = 1000
image_size = 32

images = []
labels = []

for _ in range(n_images):

    image = np.zeros(
        (image_size, image_size),
        dtype=np.float32
    )

    # Random shape position
    x = np.random.randint(8, 24)
    y = np.random.randint(8, 24)

    # 0 = circle
    # 1 = square
    label = np.random.randint(0, 2)

    if label == 0:

        # Draw a circle
        for row in range(image_size):
            for col in range(image_size):

                distance = np.sqrt(
                    (row - y) ** 2
                    + (col - x) ** 2
                )

                if distance < 6:
                    image[row, col] = 1.0

    else:

        # Draw a square
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
# 2. ADD CHANNEL DIMENSION
# ============================================================

# [batch, height, width]
# ->
# [batch, channels, height, width]
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

print(
    "Training circles:",
    int((y_train == 0).sum())
)

print(
    "Training squares:",
    int((y_train == 1).sum())
)

print(
    "Test circles:",
    int((y_test == 0).sum())
)

print(
    "Test squares:",
    int((y_test == 1).sum())
)


# ============================================================
# 4. CREATE CNN
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

print("\nMODEL:")
print(model)


# ============================================================
# 5. LOSS AND OPTIMIZER
# ============================================================

loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ============================================================
# 6. TRAINING
# ============================================================

print("\nTraining...")

model.train()

for epoch in range(1000):

    # Clear gradients from the previous iteration
    optimizer.zero_grad()

    # Forward pass using training data only
    predictions = model(X_train)

    # Calculate training loss
    loss = loss_function(
        predictions,
        y_train.float().unsqueeze(1)
    )

    # Calculate gradients
    loss.backward()

    # Update convolution and linear parameters
    optimizer.step()

    if (epoch + 1) % 100 == 0:

        print(
            f"Epoch {epoch + 1}, "
            f"Loss: {loss.item():.4f}"
        )


# ============================================================
# 7. EVALUATE TRAINING DATA
# ============================================================

model.eval()

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

generalization_gap = (
    train_accuracy - test_accuracy
)


print("\nGENERAL RESULTS")
print("=" * 50)

print(
    "Training accuracy:",
    train_accuracy
)

print(
    "Test accuracy:",
    test_accuracy
)

print(
    "Generalization gap:",
    generalization_gap
)


# ============================================================
# 9. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test.numpy(),
    test_predictions.numpy(),
    labels=[0, 1]
)

print("\nConfusion matrix:")
print(cm)

print(
    "\nMatrix layout:"
)

print(
    "[[correct circles, circles predicted as squares],"
)

print(
    " [squares predicted as circles, correct squares]]"
)


# ============================================================
# 10. INSPECT EXAMPLE PREDICTIONS
# ============================================================

print("\nExample predictions:")

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


# ============================================================
# 11. INSPECT FIRST CONVOLUTION FILTERS
# ============================================================

print("\nFIRST CONVOLUTION FILTERS:")

filters = model[0].weight.detach()

print(
    "Filter tensor shape:",
    filters.shape
)

for i in range(16):

    print()
    print(f"Filter {i}:")
    print(filters[i, 0])


# ============================================================
# 12. INSPECT FIRST-LAYER FEATURE MAPS
# ============================================================

# Select one unseen test image
image = X_test[0:1]

with torch.no_grad():

    first_feature_maps = model[0](image)


print(
    "\nInput shape:",
    image.shape
)

print(
    "First convolution feature maps shape:",
    first_feature_maps.shape
)


# Show original image
plt.figure(figsize=(4, 4))

plt.imshow(
    image[0, 0],
    cmap="gray"
)

plt.title("Original image")
plt.axis("off")
plt.show()


# Show 16 first-layer feature maps
fig, axes = plt.subplots(
    4,
    4,
    figsize=(10, 10)
)

for i, ax in enumerate(axes.flat):

    ax.imshow(
        first_feature_maps[0, i],
        cmap="gray"
    )

    ax.set_title(
        f"Conv1 Filter {i}"
    )

    ax.axis("off")

plt.tight_layout()
plt.show()


# ============================================================
# 13. INSPECT SECOND-LAYER FEATURE MAPS
# ============================================================

with torch.no_grad():

    # First convolutional block
    x = model[0](image)
    x = model[1](x)
    x = model[2](x)

    print(
        "\nAfter Conv1 + ReLU + MaxPool:",
        x.shape
    )

    # Second convolution
    second_feature_maps = model[3](x)


print(
    "After Conv2:",
    second_feature_maps.shape
)


# Show the first 16 of the 32 second-layer feature maps
fig, axes = plt.subplots(
    4,
    4,
    figsize=(10, 10)
)

for i, ax in enumerate(axes.flat):

    ax.imshow(
        second_feature_maps[0, i],
        cmap="gray"
    )

    ax.set_title(
        f"Conv2 Filter {i}"
    )

    ax.axis("off")

plt.tight_layout()
plt.show()