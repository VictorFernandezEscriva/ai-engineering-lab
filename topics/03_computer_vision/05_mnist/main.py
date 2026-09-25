import torch
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD MNIST DATASET
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


print("Training samples:", len(train_dataset))
print("Test samples:", len(test_dataset))


# ============================================================
# 2. INSPECT ONE SAMPLE
# ============================================================

image, label = train_dataset[0]


print()
print("Image type:", type(image))
print("Image shape:", image.shape)
print("Image dtype:", image.dtype)

print(
    "Pixel value range:",
    image.min().item(),
    "to",
    image.max().item()
)

print("Label:", label)


# ============================================================
# 3. UNDERSTAND THE SAMPLE STRUCTURE
# ============================================================

print()
print("Channels:", image.shape[0])
print("Height:", image.shape[1])
print("Width:", image.shape[2])

# ============================================================
# 4. VISUALIZE EXAMPLE IMAGES
# ============================================================

fig, axes = plt.subplots(
    2,
    5,
    figsize=(10, 5)
)

for i, ax in enumerate(axes.flat):

    image, label = train_dataset[i]

    ax.imshow(
        image.squeeze(0),
        cmap="gray"
    )

    ax.set_title(
        f"Label: {label}"
    )

    ax.axis("off")


plt.tight_layout()
plt.show()