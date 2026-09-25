import torch
import torch.nn as nn
import numpy as np


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

# Add grayscale channel dimension:
# [batch, height, width]
# ->
# [batch, channels, height, width]
X = X.unsqueeze(1)

print("After adding channel:", X.shape)


# ============================================================
# 2. CREATE CNN
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
# 3. INSPECT INITIAL FORWARD PASS
# ============================================================

model.eval()

with torch.no_grad():
    initial_output = model(X[:5])

print("\nInitial output shape:")
print(initial_output.shape)

print("\nInitial raw output:")
print(initial_output)


# ============================================================
# 4. LOSS AND OPTIMIZER
# ============================================================

loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ============================================================
# 5. TRAIN CNN
# ============================================================

model.train()

for epoch in range(1000):

    # Clear gradients from the previous iteration
    optimizer.zero_grad()

    # Forward pass
    predictions = model(X)

    # Calculate training loss
    loss = loss_function(
        predictions,
        y.float().unsqueeze(1)
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
# 6. TRAINING ACCURACY
# ============================================================

model.eval()

with torch.no_grad():

    output = model(X)

    probabilities = torch.sigmoid(output)

    predictions = (
        probabilities >= 0.5
    ).long()

    training_accuracy = (
        predictions.squeeze(1) == y
    ).float().mean()


print(
    "\nTraining accuracy:",
    training_accuracy.item()
)


# ============================================================
# 7. INSPECT LEARNED CONVOLUTION FILTERS
# ============================================================

print("\nFIRST CONVOLUTION WEIGHT SHAPE:")
print(model[0].weight.shape)

print("\nSECOND CONVOLUTION WEIGHT SHAPE:")
print(model[3].weight.shape)

print("\nEXAMPLE LEARNED FILTER FROM FIRST CONVOLUTION:")
print(model[0].weight[0, 0].detach())