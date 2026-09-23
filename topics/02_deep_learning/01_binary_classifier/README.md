# Experiment 03 — First PyTorch Binary Classifier

## Objective

How does a neural network learn a binary classification rule from numerical inputs?

This experiment introduces the basic training process of a neural network using PyTorch.

Unlike the previous decision-tree experiments, the model does not learn explicit rules such as:

```text
temperature <= 83.5
```

Instead, it learns numerical parameters called **weights** and **biases**.

The objective is to understand the complete training cycle:

```text
inputs
  ↓
forward pass
  ↓
prediction
  ↓
loss
  ↓
backpropagation
  ↓
gradients
  ↓
optimizer
  ↓
updated weights
```

## Concepts

### Tensors

PyTorch represents numerical data using tensors.

In this experiment:

```text
X shape = [10, 4]
y shape = [10, 1]
```

`X` contains:

```text
10 motors
×
4 input features
```

The four features are:

* `temperature`
* `vibration`
* `rpm`
* `pressure`

`y` contains one binary target for each motor:

```text
0 → NORMAL
1 → FAILURE
```

Tensors are one of the fundamental data structures used by PyTorch and will appear throughout deep learning.

### Feature normalization

The raw features use very different numerical scales.

For example:

```text
temperature ≈ 70–95
vibration   ≈ 0.2–1.7
rpm         ≈ 4500–5200
pressure    ≈ 2.1–2.5
```

The experiment standardizes each feature using:

```python
mean = X.mean(dim=0)
std = X.std(dim=0)

X_normalized = (X - mean) / std
```

Conceptually:

```text
normalized value =
(value - mean) / standard deviation
```

After standardization, the features are represented on more comparable numerical scales.

This generally makes neural-network optimization easier because very large numerical differences between features are reduced.

### Neural-network architecture

The model is:

```python
model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)
```

Its architecture can be represented as:

```text
4 input features
      ↓
Linear(4 → 8)
      ↓
8 hidden values
      ↓
ReLU
      ↓
Linear(8 → 1)
      ↓
1 logit
```

### Linear layer

A linear layer performs a transformation conceptually similar to:

```text
output = input × weights + bias
```

The first layer:

```python
nn.Linear(4, 8)
```

takes four input features and produces eight output values.

The second layer:

```python
nn.Linear(8, 1)
```

takes the eight hidden values and produces one final output.

The weights and biases inside these layers are trainable parameters.

Unlike the thresholds of a decision tree, these values are continuously adjusted during neural-network training.

### ReLU

The hidden layer is followed by:

```python
nn.ReLU()
```

ReLU applies the function:

```text
ReLU(x) = max(0, x)
```

For example:

```text
-5 → 0
-2 → 0
 0 → 0
 3 → 3
 8 → 8
```

ReLU introduces non-linearity into the network.

Without non-linear activation functions, stacking multiple linear layers would still behave like a single linear transformation and would severely limit what the network could represent.

### Logit

The final layer produces a raw value called a **logit**.

A logit is not yet a probability.

It can take values such as:

```text
-5.4
-0.7
0
2.3
8.1
```

Conceptually:

```text
large negative logit
→ strong tendency toward class 0

logit around 0
→ uncertain

large positive logit
→ strong tendency toward class 1
```

### Sigmoid

The sigmoid function converts a logit into a value between `0` and `1`.

```python
probability = torch.sigmoid(output)
```

Conceptually:

```text
large negative logit → probability close to 0

logit = 0            → probability = 0.5

large positive logit → probability close to 1
```

The experiment uses a threshold of:

```text
0.5
```

to convert the sigmoid output into a binary prediction:

```text
probability >= 0.5 → FAILURE
probability < 0.5  → NORMAL
```

The sigmoid output can be interpreted as a model score on a probability scale, but this simple experiment does not demonstrate that the score is perfectly calibrated as a real-world probability.

### Binary cross-entropy

The experiment uses:

```python
loss_function = nn.BCEWithLogitsLoss()
```

