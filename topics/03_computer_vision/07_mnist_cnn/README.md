# Experiment 11 — MNIST CNN Multiclass Classification

## Objective

Can a convolutional neural network learn to classify handwritten digits from `0` to `9` using mini-batch training?

The previous experiments introduced:

```text
MNIST
↓
Dataset
↓
DataLoader
↓
mini-batches
```

This experiment combines those concepts with a trainable CNN.

It also introduces multiclass classification.

Previous classification experiments used two classes:

```text
circle
square
```

MNIST requires ten classes:

```text
0 1 2 3 4 5 6 7 8 9
```

## Concepts

### Multiclass classification

MNIST contains ten possible classes.

The CNN must produce evidence for every possible digit.

Therefore the final layer is:

```python
nn.Linear(
    32 * 7 * 7,
    10
)
```

The model produces:

```text
10 logits per image
```

One for each class:

```text
logit 0 → digit 0
logit 1 → digit 1
logit 2 → digit 2
...
logit 9 → digit 9
```

### CNN architecture

The model is:

```text
MNIST image
[1, 28, 28]

      ↓

Conv2d
1 → 16

      ↓

[16, 28, 28]

      ↓
ReLU
      ↓
MaxPool

[16, 14, 14]

      ↓

Conv2d
16 → 32

      ↓

[32, 14, 14]

      ↓
ReLU
      ↓
MaxPool

[32, 7, 7]

      ↓
Flatten

[1568]

      ↓
Linear

[10 logits]
```

### Why `32 * 7 * 7`?

The original MNIST image has spatial dimensions:

```text
28 × 28
```

The first convolution uses padding and preserves this size.

The first pooling operation reduces:

```text
28 × 28
↓
14 × 14
```

The second convolution preserves:

```text
14 × 14
```

The second pooling operation reduces:

```text
14 × 14
↓
7 × 7
```

At this point there are:

```text
32 feature maps
```

Therefore:

```text
32 × 7 × 7
=
1568
```

values are passed to the classifier.

### Batch output shape

The experiment uses:

```text
batch_size = 64
```

Each image produces ten logits.

Therefore one model output has shape:

```text
[64, 10]
```

which means:

```text
64 images
10 logits per image
```

### Logits

A logit is a raw model output before softmax.

For one image, the untrained network produced:

```text
[ 0.0172,
  0.0911,
  0.0461,
  0.1980,
 -0.1149,
 -0.0592,
 -0.0429,
  0.0903,
  0.0097,
 -0.0349]
```

Each value corresponds to one digit class.

The largest value was at index `3`.

Before training, however, these outputs do not represent meaningful learned digit recognition.

### `argmax`

The predicted class is selected using:

```python
torch.argmax(
    logits,
    dim=1
)
```

`argmax` returns the index containing the largest value.

For example:

```text
[0.1, 0.3, 0.2, 4.8, 0.1, ...]
               ↑
          largest value
```

produces:

```text
prediction = 3
```

### Cross-entropy loss

Binary classification previously used:

```python
BCEWithLogitsLoss
```

MNIST uses multiclass classification, so this experiment uses:

```python
nn.CrossEntropyLoss()
```

The function receives:

```text
model logits
+
correct class labels
```

For example:

```text
10 logits
+
label = 5
```

PyTorch does not require manually converting the label to one-hot encoding.

### Mini-batch training

Training uses:

```python
for images, labels in train_loader:
```

The `for` loop automatically requests each next batch from the DataLoader.

Conceptually:

```text
batch 1
↓
forward
↓
loss
↓
backward
↓
optimizer update

batch 2
↓
forward
↓
loss
↓
backward
↓
optimizer update

...
```

The MNIST training DataLoader contains:

```text
938 batches
```

Therefore one epoch processes all 60,000 training samples.

### Epochs

The experiment uses:

```text
3 epochs
```

Therefore:

```text
Epoch 1
→ 938 batches

Epoch 2
→ 938 batches

Epoch 3
→ 938 batches
```

This corresponds to approximately:

```text
938 × 3
=
2814
```

optimizer updates.

Because the training DataLoader uses:

```python
shuffle=True
```

the sample ordering changes between epochs.

### Softmax

During final inspection:

```python
torch.softmax(
    logits,
    dim=1
)
```

converts logits into scores between `0` and `1` that sum to approximately `1` for each image.

For example:

```text
digit 0 → 0.001
digit 1 → 0.002
digit 2 → 0.005
digit 3 → 0.980
...
```

These scores are useful for inspecting model confidence.

Softmax is not manually applied before `CrossEntropyLoss`.

The loss function expects raw logits.

## Hypothesis

A small convolutional neural network trained with mini-batches should learn visual representations capable of classifying MNIST digits with high accuracy.

Training loss should decrease across epochs while training accuracy should increase.

The trained model should also achieve high accuracy on the independent MNIST test dataset.

## Implementation

The experiment:

1. Loads the MNIST training dataset.
2. Loads the MNIST test dataset.
3. Creates DataLoaders with a batch size of 64.
4. Shuffles training data.
5. Creates a two-layer CNN.
6. Produces ten logits per image.
7. Uses `CrossEntropyLoss`.
8. Uses Adam for optimization.
9. Trains for three epochs.
10. Performs one optimizer update per training batch.
11. Tracks loss and training accuracy during each epoch.
12. Evaluates the final model on the test dataset.
13. Uses `argmax` to select predicted classes.
14. Uses softmax to inspect prediction confidence.
15. Prints several example predictions.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/07_mnist_cnn/main.py
```

MNIST is reused from the locally downloaded:

```text
data/
```

directory.

## Observed results

The verified dataset contained:

```text
Training samples: 60000
Test samples: 10000

Training batches: 938
Test batches: 157
```

### Batch shapes

One training batch produced:

```text
Images shape:
torch.Size([64, 1, 28, 28])

Labels shape:
torch.Size([64])
```

### Model output

The same batch produced:

```text
Model output shape:
torch.Size([64, 10])
```

This confirms:

```text
64 images
×
10 class logits
```

### Initial logits

Before training, one image produced:

```text
tensor([
 0.0172,
 0.0911,
 0.0461,
 0.1980,
-0.1149,
-0.0592,
-0.0429,
 0.0903,
 0.0097,
-0.0349
])
```

These values were generated before the CNN learned the MNIST classification task.

### Training

The verified training run produced:

```text
Epoch 1/3
Loss: 0.2426
Training accuracy: 0.9281

Epoch 2/3
Loss: 0.0708
Training accuracy: 0.9790

