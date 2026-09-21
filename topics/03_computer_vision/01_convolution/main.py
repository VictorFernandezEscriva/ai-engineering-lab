import torch
import torch.nn as nn

# Imagen 5x5
image = torch.tensor([
    [0., 0., 0., 0., 0.],
    [0., 1., 1., 1., 0.],
    [0., 1., 1., 1., 0.],
    [0., 1., 1., 1., 0.],
    [0., 0., 0., 0., 0.]
])

print("IMAGE:")
print(image)

# Filtro 2x2
kernel = torch.tensor([
    [-1., 1.],
    [-1., 1.]
])

print()
print("KERNEL:")
print(kernel)

# Añadimos dimensiones para que PyTorch lo trate como imagen
image = image.unsqueeze(0).unsqueeze(0)

# Creamos una convolución
conv = nn.Conv2d(
    in_channels=1,
    out_channels=1,
    kernel_size=2,
    bias=False
)

# Sustituimos los pesos aprendibles por nuestro filtro
with torch.no_grad():
    conv.weight[:] = kernel

# Aplicamos convolución
# Conv2d computes cross-correlation: the supplied kernel is not flipped.
feature_map = conv(image)

print()
print("FEATURE MAP:")
print(feature_map)