`BCE` stands for **Binary Cross Entropy**.

It is a loss function designed for binary classification.

The loss measures how well the model outputs agree with the correct targets.

Conceptually:

```text
prediction far from target
→ larger loss

prediction close to target
→ smaller loss
```

Training tries to reduce this loss.

### Why `BCEWithLogitsLoss`?

The final layer produces raw logits rather than probabilities.

`BCEWithLogitsLoss` combines:

```text
sigmoid
+
binary cross entropy
```

internally in a numerically stable implementation.

Therefore, during training we do **not** manually apply sigmoid before calculating the loss.

We use:

```python
predictions = model(X_normalized)
loss = loss_function(predictions, y)
```

The `predictions` variable contains logits.

Sigmoid is applied manually only later when we want to interpret the final model output during inference.

### Forward pass

The forward pass sends the input through the network using the current weights and biases.

In this experiment:

```text
X
↓
Linear(4 → 8)
↓
ReLU
↓
Linear(8 → 1)
↓
logits
```

It occurs here:

```python
predictions = model(X_normalized)
```

The forward pass calculates outputs using the current parameters.

It does not update the parameters by itself.

### Loss

After the forward pass, the model output is compared with the correct target:

```python
loss = loss_function(predictions, y)
```

The loss is a single numerical value representing how poorly the current model is fitting the training examples.

For example:

```text
Epoch 0
Loss ≈ 0.7

...

Epoch 900
Loss ≈ very small value
```

A decreasing training loss means the model is becoming better at fitting the training data.

It does not automatically mean that the model generalizes well to unseen data.

### Gradients

A gradient describes how changing a trainable parameter would affect the loss.

Conceptually:

```text
weight
  ↓
small change
  ↓
how much would loss change?
```

The gradient gives information about both:

* the direction in which the parameter should change,
* how strongly that parameter affects the loss locally.

### Backpropagation

Backpropagation is the process used to calculate gradients through the neural network.

In PyTorch:

```python
loss.backward()
```

computes the gradients of the loss with respect to the trainable parameters.

Conceptually:

```text
loss
 ↓
output layer
 ↓
hidden layer
 ↓
weights and biases
```

PyTorch follows the computational graph backwards and calculates derivatives such as:

```text
∂loss / ∂weight
```

`loss.backward()` calculates gradients.

It does **not** update the model parameters.

The parameters are updated later by the optimizer.

### Why `zero_grad()`?

PyTorch accumulates gradients by default.

Therefore, before calculating gradients for the current training step, we call:

```python
optimizer.zero_grad()
```

Without this step, gradients from previous iterations would be added to the newly calculated gradients.

The training cycle therefore includes:

```text
remove previous gradients
       ↓
calculate new gradients
       ↓
update parameters
```

### Optimizer

The optimizer determines how the model parameters should be changed using the calculated gradients.

This experiment uses:

```python
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)
```

Adam is an optimization algorithm commonly used for neural-network training.

The parameter:

```text
lr = 0.01
```

is the **learning rate**.

It influences the size of the parameter updates.

The actual parameter update occurs here:

```python
optimizer.step()
```

Conceptually:

```text
current weights
      ↓
gradients
      ↓
Adam optimizer
      ↓
updated weights
```

### Training loop

The complete training cycle is:

```text
forward pass
     ↓
calculate loss
     ↓
zero old gradients
     ↓
backpropagation
     ↓
calculate gradients
     ↓
optimizer step
     ↓
update weights
     ↓
repeat
```

In code:

```python
for epoch in range(1000):

    predictions = model(X_normalized)

    loss = loss_function(predictions, y)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()
```

### Epoch

An epoch is one complete pass through the training dataset.

This experiment contains ten training samples and processes all ten at once.

Therefore:

```text
1 epoch
=
one complete pass through all 10 samples
```

The experiment performs:

```text
1000 epochs
```

meaning that the same training dataset is repeatedly used while the model parameters are gradually updated.

### Training vs inference

Training modifies the model parameters.

