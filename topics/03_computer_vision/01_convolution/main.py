import torch
import torch.nn as nn


# ============================================================
# 1. CREATE IMAGE
# ============================================================

image = torch.tensor([
    [0., 0., 0., 0., 0.],
    [0., 1., 1., 1., 0.],
    [0., 1., 1., 1., 0.],
    [0., 1., 1., 1., 0.],
    [0., 0., 0., 0., 0.]
])

print("IMAGE:")
print(image)

print("\nOriginal image shape:")
print(image.shape)


# ============================================================
# 2. CREATE KERNEL
# ============================================================

kernel = torch.tensor([
    [-1., 1.],
    [-1., 1.]
])

print("\nKERNEL:")
print(kernel)


# ============================================================
# 3. ADD BATCH AND CHANNEL DIMENSIONS
# ============================================================

image = image.unsqueeze(0).unsqueeze(0)

print("\nConv2d input shape:")
print(image.shape)


# ============================================================
# 4. CREATE CONVOLUTION
# ============================================================

conv = nn.Conv2d(
    in_channels=1,
    out_channels=1,
    kernel_size=2,
    stride=1,
    padding=0,
    bias=False
)


# ============================================================
# 5. SET THE KERNEL MANUALLY
# ============================================================

with torch.no_grad():
    conv.weight[0, 0] = kernel


# ============================================================
# 6. APPLY CONVOLUTION
# ============================================================

# PyTorch Conv2d actually computes cross-correlation:
# the supplied kernel is not flipped.

with torch.no_grad():
    feature_map = conv(image)


# ============================================================
# 7. SHOW RESULT
# ============================================================

print("\nFEATURE MAP:")
print(feature_map)

print("\nFeature map shape:")
print(feature_map.shape)