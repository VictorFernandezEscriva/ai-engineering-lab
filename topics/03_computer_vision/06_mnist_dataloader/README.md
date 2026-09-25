# Experiment 10 — MNIST DataLoader and Batches

## Objective

How can a large dataset be processed in smaller groups instead of sending every image through the model at once?

The previous experiment introduced the MNIST dataset and its `(image, label)` sample structure.

This experiment introduces PyTorch `DataLoader` and the concept of mini-batches.

No neural network is trained yet.

The goal is to understand how a dataset is divided, shuffled and delivered in batches before introducing a complete training loop.

## Concepts

### Dataset vs DataLoader

A PyTorch `Dataset` stores and provides individual samples.

For MNIST:

```text
dataset sample
→
(image, label)
```

A `DataLoader` organizes those samples into batches.

Conceptually:

```text
Dataset
↓
DataLoader
↓
batch 1
batch 2
batch 3
...
```

The dataset contains the data.

The DataLoader controls how that data is delivered.

### Batch size

The experiment uses:

```python
batch_size = 64
```

This means the DataLoader normally returns 64 samples at a time.

Instead of processing:

```text
60,000 images at once
```

the training dataset becomes:

```text
64 images
↓
64 images
↓
64 images
↓
...
```

A batch size is a hyperparameter.

Possible values include:

```text
16
32
64
128
256
```

The appropriate value depends on factors such as memory, hardware, model size and training behavior.

### Training batch shape

One verified training batch had shape:

```text
[64, 1, 28, 28]
```

This means:

```text
64 = images in the batch
1  = grayscale channel
28 = height
28 = width
```

The corresponding labels had shape:

```text
[64]
```

There is therefore one label for every image.

Conceptually:

```text
64 images
+
64 labels
```

### Number of training batches

MNIST contains:

```text
60,000 training samples
```

with:

```text
batch_size = 64
```

A batch calculation gives:

```text
60,000 / 64 = 937.5
```

There are:

```text
937 full batches
```

because:

```text
937 × 64 = 59,968
```

This leaves:

```text
60,000 - 59,968 = 32
```

samples.

Therefore the DataLoader creates:

```text
937 batches of 64
+
1 final batch of 32
=
938 batches
```

### Number of test batches

MNIST contains:

```text
10,000 test samples
```

With a batch size of 64:

```text
156 × 64 = 9,984
```

which leaves:

```text
16 samples
```

Therefore:

```text
156 full batches
+
1 final batch of 16
=
157 test batches
```

### Incomplete final batches

A DataLoader batch does not always have exactly the configured batch size.

The final batch may contain fewer samples when the dataset size is not divisible by the batch size.

Training:

```text
final batch = 32 images
```

Testing:

```text
final batch = 16 images
```

PyTorch can optionally discard incomplete batches using:

```python
drop_last=True
```

but this experiment keeps every sample.

### Shuffle

The training DataLoader uses:

```python
shuffle=True
```

This means the training samples are presented in a shuffled order.

Conceptually:

```text
original dataset order
↓
shuffle
↓
different batch composition
```

This helps prevent the model from depending on a fixed sample ordering during training.

The test DataLoader uses:

```python
shuffle=False
```

because evaluation does not require random sample ordering.

### Getting one batch

The experiment uses:

```python
images, labels = next(
    iter(train_loader)
)
```

`iter(train_loader)` creates an iterator over the batches.

`next(...)` requests the next batch.

Conceptually:

```text
train_loader
↓
iterator
↓
next batch
↓
images + labels
```

The verified first batch contained:

```text
64 images
64 labels
```

### Iterating through batches

A DataLoader is normally used with a loop:

```python
for images, labels in train_loader:
```

Each iteration returns one batch.

Conceptually:

```text
iteration 1
→ batch 1

iteration 2
→ batch 2

iteration 3
→ batch 3
```

This structure will later become the inner loop of neural-network training.

### DataLoader and epochs

When a model is trained, one epoch normally means processing the entire training dataset once.

With this experiment:

```text
1 epoch
=
938 training batches
```

A future training loop will therefore look approximately like:

```text
epoch
│
├── batch 1  → forward → loss → backward → update
├── batch 2  → forward → loss → backward → update
├── batch 3  → forward → loss → backward → update
│
...
└── batch 938 → forward → loss → backward → update
```

This is different from full-batch training, where the entire dataset produces only one optimizer update per epoch.

## Hypothesis

The DataLoader should divide the MNIST datasets into batches of up to 64 samples.

The training batch should have shape:

```text
[64, 1, 28, 28]
```

and its corresponding labels should have shape:

```text
[64]
```

Because 60,000 and 10,000 are not exactly divisible by 64, the number of batches should include smaller final batches.

## Implementation

The experiment:

1. Loads the MNIST training dataset.
2. Loads the MNIST test dataset.
3. Creates a training DataLoader.
4. Creates a test DataLoader.
5. Uses a batch size of 64.
6. Enables shuffling for training.
7. Disables shuffling for testing.
8. Prints the number of batches.
9. Retrieves one training batch.
10. Inspects its image tensor shape.
11. Inspects its label tensor shape.
12. Inspects several labels.
13. Inspects one individual image inside the batch.
14. Iterates through the first three training batches.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/06_mnist_dataloader/main.py
```

MNIST is reused from the local:

```text
data/
```

directory if it has already been downloaded.

## Observed results

A verified run produced:

```text
Training samples: 60000
Test samples: 10000
```

The configured batch size was:

```text
64
```

The DataLoaders contained:

```text
Training batches: 938
Test batches: 157
```

### One training batch

The inspected batch had:

```text
Images shape:
torch.Size([64, 1, 28, 28])

Labels shape:
torch.Size([64])
```

The first ten labels were:

```text
tensor([6, 3, 0, 1, 2, 7, 9, 1, 5, 4])
```

The first image inside the batch had:

```text
First image shape:
torch.Size([1, 28, 28])

First image label:
6
```

This confirms that one batch contains multiple MNIST samples while each individual image still has shape:

```text
[1, 28, 28]
```

### First three batches

The first inspected batches were:

```text
Batch 0:
images=torch.Size([64, 1, 28, 28])
labels=torch.Size([64])

Batch 1:
images=torch.Size([64, 1, 28, 28])
labels=torch.Size([64])

Batch 2:
images=torch.Size([64, 1, 28, 28])
labels=torch.Size([64])
```

These batches were full batches containing 64 samples each.

The final training batch is expected to contain only 32 samples because the dataset size is not exactly divisible by 64.

## Interpretation

The experiment demonstrates how PyTorch separates data storage from data delivery.

The `Dataset` provides individual samples:

```text
(image, label)
```

while the `DataLoader` groups those samples into:

```text
(images, labels)
```

batches.

The key transition is:

```text
single sample
[1, 28, 28]

↓

batch of samples
[64, 1, 28, 28]
```

The first tensor dimension therefore represents the number of samples inside the batch.

This batching mechanism prepares the project for a more realistic training loop.

Instead of one optimizer update after processing an entire dataset, training can update the model after each batch.

## Conclusion

The MNIST datasets were successfully divided into mini-batches using PyTorch `DataLoader`.

The verified training batch shape was:

```text
[64, 1, 28, 28]
```

with:

```text
64 corresponding labels
```

The 60,000 training examples produced:

```text
938 batches
```

and the 10,000 test examples produced:

```text
157 batches
```

The experiment establishes the data-delivery mechanism needed for mini-batch neural-network training.

The next stage can combine:

```text
Dataset
↓
DataLoader
↓
CNN
↓
loss
↓
backpropagation
↓
optimizer
```

## Limitations

This experiment does not yet:

* create a neural network,
* perform a forward pass through a classifier,
* calculate training loss,
* perform backpropagation,
* update model parameters,
* calculate training accuracy,
* calculate test accuracy.

Only the batching and iteration mechanics are studied.

The batch size is fixed at 64 and no comparison with other batch sizes is performed.

## Product connection

### Concept

Real machine-learning systems often process datasets using mini-batches instead of loading an entire dataset into one model operation.

### Implementation

PyTorch separates:

```text
Dataset
→ stores and provides samples

DataLoader
→ groups and delivers samples
```

A training system can then process one batch at a time.

### Product

A production image-training pipeline may contain millions of images that cannot all be processed simultaneously.

The same general pattern applies:

```text
large dataset
↓
DataLoader
↓
mini-batches
↓
GPU
↓
model training
```

Batching therefore connects dataset management with practical model training.

## Check yourself

### What does `batch_size=64` mean?

The DataLoader attempts to provide 64 samples in each batch.

The final batch may be smaller if the number of dataset samples is not divisible by 64.

### Why does the image batch have shape `[64, 1, 28, 28]`?

It represents:

```text
64 images
1 grayscale channel
28 pixels high
28 pixels wide
```

### Why do labels have shape `[64]`?

There is one class label for each of the 64 images in the batch.

### Why are there 938 training batches?

There are 60,000 training images.

```text
937 × 64 = 59,968
```

which leaves:

```text
32 images
```

The final smaller batch creates batch number 938.

### How large is the final training batch?

```text
32 images
```

### Why are there 157 test batches?

There are 10,000 test images.

```text
156 × 64 = 9,984
```

which leaves:

```text
16 images
```

Therefore the test DataLoader creates 157 batches.

### Why use `shuffle=True` for training?

Shuffling changes sample order so that training batches are not always composed of the same neighboring dataset samples.

### Why use `shuffle=False` for testing?

The model is not learning during test evaluation.

A stable order is therefore useful and shuffling is unnecessary.

### What does `next(iter(train_loader))` do?

It creates an iterator over the DataLoader and retrieves one batch.

The result is:

```text
images
+
labels
```

### How is mini-batch training different from full-batch training?

Full-batch training processes the entire training dataset before one parameter update.

Mini-batch training performs parameter updates after smaller groups of samples.

For this experiment:

```text
1 epoch
≈
938 possible training updates
```

once a training loop is introduced.