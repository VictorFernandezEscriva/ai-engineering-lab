# Experiment 09 — MNIST Dataset Loading

## Objective

How do we move from fully synthetic images to a standard labelled computer-vision dataset?

## Concepts

MNIST contains grayscale images of handwritten digits and corresponding labels. `torchvision.datasets.MNIST` provides a convenient dataset interface.

The important step here is deliberately small: load the dataset, understand its structure and inspect one sample before designing or training another network.

## Hypothesis

The dataset loader should expose labelled image tensors and separate training and test collections.

## Implementation

The script creates separate training and test dataset objects and converts images to PyTorch tensors using `ToTensor()`.

Then it inspects:

- number of training samples,
- number of test samples,
- shape of one image tensor,
- label associated with that image.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/03_computer_vision/05_mnist/main.py
```

The first run downloads MNIST to the ignored root `data/` directory.

## Observed results

Not verified yet on the current environment.

No numerical result is claimed. See the [verification log](../../../docs/verification.md) for current execution blockers.

## Interpretation

No current dataset output is available. Loading data would verify acquisition and tensor conversion, not digit classification.

## Conclusion

The implementation introduces a dataset interface; it contains no digit classifier or training experiment.

## Limitations

This only inspects one sample and dataset sizes. No model is trained or evaluated. The first download needs internet access.

## Product connection

**Concept:** How do we move from fully synthetic images to a standard labelled computer-vision dataset?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Training pipelines need reproducible dataset acquisition and local storage; offline applications must account for downloads.

## Check yourself

- Why are training and test datasets separate?
- What does `ToTensor()` change?
- Where is the downloaded data stored?
- Why should downloaded datasets not normally be committed to Git?
