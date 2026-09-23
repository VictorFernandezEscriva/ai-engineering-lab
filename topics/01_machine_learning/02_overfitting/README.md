# Experiment 02 — Overfitting and Generalization

## Objective

Why is training performance alone not enough to evaluate a machine learning model?

This experiment studies the difference between fitting the training data and generalizing to unseen data.

It also explores how increasing model capacity can cause a decision tree to fit noise in the training set.

## Concepts

### Generalization

A model generalizes when patterns learned from the training data also work well on samples that were not used during training.

Good performance on the training set alone does not guarantee good performance on unseen data.

### Overfitting

Overfitting occurs when a model learns details, exceptions or noise that are specific to the training set instead of learning only patterns that generalize.

A common symptom is:

```text
very high training performance
            +
lower test performance
```

### Model capacity

Model capacity describes how flexible a model is and how complex a relationship it can represent.

For a decision tree, depth is one factor that controls capacity.

A deeper tree can represent more specific rules than a shallow tree.

### Generalization gap

The generalization gap is the difference between training and test performance:

```text
generalization gap =
training accuracy - test accuracy
```

A gap does not automatically prove severe overfitting, but a large gap can be evidence that the model is fitting the training data more closely than it generalizes to unseen data.

### Label noise

Label noise occurs when some training targets are incorrect or inconsistent with the underlying pattern.

In this experiment, approximately 5% of the generated labels are deliberately flipped.

This creates examples that do not follow the original failure rule and gives a sufficiently flexible model an opportunity to learn noise.

## Hypothesis

The depth-limited decision tree should capture the main failure pattern while being unable to fit every noisy training example.

The unrestricted tree should fit the training data more closely.

If this additional training performance is accompanied by worse test performance, it provides evidence of overfitting.

## Implementation

The script generates 200 synthetic motors with four input features:

* `temperature`
* `vibration`
* `rpm`
* `pressure`

The underlying failure rule is:

```text
temperature > 85
AND
vibration > 0.7
        ↓
failure = 1
```

Otherwise:

```text
failure = 0
```

Approximately 5% of the labels are then randomly flipped to introduce label noise.

The dataset is split into:

```text
70% training data
30% test data
```

Two decision trees are trained on exactly the same training samples.

### Depth-limited tree

```python
DecisionTreeClassifier(
    max_depth=2,
    random_state=42
)
```

This restricts the capacity of the model.

### Unrestricted tree

```python
DecisionTreeClassifier(
    max_depth=None,
    random_state=42
)
```

This allows the tree to continue growing until other stopping conditions prevent further splits.

For each model, the experiment measures:

* training accuracy,
* test accuracy,
* generalization gap,
* learned tree depth,
* number of leaves.

## Run

Run from the repository root:

```bash
python topics/01_machine_learning/02_overfitting/main.py
```

## Observed results

A verified run produced:

```text
Realized label noise: 10 / 200

LIMITED TREE
Max depth: 2
Number of leaves: 4
Training accuracy: 0.9714285714285714
Test accuracy: 0.9166666666666666
Generalization gap: 0.05476190476190479

UNRESTRICTED TREE
Max depth: 4
Number of leaves: 9
Training accuracy: 1.0
Test accuracy: 0.9
Generalization gap: 0.09999999999999998
```

Expressed as percentages:

```text
                     LIMITED TREE    UNRESTRICTED TREE

Training accuracy       97.14%            100.00%
Test accuracy           91.67%             90.00%
Generalization gap       5.48 pp            10.00 pp
Tree depth               2                  4
Number of leaves         4                  9
```

Exactly 10 of the 200 generated labels were flipped in this run, corresponding to a realized label-noise rate of 5%.

## Interpretation

The unrestricted tree has greater model capacity than the depth-limited tree.

Its learned structure is deeper and contains more leaves:

```text
Depth:  2 → 4
Leaves: 4 → 9
```

This additional capacity allows the unrestricted tree to fit the training data perfectly:

