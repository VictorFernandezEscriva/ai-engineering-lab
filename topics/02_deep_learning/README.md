# Deep Learning

Deep learning is a subfield of machine learning based on neural networks composed of trainable numerical layers.

Instead of defining explicit decision rules manually, a neural network learns numerical parameters — primarily weights and biases — from data.

The fundamental training process introduced in this section is:

```text
input data
    ↓
forward pass
    ↓
model output
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

After training, the learned parameters can be reused during inference:

```text
new input
    ↓
trained neural network
    ↓
logit
    ↓
sigmoid
    ↓
score
    ↓
decision threshold
    ↓
prediction
```

These concepts form part of the foundation used later in larger neural networks, computer vision systems and language models.

## Available material

* [Experiment 03 — First PyTorch Binary Classifier](01_binary_classifier/README.md)
* [Experiment 04 — Neural Network Evaluation and Thresholds](02_train_test_and_thresholds/README.md)

## Concepts covered

The current experiments cover:

* PyTorch tensors,
* tensor shapes,
* feature standardization,
* neural-network layers,
* weights and biases,
* `Linear` layers,
* hidden layers,
* ReLU activation,
* logits,
* sigmoid,
* binary classification,
* binary cross-entropy,
* `BCEWithLogitsLoss`,
* forward passes,
* loss functions,
* gradients,
* backpropagation,
* gradient accumulation,
* `zero_grad()`,
* optimizers,
* Adam,
* learning rate,
* epochs,
* parameter updates,
* training mode,
* evaluation mode,
* `torch.no_grad()`,
* reproducibility with random seeds,
* training vs inference,
* train/test splits,
* generalization,
* normalization without data leakage,
* confusion matrices,
* true positives,
* true negatives,
* false positives,
* false negatives,
* accuracy,
* precision,
* recall,
* F1-score,
* decision thresholds,
* threshold trade-offs,
* class imbalance,
* inspection of learned network parameters.

## What the experiments demonstrate

### First PyTorch Binary Classifier

The first experiment introduces the fundamental neural-network training process using a small `4 → 8 → 1` network.

It demonstrates how:

```text
4 input features
      ↓
Linear(4 → 8)
      ↓
ReLU
      ↓
Linear(8 → 1)
      ↓
logit
```

is trained by repeatedly performing:

```text
forward pass
→ loss
→ backpropagation
→ parameter update
```

It also demonstrates the distinction between a raw logit and the value obtained after applying sigmoid.

The experiment intentionally uses all samples for training, so it demonstrates optimization and training fit but does not measure generalization.

### Neural Network Evaluation and Thresholds

The second experiment introduces held-out test data and evaluates the trained neural network on samples that were not used for training.

It demonstrates the importance of:

```text
training data
→ learn parameters

test data
→ evaluate unseen performance
```

It also shows why preprocessing statistics must be calculated from training data only.

The experiment compares multiple classification thresholds:

```text
0.3
0.5
0.7
```

and demonstrates that changing the threshold can change:

* false positives,
* false negatives,
* precision,
* recall,
* F1-score,
* accuracy,

without retraining the neural network.

It also traces one motor through the complete network:

```text
original features
      ↓
normalization
      ↓
Linear(4 → 8)
      ↓
ReLU
      ↓
Linear(8 → 1)
      ↓
logit
      ↓
sigmoid
      ↓
threshold
      ↓
prediction
```

## Key distinction learned

One of the main differences between the earlier decision-tree experiments and these neural-network experiments is how the models learn.

A decision tree learns a structure of explicit decision rules:

```text
temperature <= threshold
        ↓
branch
```

A neural network instead learns numerical parameters:

```text
weights
+
biases
```

Training repeatedly modifies those parameters in order to reduce a loss function.

Conceptually:

```text
Decision Tree

data
 ↓
find useful splits
 ↓
tree structure


Neural Network

data
 ↓
forward pass
 ↓
loss
 ↓
gradients
 ↓
update weights
```

## Evaluation workflow learned

The experiments also introduce the separation between model training and model evaluation.

A basic workflow is:

```text
dataset
   ↓
train/test split
   │
   ├── training set
   │      ↓
   │   preprocessing statistics
   │      ↓
   │   model training
   │
   └── test set
          ↓
       same preprocessing
          ↓
       model inference
          ↓
       evaluation metrics
```

A more complete machine-learning workflow will later introduce a validation set:

```text
training set
    ↓
learn parameters

validation set
    ↓
choose hyperparameters
architecture
threshold

test set
    ↓
final evaluation
```

## Intentionally not covered yet

This section does not yet study:

* mini-batch training,
* `Dataset` and `DataLoader`,
* stochastic gradient descent in depth,
* learning-rate schedules,
* validation-based hyperparameter tuning,
* systematic architecture comparison,
* regularization techniques such as Dropout,
* Batch Normalization,
* weight decay,
* early stopping,
* multiclass classification,
* regression with neural networks,
* probability calibration,
* ROC curves,
* AUC,
* GPU/CUDA training in depth,
* saving and loading trained models,
* larger real-world datasets,
* production deployment,
* model monitoring,
* distributed training.

These topics will be introduced when they become relevant in later experiments.

See the [roadmap](../../ROADMAP.md).

## Status

The current Deep Learning experiments have been reviewed, executed and documented.

The experiments contain verified execution evidence, observed results, interpretations and limitations.

At this stage, the section establishes a practical understanding of the fundamental neural-network workflow:

```text
tensor
→ layer
→ activation
→ logit
→ loss
→ gradient
→ backpropagation
→ optimizer
→ trained parameters
→ inference
→ evaluation
```

This represents verified learning progress and practical experimentation, not a claim of mastery of the deep-learning field.