```text
training
↓
forward pass
↓
loss
↓
gradients
↓
optimizer
↓
weights change
```

Inference uses the already learned parameters without changing them.

```text
new input
↓
trained model
↓
output
```

The inference section therefore uses:

```python
model.eval()

with torch.no_grad():
    output = model(new_motor_normalized)
    probability = torch.sigmoid(output)
```

`model.eval()` places the model in evaluation mode.

For this specific network it does not change the behavior because the architecture does not contain layers such as Dropout or BatchNorm, but it is the correct general inference pattern.

`torch.no_grad()` tells PyTorch that gradients are not required, avoiding unnecessary gradient tracking during inference.

### Reproducibility

Neural-network weights are initialized using random values.

Therefore, without controlling randomness, different executions may start with different weights and produce slightly different results.

The experiment uses:

```python
torch.manual_seed(42)
```

to make the PyTorch random initialization reproducible.

The value `42` itself is not special. It is simply a fixed seed.

## Hypothesis

Repeated optimization steps should reduce the binary cross-entropy loss on the ten training samples.

Because the dataset is very small and no independent test set is used, a very low training loss should not be interpreted as evidence that the model generalizes well to unseen data.

The network should eventually produce a strong positive logit for the additional motor because its measurements are similar to the training examples labelled as failures.

## Implementation

The script performs the following sequence:

1. Creates ten labelled motor examples as PyTorch tensors.
2. Separates four input features from the binary targets.
3. Calculates the mean and standard deviation of each input feature.
4. Standardizes the input data.
5. Creates a `4 → 8 → 1` feed-forward neural network.
6. Uses ReLU as the hidden activation function.
7. Uses `BCEWithLogitsLoss` as the training objective.
8. Uses Adam to optimize the trainable parameters.
9. Performs 1000 training epochs.
10. Prints the loss every 100 epochs.
11. Normalizes one additional motor using the training mean and standard deviation.
12. Performs inference using the trained model.
13. Converts the output logit with sigmoid.
14. Applies a `0.5` decision threshold.

The important training sequence is:

```text
forward pass
    ↓
loss
    ↓
zero old gradients
    ↓
backward()
    ↓
gradients
    ↓
optimizer.step()
    ↓
updated parameters
```

## Run

Run from the repository root:

```bash
python topics/02_deep_learning/01_binary_classifier/main.py
```

## Observed results

A verified run using:

```python
torch.manual_seed(42)
```

produced the following training behavior:

```text
Epoch 0, Loss: 0.6468
Epoch 100, Loss: 0.0138
Epoch 200, Loss: 0.0035
Epoch 300, Loss: 0.0016
Epoch 400, Loss: 0.0009
Epoch 500, Loss: 0.0006
Epoch 600, Loss: 0.0004
Epoch 700, Loss: 0.0003
Epoch 800, Loss: 0.0002
Epoch 900, Loss: 0.0002
```

The loss decreases substantially during training:

```text
0.6468
   ↓
0.0138
   ↓
0.0035
   ↓
...
   ↓
0.0002
```

This shows that the optimizer successfully adjusts the weights and biases so that the network increasingly fits the ten training examples.

The model architecture was:

```text
Sequential(
  (0): Linear(in_features=4, out_features=8, bias=True)
  (1): ReLU()
  (2): Linear(in_features=8, out_features=1, bias=True)
)
```

The tensor shapes were:

```text
Input shape:  torch.Size([10, 4])
Target shape: torch.Size([10, 1])
```

For the additional motor:

```text
temperature = 92.0
vibration   = 1.4
rpm         = 5150.0
pressure    = 2.4
```

the trained network produced:

```text
Raw output: 22.570871353149414
Probability of failure: 1.0
Prediction: FAILURE
```

The raw output is a strongly positive logit.

Applying sigmoid maps this value extremely close to `1`, so the `0.5` decision threshold produces the class:

```text
FAILURE
```

The displayed value `1.0` should not be interpreted as proof of a real-world 100% probability of failure.

It only shows that this trained model strongly favors class `1` for this input.

