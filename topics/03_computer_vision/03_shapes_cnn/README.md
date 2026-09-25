# Experiment 07 — CNN for Circles vs Squares

## Objective

Can a convolutional neural network learn useful image filters automatically instead of receiving manually designed kernels?

The previous computer-vision experiments used convolution filters whose values were manually selected.

This experiment introduces trainable convolution filters.

The objective is to understand how convolutional layers, pooling and a final classifier can be trained together using backpropagation.

## Concepts

### Dataset

The experiment generates 1000 synthetic grayscale images.

Each image has size:

```text
32 × 32
```

and contains either:

```text
circle → label 0
square → label 1
```

The position of the shape is randomized.

Before adding the channel dimension, the dataset has shape:

```text
[1000, 32, 32]
```

After:

```python
X = X.unsqueeze(1)
```

the shape becomes:

```text
[1000, 1, 32, 32]
```

which represents:

```text
1000 images
1 grayscale channel
32 pixels high
32 pixels wide
```

### CNN architecture

The model is:

```text
32×32 grayscale image
        ↓
Conv2d 1 → 16
        ↓
ReLU
        ↓
MaxPool
        ↓
Conv2d 16 → 32
        ↓
ReLU
        ↓
MaxPool
        ↓
Flatten
        ↓
Linear
        ↓
1 logit
```

For the complete batch, the tensor shapes evolve as:

```text
[1000, 1, 32, 32]
        ↓
Conv2d(1 → 16)
        ↓
[1000, 16, 32, 32]
        ↓
MaxPool
        ↓
[1000, 16, 16, 16]
        ↓
Conv2d(16 → 32)
        ↓
[1000, 32, 16, 16]
        ↓
MaxPool
        ↓
[1000, 32, 8, 8]
        ↓
Flatten
        ↓
[1000, 2048]
        ↓
Linear(2048 → 1)
        ↓
[1000, 1]
```

### First convolution

The first convolution is:

```python
nn.Conv2d(
    in_channels=1,
    out_channels=16,
    kernel_size=3,
    padding=1
)
```

It receives one grayscale channel and produces 16 feature maps.

For each image:

```text
[1, 32, 32]
        ↓
16 learned filters
        ↓
[16, 32, 32]
```

Unlike the previous experiments, these filters are not manually defined.

Their weights are trainable parameters.

### Max pooling

The first pooling layer reduces:

```text
32 × 32
```

to:

```text
16 × 16
```

without changing the number of channels.

Therefore:

```text
[16, 32, 32]
↓
[16, 16, 16]
```

The second pooling layer later reduces:

```text
[32, 16, 16]
↓
[32, 8, 8]
```

Pooling reduces spatial resolution while retaining strong local activations.

### Second convolution

The second convolution is:

```python
nn.Conv2d(
    in_channels=16,
    out_channels=32,
    kernel_size=3,
    padding=1
)
```

It receives the 16 feature maps produced by the previous convolutional block and generates 32 new feature maps.

Conceptually:

```text
16 previous feature channels
          ↓
second convolution
          ↓
32 new feature channels
```

Each output filter can combine information from all 16 input channels.

### Flatten

Immediately before the classifier, each image is represented as:

```text
[32, 8, 8]
```

This contains:

```text
32 × 8 × 8 = 2048
```

values.

`Flatten()` reorganizes them into:

```text
[2048]
```

No values are removed by `Flatten`.

The spatial and channel dimensions are converted into a single feature vector that can be passed to the final linear layer.

### Final classifier

The final layer is:

```python
nn.Linear(
    32 * 8 * 8,
    1
)
```

which is equivalent to:

```python
nn.Linear(
    2048,
    1
)
```

For each image:

```text
2048 extracted feature values
        ↓
Linear layer
        ↓
1 logit
```

The logit represents the model output before sigmoid.

### Learned convolution filters

In the previous convolution experiments, filters were manually defined.

For example:

```text
[-1  1]
[-1  1]
```

In this experiment, convolution filters begin from initialized parameter values and are updated during training.

The learning process is:

```text
images
  ↓
CNN
  ↓
predictions
  ↓
loss
  ↓
backpropagation
  ↓
gradients
  ↓
optimizer
  ↓
updated convolution filters
```

Therefore, the model learns convolution kernels that help reduce the classification loss.

### Training

The network uses:

```python
nn.BCEWithLogitsLoss()
```

for binary classification.

Optimization uses:

```python
torch.optim.Adam(
    model.parameters(),
    lr=0.001
)
```

During each epoch:

```text
forward pass
    ↓
loss
    ↓
backpropagation
    ↓
gradients
    ↓
Adam
    ↓
updated parameters
```

The parameters updated during training include:

* first convolution weights and biases,
* second convolution weights and biases,
* final linear weights and bias.

## Hypothesis

The CNN should learn convolutional filters and classifier parameters that reduce binary classification loss on the generated training images.

Because circles and squares contain different visual structures, the learned convolution features should provide enough information for the final classifier to separate the two classes.

However, this experiment uses all generated images for training.

Therefore, low training loss and high training accuracy should not be interpreted as evidence of good generalization.

## Implementation

The experiment:

1. Generates 1000 synthetic images.
2. Randomly selects circle or square labels.
3. Randomizes the location of each shape.
4. Adds the grayscale channel dimension.
5. Creates two convolutional layers.
6. Applies ReLU activations.
7. Uses max pooling to reduce spatial dimensions.
8. Flattens the final feature maps.
9. Produces one binary classification logit.
10. Trains all model parameters using backpropagation and Adam.
11. Measures training accuracy.
12. Inspects the shapes of the learned convolution weights.
13. Displays one learned convolution kernel.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/03_shapes_cnn/main.py
```

## Observed results

A verified run produced:

```text
Dataset shape:
torch.Size([1000, 32, 32])

