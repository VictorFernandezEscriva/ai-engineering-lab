import torch
import torch.nn as nn
from torchvision import datasets
from torchvision.transforms import ToTensor


# ============================================================
# 1. DESCARGAR DATASET
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
# 2. MIRAR UNA IMAGEN
# ============================================================

image, label = train_dataset[0]

print()
print("Image shape:", image.shape)
print("Label:", label)