Because all labelled examples were used during training and there is no independent test set, these results demonstrate training fit but do not measure generalization.

## Interpretation

A decreasing loss demonstrates that the optimizer is modifying the neural-network parameters in a direction that improves the fit to the training examples.

The network is learning numerical weights and biases rather than explicit human-readable rules such as those produced by a decision tree.

A very small training loss only demonstrates that the model fits these ten training examples well.

It does not demonstrate good performance on unseen data because this experiment does not contain an independent test set.

Similarly, a sigmoid output close to `1` indicates that the trained model strongly favors the `FAILURE` class for the supplied input.

It does not prove that the real-world probability of failure is exactly that value.

## Conclusion

This experiment demonstrates the fundamental training loop of a neural network.

The main process is:

```text
initialize parameters
       ↓
forward pass
       ↓
calculate loss
       ↓
backpropagation
       ↓
calculate gradients
       ↓
optimizer updates parameters
       ↓
repeat
```

Unlike a decision tree, which learns explicit decision branches, a neural network learns numerical weights and biases.

The experiment also demonstrates the distinction between:

```text
logit
↓
sigmoid
↓
value between 0 and 1
↓
decision threshold
↓
binary prediction
```

The experiment demonstrates learning on the training data but does not yet measure generalization.

## Limitations

This experiment has several important limitations:

* The dataset contains only 10 samples.
* All ten samples are used for training.
* There is no independent test set.
* The data is synthetic.
* The network is evaluated on only one additional manually selected input.
* No validation set is used.
* No cross-validation is performed.
* No class-imbalance analysis is performed.
* The model trains using the complete dataset at once rather than mini-batches.
* Only one network architecture is tested.
* Only one learning rate is tested.
* Only one optimizer is tested.
* The sigmoid output is not evaluated for probability calibration.

A very low training loss therefore does **not** prove good generalization.

The next evaluation experiment will introduce held-out data and metrics that provide more information about behavior on unseen samples.

## Product connection

### Concept

A neural network learns numerical parameters that transform input features into an output useful for prediction.

### Implementation

This experiment uses a small PyTorch network to transform four motor measurements into a binary failure score.

The model learns its weights through:

```text
forward pass
→ loss
→ backpropagation
→ optimizer
```

### Product

A real predictive-maintenance application could use a trained neural network to process telemetry and estimate equipment failure risk.

A production system would require considerably more than this training script, including:

* representative historical data,
* correct train/validation/test separation,
* reproducible preprocessing,
* storage of normalization statistics,
* model serialization,
* model versioning,
* evaluation on unseen data,
* appropriate decision thresholds,
* analysis of false positives and false negatives,
* inference performance measurement,
* monitoring after deployment,
* detection of data drift,
* retraining procedures.

It would also be essential to apply exactly the same preprocessing during inference that was used during training.

For example:

```text
training mean/std
       ↓
saved with model pipeline
       ↓
new production sample
       ↓
same normalization
       ↓
model inference
```

## Check yourself

### What is the difference between a logit and a probability?

A logit is the raw numerical output produced by the final layer of the neural network.

It is not restricted to the range between `0` and `1`.

For example:

```text
-5.2
0
3.7
```

are valid logits.

A sigmoid function can transform a logit into a value between `0` and `1`:

```text
logit
  ↓
sigmoid
  ↓
value between 0 and 1
```

In this experiment, that sigmoid output is then compared with the threshold `0.5` to produce the final binary prediction.

### Why should normalization statistics be computed correctly?

The model is trained using inputs transformed with specific normalization statistics.

In this experiment:

```python
mean = X.mean(dim=0)
std = X.std(dim=0)
```

define the transformation used during training.

New inputs must use the same `mean` and `std`.

If inference data were normalized using different statistics, the model would receive values represented differently from those it learned during training.

Therefore:

```text
training preprocessing
must match
inference preprocessing
```

In a real application, the normalization statistics would normally be stored together with the model or preprocessing pipeline.

### Why do we call `zero_grad()`?

