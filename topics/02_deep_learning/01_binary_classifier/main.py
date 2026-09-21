import torch
import torch.nn as nn

# Datos de entrenamiento
X = torch.tensor([
    [70.0, 0.2, 4500.0, 2.1],
    [72.0, 0.3, 4600.0, 2.2],
    [75.0, 0.2, 4700.0, 2.1],
    [80.0, 0.4, 4800.0, 2.2],
    [82.0, 0.5, 4850.0, 2.2],
    [85.0, 0.7, 4900.0, 2.3],
    [88.0, 0.9, 5000.0, 2.3],
    [90.0, 1.2, 5100.0, 2.4],
    [93.0, 1.5, 5150.0, 2.4],
    [95.0, 1.7, 5200.0, 2.5]
])

y = torch.tensor([
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [0.0],
    [1.0],
    [1.0],
    [1.0],
    [1.0],
    [1.0]
])

# Normalización de los datos
mean = X.mean(dim=0)
std = X.std(dim=0)

X_normalized = (X - mean) / std

print("Media:")
print(mean)

print("\nDesviación estándar:")
print(std)

print("\nDatos normalizados:")
print(X_normalized)

model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)

loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)

for epoch in range(1000):

    # 1. Predicción
    predictions = model(X_normalized)

    # 2. Calcular error
    loss = loss_function(predictions, y)

    # 3. Borrar gradientes anteriores
    optimizer.zero_grad()

    # 4. Calcular cómo cambiar los pesos
    loss.backward()

    # 5. Actualizar los pesos
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# Nuevo motor
new_motor = torch.tensor([
    [92.0, 1.4, 5150.0, 2.4]
])

new_motor_normalized = (new_motor - mean) / std

output = model(new_motor_normalized)

probability = torch.sigmoid(output)

print("\nRaw output:", output.item())
print("Probability of failure:", probability.item())

if probability.item() >= 0.5:
    print("Prediction: FAILURE")
else:
    print("Prediction: NORMAL")