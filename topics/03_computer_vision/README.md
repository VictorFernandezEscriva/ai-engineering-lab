# Computer Vision

Computer vision extracts information from images by exploiting spatial structure.

Unlike fully connected models that treat inputs as generic feature vectors, convolutional neural networks preserve local relationships between pixels and learn spatial filters that detect useful visual patterns.

The experiments in this topic progress from manually designed convolution kernels to a complete image-classification pipeline using:

```text
images
↓
convolution
↓
feature maps
↓
pooling
↓
learned representations
↓
mini-batch training
↓
multiclass classification
↓
held-out evaluation
↓
error analysis
```

The topic also introduces PyTorch image datasets and DataLoaders using MNIST.

## Available Material

* [Experiment 05 — Manual Convolution Kernel](01_convolution/README.md)
* [Experiment 06 — Multiple Convolution Filters](02_multiple_filters/README.md)
* [Experiment 07 — CNN for Circles vs Squares](03_shapes_cnn/README.md)
* [Experiment 08 — Shape CNN Evaluation and Feature Maps](04_shapes_evaluation/README.md)
* [Experiment 09 — MNIST Dataset Loading](05_mnist/README.md)
* [Experiment 10 — MNIST DataLoader and Batches](06_mnist_dataloader/README.md)
* [Experiment 11 — MNIST CNN Multiclass Classification](07_mnist_cnn/README.md)
* [Experiment 12 — MNIST Error Analysis](08_mnist_error_analysis/README.md)

## Learning Progression

### Manual Convolution

The first experiments introduce convolution using manually selected kernels.

The basic operation is:

```text
image
+
kernel
↓
convolution
↓
feature map
```

This establishes the relationship between:

* local image regions,
* kernel weights,
* convolution responses,
* output feature maps.

### Multiple Filters and Channels

Multiple filters are then applied to the same image.

This introduces the idea that:

```text
1 input image
↓
multiple filters
↓
multiple feature maps
```

and explains why CNN tensors contain channel dimensions.

### Learned Convolution Filters

The next step replaces manually selected kernels with trainable convolution parameters.

Instead of:

```text
human designs kernel
```

the model learns:

```text
initialized weights
↓
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
updated convolution filters
```

This connects convolution directly to the deep-learning concepts introduced in the previous topic.

### CNN Architecture

The synthetic shape experiments introduce a complete CNN:

```text
image
↓
Conv2d
↓
ReLU
↓
MaxPool
↓
Conv2d
↓
ReLU
↓
MaxPool
↓
Flatten
↓
Linear
↓
classification logit
```

Important tensor-shape transformations are inspected directly.

For example:

```text
[1, 32, 32]
↓
[16, 32, 32]
↓
[16, 16, 16]
↓
[32, 16, 16]
↓
[32, 8, 8]
↓
[2048]
↓
[1]
```

### Feature Maps

The experiments distinguish between:

```text
filter
```

and:

```text
feature map
```

A filter contains learned weights.

A feature map is the result of applying those weights to a particular input.

```text
input
+
filter
↓
convolution
↓
feature map
```

Intermediate feature maps from multiple CNN layers are inspected and visualized.

### Held-Out Evaluation

Synthetic shape classification is evaluated using separate training and test data.

This reinforces the distinction between:

```text
training fit
```

and:

```text
generalization
```

A model performing well on its training data does not automatically prove that it performs well on unseen examples.

### MNIST Dataset

The topic then moves from manually generated images to a standard labelled image dataset.

MNIST provides:

```text
60,000 training samples
10,000 test samples
```

Each image has shape:

```text
[1, 28, 28]
```

representing:

```text
1 grayscale channel
28 pixels high
28 pixels wide
```

Each image is paired with a digit label from:

```text
0 to 9
```

### Dataset and DataLoader

PyTorch separates data storage from data delivery.

A `Dataset` provides individual samples:

```text
(image, label)
```

A `DataLoader` groups those samples into mini-batches:

```text
Dataset
↓
DataLoader
↓
batch
↓
batch
↓
batch
```

With:

```text
batch_size = 64
```

one training batch has shape:

```text
[64, 1, 28, 28]
```

with:

```text
[64]
```

corresponding labels.

MNIST produces:

```text
938 training batches
157 test batches
```

with the final batches being smaller because the dataset sizes are not exactly divisible by 64.

### Mini-Batch Training

The MNIST CNN introduces a realistic training loop:

```text
epoch
↓
batch
↓
forward pass
↓
loss
↓
backpropagation
↓
optimizer update
↓
next batch
```

One epoch corresponds to one complete traversal of the training DataLoader.

With 938 training batches:

```text
1 epoch
≈
938 optimizer updates
```

### Multiclass Classification

Previous experiments used binary classification.

MNIST introduces ten classes:

```text
0 1 2 3 4 5 6 7 8 9
```

The final layer therefore produces:

```text
10 logits per image
```

For a batch of 64 images:

```text
output shape
=
[64, 10]
```

The model uses:

```python
nn.CrossEntropyLoss()
```

for multiclass classification.

Predictions are selected using:

```python
torch.argmax(logits, dim=1)
```

### Verified MNIST CNN Result

The multiclass CNN was trained for three epochs.

