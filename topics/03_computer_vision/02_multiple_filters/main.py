import torch
import torch.nn as nn

# Nuestra imagen 5x5
image = torch.tensor([
    [0., 0., 0., 0., 0.],
    [0., 1., 1., 1., 0.],
    [0., 1., 1., 1., 0.],
    [0., 1., 1., 1., 0.],
    [0., 0., 0., 0., 0.]
])

image = image.unsqueeze(0).unsqueeze(0)

# 3 filtros diferentes
conv = nn.Conv2d(
    in_channels=1,
    out_channels=3,
    kernel_size=2,
    bias=False
)

# Filtro 1: busca transición oscuro -> claro
filter_1 = torch.tensor([
    [-1., 1.],
    [-1., 1.]
])

# Filtro 2: busca transición claro -> oscuro
filter_2 = torch.tensor([
    [1., -1.],
    [1., -1.]
])

# Filtro 3: busca cambios verticales
filter_3 = torch.tensor([
    [-1., -1.],
    [1., 1.]
])

with torch.no_grad():
    conv.weight[0] = filter_1
    conv.weight[1] = filter_2
    conv.weight[2] = filter_3

feature_maps = conv(image)

print("NUMBER OF FEATURE MAPS:")
print(feature_maps.shape)

for i in range(3):
    print()
    print(f"FEATURE MAP {i + 1}:")
    print(feature_maps[0, i])