Labels shape:
torch.Size([1000])

After adding channel:
torch.Size([1000, 1, 32, 32])
```

Before training, five images produced logits close to zero:

```text
0.0370
0.0363
0.0583
0.0542
0.0334
```

At this stage, the convolution filters and classifier parameters had not yet been optimized for the task.

### Training loss

Training produced:

```text
Epoch 100,  Loss: 0.0514
Epoch 200,  Loss: 0.0037
Epoch 300,  Loss: 0.0013
Epoch 400,  Loss: 0.0007
Epoch 500,  Loss: 0.0004
Epoch 600,  Loss: 0.0003
Epoch 700,  Loss: 0.0002
Epoch 800,  Loss: 0.0001
Epoch 900,  Loss: 0.0000
Epoch 1000, Loss: 0.0000
```

The loss decreased substantially during training.

### Training accuracy

The final training accuracy was:

```text
1.0
```

or:

```text
100%
```

All 1000 training images were classified correctly.

This demonstrates very strong fitting of the training dataset.

It does not demonstrate performance on unseen images because no independent test set is used in this experiment.

### Learned convolution parameters

The first convolution weight tensor had shape:

```text
torch.Size([16, 1, 3, 3])
```

This means:

```text
16 output filters
1 input channel
3 × 3 kernel
```

The second convolution weight tensor had shape:

```text
torch.Size([32, 16, 3, 3])
```

This means:

```text
32 output filters
16 input channels per output filter
3 × 3 kernels
```

One learned filter from the first convolution was:

```text
[[ 0.3806,  0.3900,  0.0443],
 [ 0.4272,  0.0510,  0.1850],
 [-0.0183,  0.3093,  0.4228]]
```

These values were not manually designed.

They are trainable parameters that were adjusted during optimization.

The experiment does not establish exactly which visual pattern this individual filter represents.

## Interpretation

The experiment demonstrates the transition from manually designed convolution kernels to learned convolution filters.

Previously:

```text
human chooses kernel
        ↓
fixed feature map
```

Now:

```text
initialized kernel
        ↓
training loss
        ↓
backpropagation
        ↓
optimizer
        ↓
learned kernel
```

The decreasing loss and perfect training accuracy show that the network has enough capacity to fit the generated training dataset.

The convolutional layers learn feature representations while the final linear layer uses those representations to produce the binary classification logit.

However, the result only measures training performance.

A separate test set is required to determine whether the learned features generalize to unseen circles and squares.

## Conclusion

This experiment demonstrates a complete trainable convolutional neural network.

The model learns:

```text
pixels
  ↓
first convolutional features
  ↓
combined convolutional features
  ↓
flattened representation
  ↓
binary classification
```

Unlike the previous convolution experiments, the kernel values are learned automatically.

The fundamental learning mechanism remains the same as in previous neural-network experiments:

```text
forward pass
↓
loss
↓
backpropagation
↓
gradients
↓
optimizer
↓
updated parameters
```

The difference is that the trainable parameters now include spatial convolution kernels.

## Limitations

This experiment has several important limitations:

* All 1000 generated images are used for training.
* There is no independent test set.
* There is no validation set.
* The dataset is synthetic.
* Circle and square sizes are fixed.
* Brightness is fixed.
* Backgrounds are identical.
* Shapes may contain exploitable shortcuts such as area differences.
* Duplicate or very similar images may occur.
* Training uses full-batch optimization.
* Only one architecture is tested.
* Training accuracy alone does not measure generalization.
* Individual learned filters are not automatically interpretable.

The next experiment should introduce held-out test data to evaluate whether the CNN can classify shapes that were not used during training.

## Product connection

### Concept

Convolutional neural networks can learn visual feature extractors automatically from labelled image data.

### Implementation

The model learns convolution filters using the same backpropagation and optimization process previously used for fully connected neural networks.

### Product

A real visual-inspection system could learn filters useful for identifying visual patterns such as:

```text
edges
textures
shape boundaries
surface defects
structural anomalies
```

However, real deployment would require representative data and independent evaluation.

A model that perfectly classifies its training images is not sufficient evidence that it will work reliably on new production images.

## Check yourself

### Why does the first convolution use `in_channels=1`?

The generated images are grayscale.

Each image therefore contains one input channel.

### Why does the second convolution use `in_channels=16`?

The first convolution produces 16 feature maps.

These 16 feature maps become the 16 input channels of the second convolution.

### Why does the final linear layer receive `32 * 8 * 8` values?

Immediately before `Flatten`, each image is represented by:

```text
32 feature maps
×
8 pixels high
×
8 pixels wide
```

Therefore:

```text
32 × 8 × 8 = 2048
```

values are available per image.

`Flatten()` reorganizes those values into one vector, and the final linear layer receives that 2048-value representation.

### Does `Flatten()` delete information?

No.

`Flatten()` reorganizes:

```text
[32, 8, 8]
```

into:

```text
[2048]
```

The same 2048 numerical values remain present.

However, the explicit channel-height-width structure is no longer represented as separate tensor dimensions.

### What information can pooling remove?

Max pooling keeps only the maximum activation within each pooling region.

Other values in that region are discarded.

Therefore, pooling reduces spatial detail.

### How are the convolution filters learned?

The filters are trainable model parameters.

During training:

```text
prediction
↓
loss
↓
backpropagation
↓
filter gradients
↓
optimizer
↓
updated filter weights
```

Repeated optimization gradually changes the kernels to reduce the classification loss.

### Why can low training loss be misleading here?

All generated images are used for training.

A very low training loss therefore shows that the network fits those examples well.

It does not show how accurately the network will classify images it has never seen.

A separate held-out test set is required to measure generalization.