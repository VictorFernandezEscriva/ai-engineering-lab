# Experiment 04 — Neural Network Evaluation and Thresholds

## Objective

How do we evaluate a neural-network classifier on unseen data, and how does changing the decision threshold affect its behavior?

The previous experiment demonstrated how a neural network can learn from training data.

However, good training performance does not prove that the model generalizes.

This experiment introduces a held-out test set and evaluates the network using several classification metrics.

It also demonstrates an important distinction:

```text
model
  ↓
logit
  ↓
sigmoid
  ↓
continuous score
  ↓
decision threshold
  ↓
predicted class
```

The neural network produces a continuous score.

The final classification decision depends on a threshold chosen by the application.

Changing that threshold changes the balance between different types of errors.

## Concepts

### Train/test split

The generated dataset contains:

```text
200 samples
```

It is divided into:

```text
140 training samples
60 test samples
```

corresponding to:

```text
70% training
30% testing
```

The training set is used to optimize the neural-network parameters.

The test set remains outside training and is used to evaluate how the trained model behaves on unseen samples.

Conceptually:

```text
dataset
   ↓
split
   ├── training data → learn parameters
   │
   └── test data     → evaluate generalization
```

### Avoiding data leakage

Normalization statistics are calculated only from the training set:

```python
mean = X_train.mean(dim=0)
std = X_train.std(dim=0)
```

The same statistics are then used to normalize both sets:

```python
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std
```

The test data must not influence the normalization statistics used during training.

Otherwise, information from the held-out test set would indirectly enter the training pipeline.

This is a form of **data leakage**.

The correct pattern is:

```text
training data
     ↓
calculate mean/std
     ↓
train model
     ↓
reuse same mean/std
     ↓
test data
```

### Neural-network architecture

The model uses the same basic architecture as the previous experiment:

```python
model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1)
)
```

Conceptually:

```text
4 input features
      ↓
Linear(4 → 8)
      ↓
8 hidden values
      ↓
ReLU
      ↓
Linear(8 → 1)
      ↓
logit
      ↓
sigmoid
      ↓
score between 0 and 1
```

The four input features are:

* `temperature`
* `vibration`
* `rpm`
* `pressure`

### Training

The network is trained only using `X_train` and `y_train`.

The training process follows:

```text
zero gradients
      ↓
forward pass
      ↓
loss
      ↓
backpropagation
      ↓
gradients
      ↓
optimizer step
      ↓
updated parameters
```

The model uses:

```python
nn.BCEWithLogitsLoss()
```

for binary classification and:

```python
torch.optim.Adam(...)
```

for optimization.

### Probability score and threshold

After training, the network produces a logit:

```text
-∞ ... +∞
```

Sigmoid converts it into a value between:

```text
0 ... 1
```

For example:

```text
score = 0.68
```

The model itself has produced the score.

The application must then decide which threshold converts that score into a class.

For example:

```text
threshold = 0.5

0.68 >= 0.5
→ FAILURE
```

But with:

```text
threshold = 0.7

0.68 < 0.7
→ NORMAL
```

The neural-network output has not changed.

Only the decision rule has changed.

### Confusion matrix

For binary classification, predictions can be divided into four categories:

```text
                     Predicted

                  NORMAL   FAILURE

Actual NORMAL       TN        FP

Actual FAILURE      FN        TP
```

Where:

* **TP — True Positive:** the motor is a failure and the model predicts failure.
* **TN — True Negative:** the motor is normal and the model predicts normal.
* **FP — False Positive:** the motor is normal but the model predicts failure.
* **FN — False Negative:** the motor is a failure but the model predicts normal.

These values form the confusion matrix.

For example:

```text
[[52  2]
 [ 2  4]]
```

means:

```text
TN = 52
FP = 2
FN = 2
TP = 4
```

### Accuracy

Accuracy measures the proportion of all predictions that are correct.

Conceptually:

```text
Accuracy =
correct predictions
-------------------
all predictions
```

or:

```text
Accuracy =
TP + TN
-----------
TP + TN + FP + FN
```

Accuracy is useful, but it can be misleading when classes are imbalanced.

In this test set, only:

```text
6 / 60
```

samples belong to the positive failure class.

Therefore:

```text
54 NORMAL
6 FAILURE
```

A model could achieve high accuracy while still missing important failures.

### Precision

Precision asks:

> Of all samples predicted as FAILURE, how many were actually failures?

```text
Precision =
TP
-------
TP + FP
```

High precision means that positive predictions contain relatively few false alarms.

### Recall

Recall asks:

> Of all real failures, how many did the model detect?

```text
Recall =
TP
-------
TP + FN
```

High recall means that the model misses relatively few real failures.

### F1-score

The F1-score combines precision and recall into a single metric.

It is useful when both false positives and false negatives matter.

A high F1-score generally requires both precision and recall to be reasonably strong.

### Threshold trade-off

Changing the threshold changes which scores are converted into positive predictions.

A lower threshold generally produces:

```text
more positive predictions
→ potentially higher recall
→ potentially more false positives
```

A higher threshold generally produces:

```text
fewer positive predictions
→ potentially fewer false positives
→ potentially lower recall
```

However, the exact behavior depends on the model outputs and dataset.

Raising the threshold does not guarantee that every metric will improve.

## Hypothesis

The neural network should fit the training data well.

Evaluation on the held-out test set should reveal that training performance alone does not describe generalization.

Changing the decision threshold should change the confusion matrix and the balance between precision and recall.

Increasing the threshold should generally reduce the number of positive predictions.

## Implementation

This experiment:

1. Generates 200 synthetic motor samples.
2. Creates binary labels from a known failure rule.
3. Splits the samples into training and test sets.
4. Stores the original test values for later inspection.
5. Calculates normalization statistics using only training data.
6. Normalizes both training and test data with the training statistics.
7. Creates a `4 → 8 → 1` neural network.
8. Trains the network using binary cross-entropy and Adam.
9. Measures training accuracy.
10. Performs inference on unseen test samples.
11. Evaluates thresholds `0.3`, `0.5` and `0.7`.
12. Calculates accuracy, precision, recall and F1-score.
13. Displays the confusion matrix for each threshold.
14. Traces one test sample through each network layer.
15. Prints the learned weights and biases.

## Run

Run from the repository root:

```bash
python topics/02_deep_learning/02_train_test_and_thresholds/main.py
```

## Observed results

A verified run produced:

```text
Training samples: 140
Test samples: 60
```

Training loss decreased substantially:

```text
Epoch 0, Loss:   0.7680
Epoch 100, Loss: 0.1123
Epoch 200, Loss: 0.0504
Epoch 300, Loss: 0.0301
Epoch 400, Loss: 0.0210
Epoch 500, Loss: 0.0151
Epoch 600, Loss: 0.0112
Epoch 700, Loss: 0.0084
Epoch 800, Loss: 0.0060
Epoch 900, Loss: 0.0047
```

The model reached:

```text
Training accuracy: 100%
```

The test set contained:

```text
60 samples

54 NORMAL
6 FAILURE
```

### Threshold 0.3

The confusion matrix was:

```text
[[52  2]
 [ 2  4]]
```

Therefore:

```text
TN = 52
FP = 2
FN = 2
TP = 4
```

Metrics:

| Metric               |  Value |
| -------------------- | -----: |
| Accuracy             | 93.33% |
| Precision            | 66.67% |
| Recall               | 66.67% |
| F1-score             | 66.67% |
| Positive predictions |      6 |

### Threshold 0.5

The confusion matrix was:

```text
[[52  2]
 [ 3  3]]
```

Therefore:

```text
TN = 52
FP = 2
FN = 3
TP = 3
```

Metrics:

| Metric               |  Value |
| -------------------- | -----: |
| Accuracy             | 91.67% |
| Precision            | 60.00% |
| Recall               | 50.00% |
| F1-score             | 54.55% |
| Positive predictions |      5 |

