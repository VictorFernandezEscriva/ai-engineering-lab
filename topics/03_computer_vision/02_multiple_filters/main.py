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
# 2. ADD BATCH AND CHANNEL DIMENSIONS
# ============================================================

image = image.unsqueeze(0).unsqueeze(0)

print("\nConv2d input shape:")
print(image.shape)


# ============================================================
# 3. CREATE CONVOLUTION WITH THREE FILTERS
# ============================================================

conv = nn.Conv2d(
    in_channels=1,
    out_channels=3,
    kernel_size=2,
    stride=1,
    padding=0,
    bias=False
)


# ============================================================
# 4. DEFINE THREE DIFFERENT FILTERS
# ============================================================

# Filter 1: responds positively to dark -> bright
# horizontal intensity transitions.
filter_1 = torch.tensor([
    [-1., 1.],
    [-1., 1.]
])

# Filter 2: opposite orientation of filter 1.
filter_2 = torch.tensor([
    [1., -1.],
    [1., -1.]
])

# Filter 3: detects horizontal edges by measuring vertical intensity changes.
filter_3 = torch.tensor([
    [-1., -1.],
    [1., 1.]
])


# ============================================================
# 5. SET FILTER WEIGHTS MANUALLY
# ============================================================

with torch.no_grad():
    conv.weight[0, 0] = filter_1
    conv.weight[1, 0] = filter_2
    conv.weight[2, 0] = filter_3


# ============================================================
# 6. APPLY ALL THREE FILTERS
# ============================================================

with torch.no_grad():
    feature_maps = conv(image)


# ============================================================
# 7. SHOW OUTPUT
# ============================================================

print("\nFEATURE MAP TENSOR SHAPE:")
print(feature_maps.shape)

print("\nNumber of output feature maps:")
print(feature_maps.shape[1])


for i in range(3):

    print()
    print(f"FEATURE MAP {i + 1}:")
    print(feature_maps[0, i])