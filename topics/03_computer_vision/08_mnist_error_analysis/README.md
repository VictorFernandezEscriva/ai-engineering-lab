# Experiment 12 — MNIST Error Analysis

## Objective

A single accuracy value does not explain where a classifier fails.

The previous experiment achieved high test accuracy on MNIST.

This experiment goes beyond aggregate accuracy and asks:

```text
Which digits are classified reliably?

Which digits are more difficult?

Which classes are confused with each other?

What do misclassified examples look like?
```

The objective is to introduce systematic model error analysis.

## Concepts

### Overall accuracy

Overall accuracy measures:

```text
correct predictions
/
total predictions
```

For example:

```text
9855 correct predictions
/
10000 test images
=
98.55% accuracy
```

This is useful, but it hides differences between individual classes.

A classifier may perform very well overall while having weaker performance on specific classes.

### Confusion matrix

A confusion matrix shows how real classes are mapped to predicted classes.

For MNIST:

```text
rows    = real digit
columns = predicted digit
```

For example, a row such as:

```text
[90, 2, 8]
```

could mean:

```text
90 samples correctly predicted as class 0
2 samples predicted as class 1
8 samples predicted as class 2
```

The diagonal contains correct predictions:

```text
0 → 0
1 → 1
2 → 2
...
9 → 9
```

Values outside the diagonal represent classification errors.

### Per-class accuracy

Overall accuracy combines every class into one number.

Per-class accuracy instead calculates:

```text
correct predictions for one digit
/
total test samples of that digit
```

This reveals whether some digits are systematically harder than others.

### Misclassification mask

The experiment identifies incorrect predictions using:

```python
incorrect_mask = predictions != labels
```

Conceptually:

```text
prediction:
[7, 2, 1, 9, 4]

label:
[7, 2, 1, 0, 4]

incorrect mask:
[False, False, False, True, False]
```

The `True` value identifies the incorrectly classified sample.

This mask can then select only the incorrect images:

```python
incorrect_images = images[incorrect_mask]
```

### Error analysis

Error analysis means investigating the failures of a trained model rather than only reporting a final metric.

A useful workflow is:

```text
model
↓
predictions
↓
aggregate metrics
↓
per-class metrics
↓
confusion matrix
↓
misclassified examples
↓
failure hypotheses
```

This helps identify what should be improved next.

## Hypothesis

The CNN should retain high overall test accuracy.

However, some handwritten digits should be more difficult than others.

The confusion matrix and per-class metrics should reveal specific failure patterns that are hidden by overall accuracy.

## Implementation

The experiment:

1. Loads MNIST.
2. Creates training and test DataLoaders.
3. Creates the same small CNN architecture used previously.
4. Trains the network for three epochs.
5. Runs inference across the complete test dataset.
6. Stores every true label.
7. Stores every predicted label.
8. Identifies misclassified samples.
9. Calculates overall test accuracy.
10. Builds a 10-class confusion matrix.
11. Calculates accuracy for each digit.
12. Finds the most frequent class confusions.
13. Stores incorrectly classified images.
14. Displays several misclassified examples.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/08_mnist_error_analysis/main.py
```

MNIST is reused from the local:

```text
data/
```

directory.

The script opens a Matplotlib window showing misclassified images.

## Observed results

A verified run used:

```text
Training samples: 60000
Test samples: 10000
```

### Training loss

Training produced:

```text
Epoch 1/3, Loss: 0.2636
Epoch 2/3, Loss: 0.0775
Epoch 3/3, Loss: 0.0569
```

The training loss decreased substantially across the three epochs.

### Overall results

The final test evaluation produced:

```text
Correct predictions:   9855
Incorrect predictions: 145
Test accuracy:          0.9855
```

Therefore:

```text
Test accuracy = 98.55%
```

Out of 10,000 test images:

```text
9855 were classified correctly
145 were classified incorrectly
```

### Confusion matrix

The verified confusion matrix was:

```text
[[ 977    0    0    0    1    0    0    1    1    0]
 [   0 1131    2    0    0    0    0    2    0    0]
 [   3    5 1010    1    1    0    0    8    4    0]
 [   1    0    0  999    0    4    0    4    2    0]
 [   0    0    0    0  973    0    1    3    3    2]
 [   2    0    0    5    0  881    1    0    1    2]
 [   8    1    0    1    1    1  944    0    2    0]
 [   0    2    4    1    0    0    0 1020    1    0]
 [  11    1    2    1    2    1    0    6  944    6]
 [   6    4    1    1    6    4    0   10    1  976]]