```text
97.14% → 100%
```

However, its performance on unseen test data decreases:

```text
91.67% → 90.00%
```

At the same time, the generalization gap increases from approximately:

```text
5.48 percentage points
```

to:

```text
10 percentage points
```

This is evidence of overfitting in this experiment.

The unrestricted tree fits the training set more closely, including training-specific details and some of the introduced label noise, but those additional learned rules do not improve performance on unseen samples.

The depth-limited tree cannot perfectly reproduce the training set, but it achieves slightly better test performance.

This demonstrates an important machine-learning principle:

> Better training performance does not necessarily mean better generalization.

## Conclusion

This experiment demonstrates the relationship between model capacity, training performance and generalization.

Increasing the capacity of the decision tree allows it to fit the training data more closely.

In this run, the unrestricted tree reaches 100% training accuracy, but its test accuracy is lower than that of the depth-limited tree.

The larger generalization gap provides evidence that the unrestricted tree is overfitting the training data more strongly.

The experiment therefore supports three main conclusions:

1. Training performance alone is not enough to evaluate a machine-learning model.
2. More model capacity can improve training accuracy while reducing performance on unseen data.
3. Restricting model capacity can act as a form of regularization and may improve generalization.

The result does not prove that `max_depth=2` is universally optimal. It only shows that, for this dataset and this particular train/test split, the depth-limited tree generalizes slightly better than the unrestricted one.

## Limitations

The dataset is synthetic and generated from a very simple known rule.

Real-world datasets can contain:

* sensor errors,
* missing values,
* correlations,
* class imbalance,
* distribution drift,
* incorrect labels,
* much more complex relationships.

Only one train/test split is used.

Therefore, the measured test accuracy depends partly on which samples happen to be included in the test set.

Later experiments should introduce techniques such as repeated evaluation, validation sets and cross-validation.

The experiment also compares only two model-capacity settings and should not be interpreted as proving that `max_depth=2` is universally optimal.

## Product connection

**Concept:** A model must generalize beyond the data used during training.

**Implementation:** Two decision trees with different capacities are trained on the same noisy synthetic dataset and evaluated independently on training and test data.

**Product:** In a real predictive system, strong performance on historical training data is not enough. A model must be evaluated on held-out data before deployment and monitored after deployment because production data may differ from training data.

## Check yourself

### Why must test data stay outside training?

Test data must stay outside training because it is used to evaluate how well the model performs on data it has not seen before.

If the test samples are also used during training, the model may already have adapted to those examples. This would make the measured accuracy artificially optimistic and would no longer provide a reliable estimate of generalization.

The test set should therefore simulate unseen data as closely as possible.

### What does the generalization gap measure?

The generalization gap measures the difference between the model's training performance and its test performance.

For example:

```text
Generalization gap =
Training accuracy - Test accuracy
```

A large positive gap can indicate that the model performs much better on the data it has already seen than on unseen data, which can be evidence of overfitting.

A small gap means that training and test performance are similar, but this alone does not guarantee that the model generalizes well. Both training and test performance must also be sufficiently good.

Ideally, we want strong performance on unseen data and a relatively small difference between training and test performance.

### Why does high training accuracy not necessarily mean that a model is good?

High training accuracy does not necessarily mean that a model is good because the model may be overfitting.

In that case, the model has learned the training data very well, including details or noise that are specific to those examples, but it does not perform equally well on new unseen data.

A good model should not only fit the training data; it should also generalize well to unseen data.

### What is overfitting?

Overfitting occurs when a model learns the training data too specifically, including details or noise that do not generalize well to new unseen data.

As a result, the model performs very well on the training set but noticeably worse on the test set.

In short:

```text
training performance → very high
test performance     → lower
```

This indicates that the model has adapted too much to the training data instead of learning only the patterns that generalize.

### Why can increasing model capacity increase the risk of overfitting?

Increasing model capacity allows the model to represent more complex and specific patterns.