Verified test accuracy:

```text
98.08%
```

The model architecture was intentionally small:

```text
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
Linear 1568 → 10
```

This experiment established a complete basic PyTorch computer-vision training pipeline.

### Error Analysis

Evaluation was extended beyond aggregate accuracy.

The final error-analysis experiment included:

* overall test accuracy,
* confusion matrix,
* per-class accuracy,
* most frequent class confusions,
* visualization of misclassified images.

Verified result:

```text
Correct predictions:   9855
Incorrect predictions: 145
Test accuracy:          98.55%
```

The weakest classes in that run were:

```text
Digit 9 → 96.73%
Digit 8 → 96.92%
Digit 2 → 97.87%
```

while some classes exceeded 99% accuracy.

The most common confusion was:

```text
Real 8
→
Predicted 0
```

with 11 occurrences.

This demonstrates why a single accuracy value is not sufficient for understanding model behavior.

## Concepts Covered

This topic covers:

* images as tensors,
* grayscale channels,
* batch dimensions,
* convolution kernels,
* cross-correlation in PyTorch convolution,
* local receptive fields,
* feature maps,
* multiple filters,
* input and output channels,
* learned convolution weights,
* ReLU,
* max pooling,
* spatial-dimension reduction,
* CNN architectures,
* flattening,
* binary image classification,
* multiclass image classification,
* logits,
* sigmoid,
* softmax,
* `argmax`,
* `BCEWithLogitsLoss`,
* `CrossEntropyLoss`,
* backpropagation through convolution layers,
* PyTorch datasets,
* `torchvision`,
* MNIST,
* image preprocessing with `ToTensor`,
* DataLoaders,
* mini-batches,
* shuffling,
* epochs,
* held-out test evaluation,
* confusion matrices,
* per-class accuracy,
* misclassification analysis,
* intermediate feature-map inspection.

## Key Mental Model

A CNN progressively transforms raw pixels into learned representations.

A simplified pipeline is:

```text
pixels
↓
simple local features
↓
combinations of features
↓
more useful representations
↓
classifier
↓
prediction
```

Training adjusts the convolution filters automatically:

```text
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
updated filters
```

## Important Tensor Shapes

PyTorch image batches generally use:

```text
[batch, channels, height, width]
```

For example:

```text
[64, 1, 28, 28]
```

means:

```text
64 images
1 grayscale channel
28 pixels high
28 pixels wide
```

The first tensor dimension represents the batch size.

The second represents feature channels.

The final two dimensions preserve spatial structure.

## Evaluation Lessons

Several important evaluation principles were reinforced throughout the topic.

### Training performance is not enough

High training accuracy does not prove generalization.

Independent test data is required.

### Aggregate accuracy is not enough

A model can have strong overall accuracy while performing worse on particular classes.

Useful evaluation may include:

```text
overall accuracy
+
confusion matrix
+
per-class metrics
+
misclassified examples
```

### Confidence is not probability calibration

Softmax values can be useful for inspecting relative model confidence.

They should not automatically be interpreted as calibrated real-world probabilities.

## Intentionally Not Covered Yet

This topic establishes computer-vision foundations rather than covering the entire field.

Future computer-vision work may include:

* data augmentation,
* validation datasets,
* learning-rate scheduling,
* checkpoint saving and loading,
* transfer learning,
* pretrained CNNs,
* larger image datasets,
* RGB images,
* real-world image noise,
* object detection,
* image segmentation,
* localization,
* modern vision architectures,
* Vision Transformers,
* model calibration,
* deployment and inference optimization.

These topics can be revisited later when required by the broader AI Engineering roadmap.

See the [AI Engineering Roadmap](../../ROADMAP.md).

## Completion Checkpoint

The Computer Vision Foundations phase is considered complete when the following concepts can be explained without relying only on code:

* what `[batch, channels, height, width]` represents,
* why grayscale images have one channel,
* what a convolution kernel does,
* difference between a filter and a feature map,
* why multiple filters produce multiple channels,
* why the next convolution receives the previous layer's output channels,
* how convolution filters are learned through backpropagation,
* why pooling reduces spatial dimensions,
* what information pooling may discard,
* why `Flatten()` reorganizes values rather than deleting them,
* how a CNN converts image tensors into class logits,
* how a Dataset differs from a DataLoader,
* how mini-batches are generated,
* what an epoch represents,
* why one optimizer update usually occurs per training batch,
* difference between binary and multiclass classification,
* why MNIST requires ten output logits,
* how `argmax` converts logits into class predictions,
* why `CrossEntropyLoss` receives raw logits,
* why test data must remain outside model training,
* why confusion matrices reveal information hidden by overall accuracy.

## Status

**COMPLETE — Computer Vision Foundations**

The experiments in this topic have been executed and reviewed.

The phase establishes practical foundations in convolutional neural networks, image datasets, mini-batch training, multiclass classification and model evaluation.

Completion of this phase does not imply mastery of the full computer-vision field.

The next learning phase is:

```text
Phase 04 — LLM Fundamentals
```

with the planned progression:

```text
text
↓
tokens
↓
token IDs
↓
embeddings
↓
attention
↓
transformer
↓
logits
↓
next-token prediction
```