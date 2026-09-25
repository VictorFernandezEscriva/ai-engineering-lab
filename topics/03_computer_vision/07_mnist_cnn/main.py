import torch
import torch.nn as nn

from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader


# ============================================================
# 1. LOAD MNIST
# ============================================================

train_dataset = datasets.MNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

test_dataset = datasets.MNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor()
)


# ============================================================
# 2. CREATE DATALOADERS
# ============================================================

batch_size = 64

train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False
)


print("Training samples:", len(train_dataset))
print("Test samples:", len(test_dataset))

print("Training batches:", len(train_loader))
print("Test batches:", len(test_loader))


# ============================================================
# 3. CREATE CNN
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
        32 * 7 * 7,
        10
    )
)


print()
print("MODEL:")
print(model)


# ============================================================
# 4. INSPECT ONE BATCH
# ============================================================

images, labels = next(
    iter(train_loader)
)

print()
print("ONE BATCH")

print(
    "Images shape:",
    images.shape
)

print(
    "Labels shape:",
    labels.shape
)


with torch.no_grad():

    initial_logits = model(images)


print(
    "Model output shape:",
    initial_logits.shape
)

print(
    "First image logits:",
    initial_logits[0]
)


# ============================================================
# 5. LOSS AND OPTIMIZER
# ============================================================

loss_function = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ============================================================
# 6. TRAINING
# ============================================================

epochs = 3

print()
print("Training...")


for epoch in range(epochs):

    model.train()

    running_loss = 0.0

    correct = 0
    total = 0


    for images, labels in train_loader:

        # Clear gradients from previous batch
        optimizer.zero_grad()

        # Forward pass
        logits = model(images)

        # Calculate loss
        loss = loss_function(
            logits,
            labels
        )

        # Backpropagation
        loss.backward()

        # Update parameters
        optimizer.step()


        running_loss += loss.item()


        # Highest logit determines predicted class
        predictions = torch.argmax(
            logits,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)


    average_loss = (
        running_loss
        / len(train_loader)
    )

    training_accuracy = (
        correct
        / total
    )


    print(
        f"Epoch {epoch + 1}/{epochs}, "
        f"Loss: {average_loss:.4f}, "
        f"Training accuracy: "
        f"{training_accuracy:.4f}"
    )


# ============================================================
# 7. TEST EVALUATION
# ============================================================

model.eval()

correct = 0
total = 0


with torch.no_grad():

    for images, labels in test_loader:

        logits = model(images)

        predictions = torch.argmax(
            logits,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)


test_accuracy = (
    correct
    / total
)


print()
print(
    "Test accuracy:",
    test_accuracy
)


# ============================================================
# 8. INSPECT SOME TEST PREDICTIONS
# ============================================================

images, labels = next(
    iter(test_loader)
)


with torch.no_grad():

    logits = model(images)

    probabilities = torch.softmax(
        logits,
        dim=1
    )

    predictions = torch.argmax(
        logits,
        dim=1
    )


print()
print("EXAMPLE TEST PREDICTIONS")


for i in range(10):

    confidence = probabilities[
        i,
        predictions[i]
    ].item()

    print(
        f"Image {i}: "
        f"Real={labels[i].item()}, "
        f"Predicted={predictions[i].item()}, "
        f"Confidence={confidence:.4f}"
    )