```

The large values along the diagonal show that most examples were classified correctly.

The off-diagonal values identify specific errors.

### Per-class accuracy

The verified per-class results were:

```text
Digit 0: 977/980  = 0.9969
Digit 1: 1131/1135 = 0.9965
Digit 2: 1010/1032 = 0.9787
Digit 3: 999/1010 = 0.9891
Digit 4: 973/982  = 0.9908
Digit 5: 881/892  = 0.9877
Digit 6: 944/958  = 0.9854
Digit 7: 1020/1028 = 0.9922
Digit 8: 944/974  = 0.9692
Digit 9: 976/1009 = 0.9673
```

Expressed approximately as percentages:

```text
Digit 0 → 99.69%
Digit 1 → 99.65%
Digit 2 → 97.87%
Digit 3 → 98.91%
Digit 4 → 99.08%
Digit 5 → 98.77%
Digit 6 → 98.54%
Digit 7 → 99.22%
Digit 8 → 96.92%
Digit 9 → 96.73%
```

The strongest classes in this run were:

```text
0
1
7
```

The weakest classes were:

```text
9
8
2
```

### Most common confusions

The ten most frequent errors were:

```text
Real 8 predicted as 0: 11
Real 9 predicted as 7: 10
Real 6 predicted as 0: 8
Real 2 predicted as 7: 8
Real 9 predicted as 4: 6
Real 9 predicted as 0: 6
Real 8 predicted as 9: 6
Real 8 predicted as 7: 6
Real 5 predicted as 3: 5
Real 2 predicted as 1: 5
```

These results reveal error patterns that were invisible in the overall accuracy metric.

## Interpretation

### Overall performance

The CNN achieved:

```text
98.55% test accuracy
```

which indicates strong performance on MNIST.

However, the 145 incorrect predictions demonstrate that the model is not equally reliable for every sample.

### Class-dependent performance

Digits `0` and `1` were classified extremely reliably:

```text
0 → 99.69%
1 → 99.65%
```

Digits `8` and `9` were more difficult:

```text
8 → 96.92%
9 → 96.73%
```

Therefore the aggregate accuracy:

```text
98.55%
```

does not describe the complete model behavior.

### Frequent confusion patterns

The most common individual confusion was:

```text
8 → 0
```

with 11 occurrences.

Another frequent error was:

```text
9 → 7
```

with 10 occurrences.

The experiment does not establish exactly why these errors occurred.

Visual inspection of the corresponding images is required before attributing specific visual causes.

Possible explanations should therefore be treated as hypotheses rather than verified conclusions.

### Error analysis vs accuracy

Previously the evaluation pipeline was approximately:

```text
test dataset
↓
model
↓
accuracy
```

This experiment extends it to:

```text
test dataset
↓
model
↓
predictions
↓
overall accuracy
↓
per-class accuracy
↓
confusion matrix
↓
misclassified samples
↓
error analysis
```

This provides a much more useful understanding of model behavior.

## Conclusion

The CNN classified:

```text
9855 / 10000
```

MNIST test images correctly, achieving:

```text
98.55%
```

test accuracy.

However, error analysis revealed meaningful differences between classes.

The lowest-performing classes were:

```text
Digit 9 → 96.73%
Digit 8 → 96.92%
Digit 2 → 97.87%
```

while digits such as `0` and `1` exceeded 99.6% accuracy.

The experiment demonstrates that evaluation should not stop at a single aggregate metric.

A stronger machine-learning workflow includes:

```text
overall metric
+
class-specific metrics
+
confusion analysis
+
example inspection
```

## Limitations

This experiment still has several limitations:

* only one model architecture is tested,
* only one random seed is used,
* only three epochs are used,
* there is no validation dataset,
* there is no data augmentation,
* there is no hyperparameter search,
* no model checkpoint is loaded from the previous experiment,
* errors are inspected manually rather than categorized automatically,
* no confidence analysis is performed for incorrect predictions,
* no probability calibration is evaluated.

The model is retrained inside this experiment instead of loading previously saved weights.

This keeps the experiment self-contained but introduces some repeated computation.

## Product connection

### Concept

Production ML systems must understand not only how often a model fails, but also where and how it fails.

### Implementation

The evaluation pipeline becomes:

```text
predictions
↓
accuracy
↓
confusion matrix
↓
per-class metrics
↓
failure examples
```

### Product

Consider an industrial visual-inspection model with:

```text
99% overall accuracy
```

If one critical defect class only achieves:

```text
70% accuracy
```

the overall metric could hide a serious product risk.

The same principle applies to:

* defect detection,
* medical imaging,
* document classification,
* autonomous systems,
* satellite imagery,
* fraud detection.

Model evaluation should therefore consider failure distribution, not only aggregate performance.

## Check yourself

### Why is overall accuracy insufficient?

Overall accuracy combines every class into one metric.

It can hide weaker performance on specific classes.

### What does a confusion matrix show?

It compares real classes against predicted classes.

Rows represent real labels and columns represent predicted labels.

### What does the diagonal represent?

Correct predictions:

```text
real class = predicted class
```

### What do values outside the diagonal represent?

Classification errors.

For example:

```text
row 8
column 0
```

means:

```text
real digit 8
predicted digit 0
```

### Which digit performed worst in this experiment?

Digit `9`:

```text
976 / 1009
=
96.73%
```

### Which digit performed best?

Digit `0`:

```text
977 / 980
=
99.69%
```

Digit `1` was very close:

```text
1131 / 1135
=
99.65%
```

### What was the most common confusion?

```text
Real 8
→
Predicted 0
```

with 11 occurrences.

### What does the incorrect mask do?

```python
predictions != labels
```

returns a boolean tensor identifying samples where the model prediction differs from the correct label.

### Why inspect misclassified images?

Metrics tell us that an error occurred.

The original image can provide evidence about what type of sample caused the failure.

This allows more informed hypotheses about how to improve the system.

### Does a confusion matrix explain why the model failed?

No.

It identifies which classes were confused.

Understanding why requires additional analysis of the images, learned representations, data and model behavior.