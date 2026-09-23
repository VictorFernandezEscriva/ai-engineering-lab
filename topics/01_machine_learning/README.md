# Machine Learning

Machine learning is a field of artificial intelligence in which models learn patterns from data instead of relying only on manually programmed rules.

In supervised learning, the model receives input features together with known target values and learns a relationship that can later be used to make predictions on unseen data.

This section focuses on the fundamental workflow:

```text
data
  ↓
features + target
  ↓
training
  ↓
learned model
  ↓
inference
  ↓
evaluation
  ↓
generalization
```

The experiments are deliberately small and synthetic so that the learning process, model behavior and limitations remain easy to inspect.

Deep learning is a subfield of machine learning based on neural networks and is covered separately in the next topic.

## Available material

* [Experiment 01 — Decision Tree Failure Classification](01_decision_tree/README.md)
* [Experiment 02 — Overfitting and Generalization](02_overfitting/README.md)

## Concepts covered

The current experiments cover:

* supervised learning,
* features and targets,
* training and inference,
* decision trees,
* Gini impurity,
* train/test splits,
* reproducibility with random seeds,
* model evaluation,
* accuracy,
* generalization,
* generalization gap,
* overfitting,
* underfitting,
* model capacity,
* hyperparameters such as `max_depth`,
* label noise,
* the difference between training and test performance.

## What the experiments demonstrate

The decision-tree experiment shows how a supervised model can learn explicit decision rules from labelled data and use those rules during inference.

The overfitting experiment shows why training performance alone is not enough to evaluate a model. By comparing a depth-limited tree with an unrestricted tree, it demonstrates how additional model capacity can improve training accuracy while reducing performance on unseen data.

## Intentionally not covered yet

This section does not yet study:

* cross-validation,
* repeated train/test evaluation,
* systematic hyperparameter tuning,
* validation sets,
* precision, recall and F1 in depth,
* ROC/AUC,
* calibrated probabilities,
* class imbalance in depth,
* feature engineering,
* production model monitoring,
* real-world deployment.

These topics will be introduced when they become relevant in later experiments.

See the [roadmap](../../ROADMAP.md).

## Status

The current machine-learning experiments have been reviewed, executed and documented.

Observed results and limitations are recorded inside each experiment.

This section represents verified learning progress and practical experimentation, not a claim of mastery of the machine-learning field.