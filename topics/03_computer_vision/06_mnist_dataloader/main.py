import torch

from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader


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


print()
print("Batch size:", batch_size)

print(
    "Training batches:",
    len(train_loader)
)

print(
    "Test batches:",
    len(test_loader)
)


# ============================================================
# 3. GET ONE TRAINING BATCH
# ============================================================

images, labels = next(
    iter(train_loader)
)


print()
print("ONE TRAINING BATCH")

print(
    "Images shape:",
    images.shape
)

print(
    "Labels shape:",
    labels.shape
)


# ============================================================
# 4. INSPECT BATCH CONTENT
# ============================================================

print()
print("First 10 labels:")

print(
    labels[:10]
)


print()
print(
    "First image shape:",
    images[0].shape
)

print(
    "First image label:",
    labels[0].item()
)


# ============================================================
# 5. ITERATE THROUGH A FEW BATCHES
# ============================================================

print()
print("FIRST THREE BATCHES")

for batch_index, (images, labels) in enumerate(train_loader):

    print(
        f"Batch {batch_index}: "
        f"images={images.shape}, "
        f"labels={labels.shape}"
    )

    if batch_index == 2:
        break