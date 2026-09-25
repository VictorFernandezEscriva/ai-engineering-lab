# Experiment 09 — MNIST Dataset Loading

## Objective

How do we move from manually generated synthetic images to a standard labelled computer-vision dataset?

The previous computer-vision experiments generated circles and squares directly in Python.

This experiment introduces MNIST, a standard dataset of handwritten digits, and explores how real labelled image data is represented and accessed through PyTorch.

No neural network is trained in this experiment.

## Concepts

### MNIST

MNIST contains grayscale images of handwritten digits:

```text
0 1 2 3 4 5 6 7 8 9
```

Each sample contains:

```text
image
+
correct label
```

For example:

```text
handwritten image of 5
+
label = 5
```

MNIST already provides separate datasets for training and testing:

```text
60,000 training samples
10,000 test samples
```

### PyTorch Dataset

The training dataset is created with:

```python
train_dataset = datasets.MNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)
```

The test dataset uses:

```python
train=False
```

Conceptually:

```text
train=True
→ training dataset

train=False
→ test dataset
```

Unlike the synthetic experiments, where images and labels were manually stored in `X` and `y`, MNIST uses a dataset object.

A sample can be retrieved using:

```python
image, label = train_dataset[0]
```

which returns:

```text
(image, label)
```

### Image and label

The image is the model input.

The label is the correct answer associated with that image.

For the first verified sample:

```text
Label: 5
```

This means the corresponding image contains a handwritten digit `5`.

Later, a classifier could receive:

```text
image of handwritten 5
        ↓
CNN
        ↓
prediction
```

and compare that prediction against:

```text
label = 5
```

### Image shape

The inspected image had shape:

```text
[1, 28, 28]
```

This means:

```text
1  = grayscale channel
28 = height
28 = width
```

MNIST images are grayscale, so they contain one channel.

A typical RGB image would instead contain three channels:

```text
Red
Green
Blue
```

### `ToTensor()`

The dataset uses:

```python
transform=ToTensor()
```

This converts the MNIST image into a PyTorch tensor.

The verified sample had:

```text
type:
torch.Tensor

dtype:
torch.float32

shape:
[1, 28, 28]

pixel range:
0.0 to 1.0
```

Conceptually:

```text
MNIST image
     ↓
ToTensor()
     ↓
PyTorch tensor
[1, 28, 28]
```

This tensor can later be passed directly into a neural network.

### Pixel values

The verified pixel value range was:

```text
0.0 to 1.0
```

For these images:

```text
values near 0.0
→ dark pixels

values near 1.0
→ bright pixels
```

### Visualizing samples

The experiment also displays several training samples using Matplotlib.

Each MNIST tensor has shape:

```text
[1, 28, 28]
```

Before displaying it as a grayscale image, the channel dimension is removed with:

```python
image.squeeze(0)
```

This transforms:

```text
[1, 28, 28]
↓
[28, 28]
```

No pixel information is removed.

Only a dimension whose size is `1` is removed.

The visualization code displays the first ten samples together with their corresponding labels.

Conceptually:

```text
dataset sample
     ↓
(image, label)
     ↓
display image
     +
display correct label
```

### Training and test datasets

MNIST already separates training and test data.

The training dataset is intended for:

```text
learning model parameters
```

The test dataset is intended for:

```text
evaluating the trained model
```

Conceptually:

```text
MNIST
   │
   ├── 60,000 training samples
   │       ↓
   │    model learns
   │
   └── 10,000 test samples
           ↓
        evaluation
```

No manual `train_test_split()` is required.

### Local dataset storage

The code uses:

```python
root="data"
```

so MNIST is downloaded under:

```text
data/
```

The repository `.gitignore` already contains:

```gitignore
data/
```

therefore the downloaded dataset is not committed to Git.

## Hypothesis

The MNIST dataset loader should:

1. provide 60,000 training samples,
2. provide 10,000 test samples,
3. return image tensors,
4. return the correct label associated with each image,
5. represent grayscale images using shape `[1, 28, 28]`,
6. produce floating-point pixel values between `0.0` and `1.0`,
7. allow individual samples to be visualized.

## Implementation

The experiment:

1. Loads the MNIST training dataset.
2. Loads the MNIST test dataset.
3. Downloads the dataset when it is not already available locally.
4. Converts images to PyTorch tensors using `ToTensor()`.
5. Prints the number of training and test samples.
6. Retrieves the first training sample.
7. Inspects the image type.
8. Inspects the tensor shape.
9. Inspects the tensor dtype.
10. Inspects the pixel value range.
11. Inspects the corresponding label.
12. Separates channel, height and width dimensions.
13. Displays the first ten training images.
14. Displays the corresponding labels.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/05_mnist/main.py
```

The first run downloads MNIST into:

```text
data/
```

Later executions can reuse the locally stored dataset.

The script also opens a Matplotlib window containing example MNIST images.

## Observed results

A verified run produced:

```text
Training samples: 60000
Test samples: 10000
```

The first training sample produced:

```text
Image type: <class 'torch.Tensor'>
Image shape: torch.Size([1, 28, 28])
Image dtype: torch.float32
Pixel value range: 0.0 to 1.0
Label: 5
```

The tensor dimensions were:

```text
Channels: 1
Height: 28
Width: 28
```

### Dataset sizes

The verified dataset therefore contains:

```text
60,000 training images
10,000 test images
```

### Image representation

Each inspected MNIST image is represented as:

```text
[1, 28, 28]
```

which means:

```text
1 grayscale channel
28 pixels high
28 pixels wide
```

### Label representation

The first inspected sample had:

```text
Label: 5
```

The label therefore represents the correct digit contained in the image.

### Tensor representation

The image was converted to:

```text
torch.float32
```

with values ranging from:

```text
0.0 to 1.0
```

This confirms that the image is ready to be used as numerical input for a neural network.

## Interpretation

This experiment demonstrates the transition from manually generated data to a reusable dataset interface.

Previously:

```text
Python code
↓
generate circle or square
↓
generate label
↓
build X and y
```

Now:

```text
MNIST Dataset
↓
request sample
↓
(image, label)
```

The dataset already contains both:

```text
input data
+
correct answers
```

This is much closer to how machine-learning training pipelines are normally structured.

The verified tensor shape also confirms that a future CNN processing MNIST will begin with:

```text
in_channels = 1
```

because MNIST images are grayscale.

The next important step is to stop accessing individual samples manually and introduce a `DataLoader`.

That will allow the dataset to be processed in batches.

## Conclusion

MNIST was successfully downloaded, loaded and inspected through `torchvision`.

The experiment verified:

```text
60,000 training samples
10,000 test samples
```

and confirmed that an individual image is represented as:

```text
[1, 28, 28]
```

with:

```text
torch.float32
```

values between:

```text
0.0 and 1.0
```

Each image is paired with its correct digit label.

The experiment also introduces visual inspection of dataset samples before any model is created.

This provides the dataset foundation required for the next stages:

```text
Dataset
↓
DataLoader
↓
batches
↓
CNN
↓
training
↓
evaluation
```

## Limitations

This experiment does not yet include:

* a `DataLoader`,
* batching,
* a neural network,
* loss calculation,
* backpropagation,
* model training,
* predictions,
* test accuracy,
* confusion matrices.

The experiment only verifies dataset acquisition, representation and inspection.

The first dataset download also requires network access.

## Product connection

### Concept

Real machine-learning systems normally work with reusable dataset pipelines rather than manually creating every training sample inside the training script.

### Implementation

MNIST provides:

```text
images
+
labels
+
predefined train/test datasets
```

PyTorch converts individual images into tensors that can later be processed by a model.

### Product

A production computer-vision pipeline follows the same general structure:

```text
dataset
↓
preprocessing
↓
tensor
↓
batching
↓
model
↓
prediction
```

The real dataset may contain millions of much larger images, but the basic abstraction remains similar.

## Check yourself

### Why are training and test datasets separate?

The training dataset is used to learn model parameters.

The test dataset is reserved for evaluating the final model on samples that were not used during training.

### What does `train=True` mean?

It tells `torchvision` to load the MNIST training collection.

### What does `train=False` mean?

It tells `torchvision` to load the MNIST test collection.

### What does `ToTensor()` do?

It converts the image into a PyTorch tensor.

In the verified run:

```text
shape:
[1, 28, 28]

dtype:
torch.float32

pixel range:
0.0 to 1.0
```

### What does the label represent?

The label is the correct digit contained in the image.

For example:

```text
image = handwritten 5
label = 5
```

### Why does the image have one channel?

MNIST images are grayscale.

Therefore:

```text
channels = 1
```

### What does `squeeze(0)` do?

For an MNIST image:

```text
[1, 28, 28]
```

it removes the first dimension because its size is `1`:

```text
[1, 28, 28]
↓
[28, 28]
```

It does not remove image pixels.

This makes the tensor convenient to display as a two-dimensional grayscale image.

### Why is `data/` ignored by Git?

The dataset can be downloaded automatically and does not need to be stored inside the source-code repository.

The repository already contains:

```gitignore
data/
```

so downloaded MNIST files remain local.

### What comes next?

The next step is to introduce a PyTorch `DataLoader`.

Instead of manually requesting:

```python
train_dataset[0]
```

the dataset will be processed in batches such as:

```text
64 images
64 images
64 images
...
```

This is the standard mechanism used when training neural networks with larger datasets.