PyTorch accumulates gradients by default.

After `loss.backward()`, the gradients are stored in the model parameters.

If they are not cleared before the next training step, the new gradients will be added to the previous ones.

Therefore:

```python
optimizer.zero_grad()
```

clears the previous gradients before calculating the gradients for the current iteration.

The usual sequence is:

```text
zero_grad()
    ↓
forward pass
    ↓
loss
    ↓
backward()
    ↓
new gradients
    ↓
optimizer.step()
```

### What does `loss.backward()` calculate?

`loss.backward()` performs backpropagation.

It calculates the gradients of the loss with respect to the trainable parameters of the neural network.

Conceptually, it answers questions such as:

```text
If this weight changed slightly,
how would the loss change?
```

Mathematically, PyTorch computes derivatives such as:

```text
∂loss / ∂weight
```

These gradients tell the optimizer how each parameter influences the current loss.

`loss.backward()` calculates the gradients but does not update the weights.

### What does `optimizer.step()` change?

`optimizer.step()` uses the calculated gradients to update the trainable parameters of the model.

These parameters include:

* weights,
* biases.

In this experiment, Adam uses the gradients and the configured learning rate to decide how the parameters should change.

Conceptually:

```text
current parameters
       ↓
gradients
       ↓
optimizer.step()
       ↓
updated parameters
```

This is the step that actually changes the neural network.

### What is the difference between `loss.backward()` and `optimizer.step()`?

`loss.backward()` calculates gradients.

```text
backward()
→ determine how parameters affect the loss
```

`optimizer.step()` uses those gradients to modify the parameters.

```text
optimizer.step()
→ update the parameters
```

Therefore:

```text
backward()
does not update weights

optimizer.step()
does update weights
```

### What is a forward pass?

A forward pass sends the input through each layer of the neural network using the current parameters.

In this experiment:

```text
input
  ↓
Linear(4 → 8)
  ↓
ReLU
  ↓
Linear(8 → 1)
  ↓
logit
```

It produces the model output needed to calculate the loss.

The forward pass itself does not change the model parameters.

### What is backpropagation?

Backpropagation is the process used to calculate how the loss depends on each trainable parameter in the neural network.

It propagates gradient information backwards through the computational graph.

Conceptually:

```text
loss
 ↓
output layer
 ↓
hidden layer
 ↓
weights and biases
```

PyTorch performs this process automatically when:

```python
loss.backward()
```

is called.

### What is an epoch?

An epoch is one complete pass through the training dataset.

In this experiment, all ten training samples are processed together.

Therefore:

```text
1 epoch
=
the network processes all 10 training samples once
```

The script performs 1000 epochs, meaning the model repeatedly processes the same training set while its weights and biases are gradually updated.

### What does the learning rate control?

The learning rate controls the scale of the parameter updates made during optimization.

In this experiment:

```python
lr=0.01
```

A learning rate that is too large can cause unstable optimization or make the model jump over useful parameter values.

A learning rate that is too small can make training unnecessarily slow.

The best learning rate depends on the model and optimization problem.

### Why is this script insufficient to claim generalization?

All ten labelled samples are used to train the neural network.

There is no independent test set containing unseen labelled examples.

Therefore, a very low training loss only demonstrates that the network can fit the training data.

It does not tell us how well the model performs on new unseen samples.

To evaluate generalization, the model must be tested using data that did not influence training.

### Why do we use `model.eval()` during inference?

`model.eval()` switches the neural network into evaluation mode.

Some layers behave differently during training and inference, especially layers such as:

* Dropout,
* BatchNorm.

The network in this experiment does not contain those layers, so `model.eval()` does not currently change its numerical behavior.

However, using it establishes the correct inference pattern for more complex neural networks.

### Why do we use `torch.no_grad()` during inference?

During inference, the model parameters are not being trained.

Therefore, gradients are unnecessary.

Using:

```python
with torch.no_grad():
```

prevents PyTorch from tracking gradient operations for that computation.

This reduces unnecessary memory use and computation during inference.