### Threshold 0.7

The confusion matrix was:

```text
[[54  0]
 [ 3  3]]
```

Therefore:

```text
TN = 54
FP = 0
FN = 3
TP = 3
```

Metrics:

| Metric               |   Value |
| -------------------- | ------: |
| Accuracy             |  95.00% |
| Precision            | 100.00% |
| Recall               |  50.00% |
| F1-score             |  66.67% |
| Positive predictions |       3 |

### Threshold comparison

| Threshold | Accuracy | Precision | Recall |     F1 | Positive predictions |
| --------: | -------: | --------: | -----: | -----: | -------------------: |
|       0.3 |   93.33% |    66.67% | 66.67% | 66.67% |                    6 |
|       0.5 |   91.67% |    60.00% | 50.00% | 54.55% |                    5 |
|       0.7 |   95.00% |   100.00% | 50.00% | 66.67% |                    3 |

Increasing the threshold from `0.3` to `0.7` reduced the number of positive predictions:

```text
6
↓
5
↓
3
```

### Training vs test performance

The model achieved:

```text
Training accuracy = 100%
```

but test accuracy remained below 100% for every tested threshold.

For the default threshold of `0.5`:

```text
Training accuracy = 100.00%
Test accuracy     = 91.67%
```

This demonstrates again that excellent training performance does not guarantee perfect performance on unseen data.

### Step-by-step analysis of one motor

One test motor had the original values:

```text
Temperature: 83.8683
Vibration:   0.4072
RPM:         4607.3477
Pressure:    2.2475
```

After normalization:

```text
[ 0.4863, -0.9633, -0.6381, -0.3380]
```

The first linear layer produced:

```text
[-3.9886,
  7.3816,
  2.7523,
  2.0381,
  2.4596,
  2.0574,
  0.1795,
 -3.5180]
```

After ReLU:

```text
[0.0000,
 7.3816,
 2.7523,
 2.0381,
 2.4596,
 2.0574,
 0.1795,
 0.0000]
```

The negative values were replaced with zero.

The second linear layer produced the logit:

```text
-38.7121
```

Sigmoid transformed it into:

```text
1.5400738157726663e-17
```

which is extremely close to zero.

Using:

```text
threshold = 0.5
```

the prediction was:

```text
NORMAL
```

The real target was:

```text
0
```

so this particular prediction was correct.

## Interpretation

### Training behavior

The training loss decreased from:

```text
0.7680
```

to approximately:

```text
0.0047
```

by epoch 900.

Training accuracy reached:

```text
100%
```

This demonstrates that the network can fit the 140 training samples extremely well.

However, the held-out test set still contains errors.

This is another demonstration that:

> Strong training performance does not guarantee perfect generalization.

### Threshold 0.3

At threshold `0.3`, the model detected:

```text
4 / 6
```

real failures.

This produced:

```text
Recall = 66.67%
```

but it also generated two false-positive alarms.

### Threshold 0.5

At threshold `0.5`, the model detected:

```text
3 / 6
```

real failures.

It also produced two false positives.

Both recall and F1-score were lower than at threshold `0.3`.

### Threshold 0.7

At threshold `0.7`, the model produced only three positive predictions.

All three were real failures:

```text
FP = 0
```

therefore:

```text
Precision = 100%
```

However, it still missed:

```text
3 / 6
```

real failures.

Therefore:

```text
Recall = 50%
```

This demonstrates why a high precision value alone does not imply that a classifier is ideal.

The model made no false-positive failure predictions at this threshold, but it still failed to detect half of the real failures.

### Accuracy and class imbalance

The test dataset contains:

```text
54 NORMAL
6 FAILURE
```

so the classes are imbalanced.

At threshold `0.7`, accuracy reaches:

```text
95%
```

which is the highest tested accuracy.

However, the model still misses:

```text
50%
```

of real failures.

Therefore, accuracy alone hides important information about classifier behavior.

For a failure-detection system, missing a real failure may be significantly more important than incorrectly raising an alarm.

