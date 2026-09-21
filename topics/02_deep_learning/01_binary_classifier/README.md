# Experiment 03 — First PyTorch Binary Classifier

## Objective

How does a neural network learn a binary classification rule from numerical inputs?

## Concepts

A small feed-forward neural network performs repeated numerical transformations:

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
      ↓
Sigmoid
      ↓
probability
```

Training changes the weights and biases. Inference reuses the learned values.

### Important concepts in this experiment

- tensors,
- feature normalization,
- linear layers,
- ReLU,
- logits,
- sigmoid,
- binary cross-entropy,
- gradients,
- backpropagation,
- Adam optimizer,
- training loop.

### Why normalize the inputs?

The raw features use very different numeric scales. RPM is around thousands while vibration is around decimal values. Standardization places features on more comparable scales, which generally makes optimization easier.

### Why `BCEWithLogitsLoss`?

The final layer emits a raw logit. `BCEWithLogitsLoss` combines the mathematically stable binary-cross-entropy calculation with the sigmoid relationship internally during training.

We apply `sigmoid` ourselves only when we want to interpret the final logit as a probability-like value for prediction.

## Hypothesis

Training should reduce binary cross-entropy on the ten supplied examples.

## Implementation

The script standardizes four features from ten motors, trains a 4 → 8 → 1 network for 1000 epochs with Adam, and scores one supplied motor using the same normalization. There is no held-out split.



The important sequence is:

```text
forward pass
    ↓
loss
    ↓
zero old gradients
    ↓
backward()
    ↓
optimizer.step()
```

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/02_deep_learning/01_binary_classifier/main.py
```

## Observed results

Not verified yet on the current environment.

Historical evidence retained from the supplied notes (environment, dependency versions and raw logs were not recorded):

In a previously recorded run, loss fell from roughly `0.70` to near zero. The selected new motor produced a strongly positive logit and a displayed sigmoid result of `1.0`, leading to `FAILURE`.

## Interpretation

The historical loss reduction describes fit to training data. A saturated sigmoid score is not a calibrated guarantee of failure.

## Conclusion

The recorded run supports learning a training objective with a small neural network; generalization remains unmeasured.

## Limitations

The dataset is extremely small and this first script does not perform an independent test evaluation. A very low training loss therefore does **not** prove good generalization.

The evaluation experiment adds a held-out split, but still uses synthetic data.

No random seed is set, so initialization and numerical outputs vary between runs.

## Product connection

**Concept:** How does a neural network learn a binary classification rule from numerical inputs?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** An alarm application converts a model score into an action with a chosen threshold.

## Check yourself

- What is the difference between a logit and a probability?
- Why should normalization statistics be computed correctly?
- Why do we call `zero_grad()`?
- What does `loss.backward()` calculate?
- What does `optimizer.step()` change?
- Why is this script insufficient to claim generalization?
