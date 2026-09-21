import torch
import torch.nn as nn
import numpy as np

# --------------------------------------------------
# 1. GENERATE DATASET
# --------------------------------------------------

torch.manual_seed(42)
np.random.seed(42)

n_images = 1000
image_size = 32

images = []
labels = []

for i in range(n_images):

    image = np.zeros((image_size, image_size), dtype=np.float32)

    # Random position
    x = np.random.randint(8, 24)
    y = np.random.randint(8, 24)

    # 0 = circle
    # 1 = square
    label = np.random.randint(0, 2)

    if label == 0:

        # Circle
        for row in range(image_size):
            for col in range(image_size):

                distance = np.sqrt(
                    (row - y) ** 2 +
                    (col - x) ** 2
                )

                if distance < 6:
                    image[row, col] = 1.0

    else:

        # Square
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

X = X.unsqueeze(1)

print("After adding channel:", X.shape)

# --------------------------------------------------
# 2. CNN MODEL
# --------------------------------------------------

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

print(model)

# --------------------------------------------------
# 3. FORWARD PASS
# --------------------------------------------------

with torch.no_grad():

    output = model(X[:5])

print()
print("Output shape:", output.shape)
print("Raw output:")
print(output)

loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

for epoch in range(1000):

    predictions = model(X)

    loss = loss_function(
        predictions,
        y.float().unsqueeze(1)
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(
            f"Epoch {epoch + 1}, "
            f"Loss: {loss.item():.4f}"
        )