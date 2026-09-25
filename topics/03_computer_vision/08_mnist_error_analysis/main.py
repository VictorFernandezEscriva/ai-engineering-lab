import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix


# ============================================================
# 1. REPRODUCIBILITY
# ============================================================

torch.manual_seed(42)


# ============================================================
# 2. LOAD MNIST
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
# 3. CREATE DATALOADERS
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
        32 * 7 * 7,
        10
    )
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
# 6. TRAIN MODEL
# ============================================================

epochs = 3

print()
print("Training...")


for epoch in range(epochs):

    model.train()

    running_loss = 0.0

    for images, labels in train_loader:

        optimizer.zero_grad()

        logits = model(images)

        loss = loss_function(
            logits,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item()


    average_loss = (
        running_loss
        / len(train_loader)
    )

    print(
        f"Epoch {epoch + 1}/{epochs}, "
        f"Loss: {average_loss:.4f}"
    )


# ============================================================
# 7. COLLECT TEST PREDICTIONS
# ============================================================

model.eval()

all_labels = []
all_predictions = []

misclassified_images = []
misclassified_labels = []
misclassified_predictions = []


with torch.no_grad():

    for images, labels in test_loader:

        logits = model(images)

        predictions = torch.argmax(
            logits,
            dim=1
        )

        all_labels.extend(
            labels.tolist()
        )

        all_predictions.extend(
            predictions.tolist()
        )


        # Store misclassified samples
        incorrect_mask = (
            predictions != labels
        )

        incorrect_images = images[
            incorrect_mask
        ]

        incorrect_labels = labels[
            incorrect_mask
        ]

        incorrect_predictions = predictions[
            incorrect_mask
        ]


        for image, real, predicted in zip(
            incorrect_images,
            incorrect_labels,
            incorrect_predictions
        ):

            misclassified_images.append(
                image
            )

            misclassified_labels.append(
                real.item()
            )

            misclassified_predictions.append(
                predicted.item()
            )


# ============================================================
# 8. OVERALL ACCURACY
# ============================================================

correct = sum(
    real == predicted
    for real, predicted in zip(
        all_labels,
        all_predictions
    )
)

total = len(all_labels)

accuracy = correct / total


print()
print("OVERALL RESULTS")
print("=" * 50)

print(
    "Correct predictions:",
    correct
)

print(
    "Incorrect predictions:",
    total - correct
)

print(
    "Test accuracy:",
    accuracy
)


# ============================================================
# 9. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(range(10))
)


print()
print("CONFUSION MATRIX")
print()

print(cm)


# ============================================================
# 10. PER-CLASS ACCURACY
# ============================================================

print()
print("PER-CLASS ACCURACY")
print("=" * 50)


for digit in range(10):

    total_for_digit = cm[
        digit
    ].sum()

    correct_for_digit = cm[
        digit,
        digit
    ]

    class_accuracy = (
        correct_for_digit
        / total_for_digit
    )


    print(
        f"Digit {digit}: "
        f"{correct_for_digit}/{total_for_digit} "
        f"= {class_accuracy:.4f}"
    )


# ============================================================
# 11. MOST COMMON CONFUSIONS
# ============================================================

confusions = []

for real_digit in range(10):

    for predicted_digit in range(10):

        if real_digit == predicted_digit:
            continue

        count = cm[
            real_digit,
            predicted_digit
        ]

        if count > 0:

            confusions.append(
                (
                    count,
                    real_digit,
                    predicted_digit
                )
            )


confusions.sort(
    reverse=True
)


print()
print("MOST COMMON CONFUSIONS")
print("=" * 50)


for count, real_digit, predicted_digit in confusions[:10]:

    print(
        f"Real {real_digit} "
        f"predicted as {predicted_digit}: "
        f"{count}"
    )


# ============================================================
# 12. VISUALIZE MISCLASSIFIED IMAGES
# ============================================================

number_to_show = min(
    16,
    len(misclassified_images)
)


fig, axes = plt.subplots(
    4,
    4,
    figsize=(10, 10)
)


for i, ax in enumerate(axes.flat):

    if i < number_to_show:

        image = misclassified_images[i]

        real = misclassified_labels[i]

        predicted = (
            misclassified_predictions[i]
        )


        ax.imshow(
            image.squeeze(0),
            cmap="gray"
        )

        ax.set_title(
            f"Real: {real} | Pred: {predicted}"
        )

    ax.axis("off")


plt.tight_layout()
plt.show()