That decision depends on the requirements and cost of each error type.

### Threshold selection is a product decision

The neural network does not inherently decide that:

```text
0.5
```

must be the final threshold.

The network produces a continuous score.

The application chooses how to transform that score into an action.

For example:

```text
lower threshold
→ more sensitive detector
→ potentially more detected failures
→ potentially more false alarms
```

while:

```text
higher threshold
→ more conservative positive prediction
→ fewer false alarms
→ potentially more missed failures
```

There is no universally correct threshold.

The appropriate threshold depends on the consequences of:

```text
false positive
vs
false negative
```

for the real application.

The test set should also not be repeatedly used to select the threshold, because doing so would gradually make design decisions based on the test data.

A real machine-learning workflow would normally use validation data for threshold and hyperparameter selection and reserve the final test set for unbiased evaluation.

## Learned parameters

The first layer is:

```python
nn.Linear(4, 8)
```

Therefore its weight matrix has shape:

```text
8 × 4
```

Conceptually:

```text
             temperature  vibration  rpm  pressure

neuron 1         w           w        w      w
neuron 2         w           w        w      w
neuron 3         w           w        w      w
...
neuron 8         w           w        w      w
```

This layer contains:

```text
8 × 4 = 32 weights
```

plus:

```text
8 biases
```

for a total of:

```text
40 parameters
```

The second layer is:

```python
nn.Linear(8, 1)
```

It contains:

```text
8 weights
+
1 bias
=
9 parameters
```

Therefore, the neural network contains:

```text
40 + 9 = 49 trainable parameters
```

During training:

```python
loss.backward()
```

calculates gradients for these parameters.

Then:

```python
optimizer.step()
```

updates them.

## Conclusion

This experiment extends neural-network training with proper held-out evaluation.

It demonstrates that:

1. Training performance alone is insufficient to evaluate a model.
2. Test data must remain outside training.
3. Normalization statistics must be calculated using training data only.
4. Binary classifiers produce continuous scores before a threshold is applied.
5. Changing the threshold changes the classifier's behavior without retraining the neural network.
6. Accuracy alone can hide important errors, especially with imbalanced classes.
7. Precision measures the reliability of positive predictions.
8. Recall measures how many real positive cases are detected.
9. F1 combines precision and recall.
10. Threshold selection depends on the consequences of false positives and false negatives.

The experiment also makes the internal neural-network computation visible:

```text
real input
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

## Limitations

This experiment still has several limitations:

* The dataset is synthetic.
* Only 200 samples are generated.
* Only 60 samples are used for testing.
* The positive class is relatively rare.
* Only one train/test split is evaluated.
* Only one network architecture is tested.
* Only one optimizer is tested.
* Only one learning rate is tested.
* Only three thresholds are compared.
* No independent validation set is used.
* No cross-validation is performed.
* The sigmoid scores are not evaluated for calibration.
* The synthetic rule is much simpler than a real predictive-maintenance problem.
* The model reaches 100% training accuracy, so additional experiments would be required to study whether capacity or training duration should be reduced.

The test set should not be repeatedly used to optimize thresholds or hyperparameters.

A more complete workflow would use:

```text
training set
     ↓
learn parameters

validation set
     ↓
choose architecture
hyperparameters
threshold

test set
     ↓
final unbiased evaluation
```

## Product connection

### Concept

A machine-learning model produces scores, but a real application must decide how those scores translate into actions.

### Implementation

This experiment trains a neural network on motor data and evaluates its output at multiple decision thresholds.

It measures:

* true positives,
* true negatives,
* false positives,
* false negatives,
* accuracy,
* precision,
* recall,
* F1-score.

### Product

Consider a predictive-maintenance system for industrial machinery.

A false positive could mean:

```text
machine is actually healthy
        ↓
model raises failure alarm
        ↓
unnecessary inspection or shutdown
```

A false negative could mean:

```text
machine is actually failing
        ↓
model predicts normal
        ↓