Epoch 3/3
Loss: 0.0528
Training accuracy: 0.9840
```

Expressed as percentages:

```text
Epoch 1 → 92.81%
Epoch 2 → 97.90%
Epoch 3 → 98.40%
```

Training loss decreased substantially:

```text
0.2426
↓
0.0708
↓
0.0528
```

while training accuracy increased.

### Important training accuracy detail

The reported training accuracy is accumulated while the model is being updated throughout the epoch.

Conceptually:

```text
batch
↓
prediction
↓
count accuracy
↓
update model
↓
next batch
```

Therefore the reported value is the training accuracy observed during that epoch.

It is not exactly equivalent to evaluating the final trained model once over the complete training dataset after optimization has finished.

### Test accuracy

The final test result was:

```text
Test accuracy:
0.9808
```

or:

```text
98.08%
```

On 10,000 test images this corresponds to:

```text
9808 correct predictions
192 incorrect predictions
```

### Example predictions

The verified run produced:

```text
Image 0: Real=7, Predicted=7, Confidence=1.0000
Image 1: Real=2, Predicted=2, Confidence=0.9989
Image 2: Real=1, Predicted=1, Confidence=0.9992
Image 3: Real=0, Predicted=0, Confidence=1.0000
Image 4: Real=4, Predicted=4, Confidence=0.9999
Image 5: Real=1, Predicted=1, Confidence=0.9992
Image 6: Real=4, Predicted=4, Confidence=0.9988
Image 7: Real=9, Predicted=9, Confidence=0.9944
Image 8: Real=5, Predicted=5, Confidence=0.9999
Image 9: Real=9, Predicted=9, Confidence=0.9997
```

All ten inspected examples were classified correctly.

## Interpretation

The experiment successfully combines the complete training pipeline:

```text
MNIST
↓
DataLoader
↓
mini-batches
↓
CNN
↓
10 logits
↓
CrossEntropyLoss
↓
backpropagation
↓
Adam
↓
updated parameters
```

The reduction in loss demonstrates that optimization is improving the model's predictions.

The increase in training accuracy demonstrates that the CNN progressively learns representations useful for digit classification.

The final:

```text
98.08% test accuracy
```

shows that the learned representations also generalize strongly to the independent MNIST test dataset.

The model is still small:

```text
Conv 1→16
↓
Conv 16→32
↓
Linear 1568→10
```

yet it successfully classifies most handwritten digits.

## Conclusion

This experiment trains the first multiclass CNN in the project using a standard computer-vision dataset.

It combines concepts introduced throughout the previous experiments:

```text
images
↓
channels
↓
convolution
↓
feature maps
↓
pooling
↓
DataLoader
↓
mini-batches
↓
logits
↓
loss
↓
backpropagation
↓
optimizer
↓
evaluation
```

The verified model achieved:

```text
98.08% test accuracy
```

after only three epochs.

This provides a complete basic PyTorch computer-vision training pipeline.

## Limitations

The experiment remains intentionally simple.

Limitations include:

* only three training epochs,
* one architecture,
* one optimizer configuration,
* no validation dataset,
* no learning-rate comparison,
* no data augmentation,
* no confusion matrix,
* no per-class accuracy,
* no visualization of classification errors,
* no GPU device management,
* no checkpoint saving,
* no probability calibration analysis.

The printed training accuracy is measured while model parameters are changing during each epoch rather than through a separate final training-set evaluation.

Softmax confidence values should also not automatically be interpreted as calibrated probabilities.

## Product connection

### Concept

Real image classifiers often require multiclass prediction rather than binary classification.

### Implementation

The model converts:

```text
image
↓
learned visual features
↓
10 logits
↓
predicted class
```

Mini-batch training allows the model to learn from a larger dataset efficiently.

### Product

The same architecture pattern appears in more advanced computer-vision systems:

```text
dataset
↓
DataLoader
↓
CNN / vision model
↓
class logits
↓
prediction
↓
evaluation
```

Real products may classify:

```text
product categories
industrial defects
medical image classes
objects
documents
satellite imagery
```

The models and datasets become much larger, but the fundamental training workflow remains similar.

## Check yourself

### Why does the model output 10 values per image?

MNIST contains ten classes:

```text
0 through 9
```

The model therefore produces one logit for every possible class.

### Why is the output shape `[64, 10]`?

The batch contains 64 images and each image produces ten logits.

### What does `argmax` do?

It returns the index containing the largest logit.

That index becomes the predicted class.

### Why use `CrossEntropyLoss`?

The task contains ten mutually exclusive classes.

`CrossEntropyLoss` compares the raw logits against the correct class index.

### Why do we not apply softmax before `CrossEntropyLoss`?

`CrossEntropyLoss` is designed to receive raw logits and internally performs the appropriate mathematical operations.

### What is one epoch?

One epoch is one complete pass through the training dataset.

In this experiment:

```text
1 epoch
=
938 batches
≈
60,000 images
```

### How many optimizer updates occur during three epochs?

Approximately:

```text
938 × 3
=
2814 updates
```

One update occurs after each training batch.

### Where does the next batch come from?

This loop:

```python
for images, labels in train_loader:
```

automatically iterates through the DataLoader.

Python internally requests each next batch until all batches have been processed.

### Why can training accuracy and test accuracy differ?

Training data is used to optimize model parameters.

Test data is not.

Test accuracy therefore measures how well the learned model generalizes to unseen samples.

### Does confidence `1.0000` guarantee the prediction is correct?

No.

Softmax scores measure the model's relative confidence between classes.

Neural networks can produce highly confident predictions that are still incorrect.

Confidence is not automatically the same as a calibrated real-world probability.