# Experiment 01 — Decision Tree Failure Classification

## Objective

Can a simple supervised-learning model infer decision rules from labelled motor measurements?

## Concepts

A decision tree repeatedly splits the feature space using rules such as:

```text
temperature <= threshold
```

Training chooses splits that separate the target classes. Inference follows the learned branches until reaching a predicted class.

## Hypothesis

A small decision tree should learn rules that separate the supplied motor labels.

## Implementation

`main.py`:

1. creates a small pandas dataset,
2. separates features `X` from target `y`,
3. performs a train/test split,
4. trains `DecisionTreeClassifier`,
5. predicts the held-out samples,
6. evaluates accuracy,
7. predicts one new motor,
8. prints the learned tree as text.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/01_machine_learning/01_decision_tree/main.py
```

## Observed results

Not verified yet on the current environment.

Historical evidence retained from the supplied notes (environment, dependency versions and raw logs were not recorded):

A previously recorded run produced:

```text
Accuracy: 1.0
Prediction: [1]
```

and a tree whose first major split used temperature.

## Interpretation

The historical score describes two held-out rows only. The predicted motor also duplicates an existing dataset row, so it is not independent new evidence.

## Conclusion

The recorded run supports inspecting learned tree rules on a tiny labelled example, not reliable motor failure prediction.

## Limitations

The dataset contains only ten rows and the test split contains only two samples. Therefore `1.0` accuracy is **not** evidence that the model would achieve 100% accuracy on real motors.

This is a mechanics experiment, not a production predictive-maintenance model.

## Product connection

**Concept:** Can a simple supervised-learning model infer decision rules from labelled motor measurements?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Predictive-maintenance software can use classifiers to prioritize inspection; representative sensor histories and error costs would be needed.

## Check yourself

You should be able to explain:

- What are `X` and `y`?
- What does `fit()` change?
- What does `predict()` do after training?
- Why is a 100% test score weak evidence when the test set has only two samples?
- What is a model parameter vs a hyperparameter such as tree depth?