This can help the model fit the training data more closely, but it can also cause the model to learn noise or training-specific details that do not generalize to unseen data.

A simpler model may generalize better because it is forced to focus on broader patterns.

However, reducing model capacity too much can also be harmful and lead to underfitting.

The goal is therefore to find a suitable balance between too little and too much model capacity.

### What does `max_depth` control in a decision tree?

`max_depth` controls the maximum number of levels that the decision tree is allowed to grow.

A larger `max_depth` gives the tree more capacity to create increasingly specific decision rules.

This can help the model fit complex patterns, but it also increases the risk of overfitting.

A very small `max_depth` can make the model too simple and cause underfitting.

Therefore, `max_depth` is a hyperparameter that directly influences the capacity of the decision tree.

### What is label noise?

Label noise occurs when some target labels in a dataset are incorrect, inconsistent, or do not follow the underlying pattern of the data.

In this experiment, the original failure labels are generated from a known rule based on `temperature` and `vibration`.

Then, approximately 5% of the labels are deliberately flipped:

```python
noise = np.random.random(n) < 0.05
failure[noise] = 1 - failure[noise]
```

This means that some samples receive a target that contradicts the original rule.

For example:

```text
Original label: 0
After noise:    1
```

or:

```text
Original label: 1
After noise:    0
```

Label noise is useful in this experiment because it creates training examples that a highly flexible model may try to memorize.

In real datasets, label noise can appear because of:

* human annotation errors,
* incorrect measurements,
* faulty sensors,
* inconsistent labelling criteria,
* data-processing errors.

A model with too much capacity may learn some of this noise instead of only learning the underlying pattern.

### Why might an unrestricted tree learn label noise?

An unrestricted decision tree has enough capacity to keep creating increasingly specific branches.

Because of this, it may create rules that isolate individual training samples, including samples whose labels were changed by noise.

Instead of learning only the underlying general pattern, the tree can therefore adapt to training-specific exceptions.

This increases the risk of overfitting.

In this experiment, the unrestricted tree reaches:

```text
Training accuracy: 100%
Test accuracy:      90%
```

while the depth-limited tree achieves:

```text
Training accuracy: 97.14%
Test accuracy:      91.67%
```

This suggests that the unrestricted tree is fitting the training data more closely, including some training-specific noise, without improving performance on unseen data.

An unrestricted tree does not necessarily overfit in every dataset, but its greater capacity makes overfitting more likely.
### Why is one train/test split not enough to precisely estimate real-world performance?

A single train/test split provides only one measurement of model performance.

The result can depend on which samples happen to be placed in the training set and which samples are placed in the test set.

With a different random split, the measured test accuracy may change even if the model and the dataset remain the same.

Therefore, one split may give an optimistic or pessimistic estimate of generalization.

More reliable evaluation can use techniques such as:

* repeated train/test splits,
* cross-validation,
* larger and more representative datasets,
* a separate validation set when tuning hyperparameters.

A large amount of data can make evaluation more reliable, but there is no general rule saying that millions of training samples are always required. The required amount depends on the problem, the complexity of the data and the model.

### What would we expect to observe if the unrestricted tree is overfitting more than the depth-limited tree?

If the unrestricted tree is overfitting more, we would expect it to achieve very high training accuracy while its test accuracy does not improve and may even become worse.

This creates a larger generalization gap.

For example:

```text
Training accuracy → increases
Test accuracy     → stays similar or decreases
Generalization gap → increases
```

This suggests that the model is learning patterns that are specific to the training data rather than patterns that generalize well to unseen data.

In this experiment, that is exactly what we observe:

```text
LIMITED TREE
Training accuracy: 97.14%
Test accuracy:     91.67%

UNRESTRICTED TREE
Training accuracy: 100%
Test accuracy:     90%
```

The unrestricted tree fits the training set better, but performs slightly worse on unseen test data, which is evidence of stronger overfitting.