failure is missed
```

These errors may have very different costs.

Therefore, the decision threshold should be based on product and engineering requirements rather than automatically choosing `0.5`.

For a safety-critical system, missing a dangerous failure might be much more costly than producing an additional inspection alarm.

A real deployed system would require:

* representative real-world data,
* independent validation and test sets,
* threshold selection based on operational costs,
* model and preprocessing versioning,
* reproducible inference,
* calibration analysis,
* monitoring,
* drift detection,
* failure analysis,
* retraining procedures.

## Check yourself

### Why use training statistics to normalize the test set?

The test set represents unseen data.

Normalization parameters such as mean and standard deviation must therefore be calculated from training data only.

If test data is used to calculate them, information from the test set indirectly influences the training pipeline.

This creates data leakage.

The correct approach is:

```text
X_train
   ↓
calculate mean/std
   ↓
normalize X_train

same mean/std
   ↓
normalize X_test
```

### Define TP, TN, FP and FN.

```text
TP — True Positive
Actual FAILURE
Predicted FAILURE

TN — True Negative
Actual NORMAL
Predicted NORMAL

FP — False Positive
Actual NORMAL
Predicted FAILURE

FN — False Negative
Actual FAILURE
Predicted NORMAL
```

### When can high precision and low recall be desirable?

High precision and lower recall can be useful when false positives are especially expensive.

High precision means that when the model predicts the positive class, that prediction is usually correct.

However, lower recall means that some real positive cases are missed.

Whether this trade-off is acceptable depends on the application.

### Why does a threshold of 0.7 usually reduce positive predictions?

For a prediction to be classified as positive at threshold `0.7`, its score must satisfy:

```text
score >= 0.7
```

This is a stricter requirement than:

```text
score >= 0.5
```

or:

```text
score >= 0.3
```

Therefore, fewer samples usually satisfy the condition.

In this experiment:

```text
threshold 0.3 → 6 positive predictions
threshold 0.5 → 5 positive predictions
threshold 0.7 → 3 positive predictions
```

### What is stored inside `model[0].weight`?

`model[0]` is:

```python
nn.Linear(4, 8)
```

Its `.weight` contains the learned connection weights between the four input features and the eight hidden neurons.

Its shape is:

```text
[8, 4]
```

meaning:

```text
8 hidden neurons
×
4 input weights per neuron
```

Therefore it contains:

```text
32 trainable weights
```

Each hidden neuron learns its own weighted combination of:

* temperature,
* vibration,
* RPM,
* pressure.

### What changes between training and inference?

During training:

```text
input
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
weights and biases change
```

During inference:

```text
input
 ↓
forward pass
 ↓
output
```

The learned weights and biases are reused but are not modified.

Therefore:

```text
training
→ learns parameters

inference
→ uses parameters
```

### Why is accuracy alone insufficient here?

The test set contains:

```text
54 normal samples
6 failure samples
```

This means the classes are imbalanced.

At threshold `0.7`, the classifier reaches:

```text
95% accuracy
```

but still detects only:

```text
3 / 6
```

failures.

Therefore:

```text
Recall = 50%
```

The high accuracy does not reveal that half of the real failures were missed.

Metrics such as precision, recall, F1-score and the confusion matrix provide additional information about the types of errors being made.

### Why can changing the threshold alter predictions without retraining the model?

The trained network produces a continuous score.

For example:

```text
score = 0.65
```

With:

```text
threshold = 0.5
```

the prediction is:

```text
FAILURE
```

but with:

```text
threshold = 0.7
```

the same model output becomes:

```text
NORMAL
```

Nothing inside the neural network changed.

Only the rule used to convert the continuous score into a discrete class changed.

### Why should we not choose the final threshold using the test set repeatedly?

The test set should represent unseen data used for final evaluation.

If we repeatedly inspect test performance and modify the threshold based on those results, information from the test set begins to influence our design decisions.

The test set is no longer completely independent.

A more appropriate workflow is:

```text
training set
→ train parameters

validation set
→ choose threshold and hyperparameters

test set
→ final evaluation
```