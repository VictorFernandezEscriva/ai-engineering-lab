# Experiment 04 — Neural Network Evaluation and Thresholds

## Objective

How do we evaluate a classifier on unseen data, and how does changing the decision threshold change its behavior?

## Concepts

A binary neural classifier produces a continuous score. The application chooses a threshold to convert that score into a class.

Changing the threshold changes the balance between false positives and false negatives, which is why accuracy alone is often insufficient.

## Hypothesis

Raising the threshold should reduce positive predictions; precision need not improve on every dataset.

## Implementation

This experiment:

1. generates 200 synthetic motor samples,
2. creates labels from a known rule,
3. splits the data into train and test,
4. computes normalization statistics using training data,
5. trains a `4 → 8 → 1` network,
6. computes probabilities for unseen test data,
7. compares thresholds `0.3`, `0.5` and `0.7`,
8. reports confusion matrix, precision, recall and F1,
9. traces one sample layer-by-layer,
10. prints the learned weights and biases.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/02_deep_learning/02_train_test_and_thresholds/main.py
```

## Observed results

Not verified yet on the current environment.

Historical evidence retained from the supplied notes (environment, dependency versions and raw logs were not recorded):

Previously recorded run:

| Threshold | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.3 | 0.667 | 0.667 | 0.667 |
| 0.5 | 0.600 | 0.500 | 0.545 |
| 0.7 | 1.000 | 0.500 | 0.667 |

Training accuracy was `1.0`, while the test confusion matrices still contained errors.

For one inspected test motor, the network produced a large negative logit and a sigmoid value near zero, resulting in the prediction `NORMAL`, matching the generated target.

## Interpretation

The historical metrics illustrate threshold-dependent errors. A fixed seed does not guarantee identical results across library versions or hardware.

## Conclusion

The recorded run supports reporting multiple error metrics and explicitly choosing a decision threshold.

## Limitations

The positive class is relatively rare in this synthetic dataset, and the test set is still small. Threshold behavior can vary across different samples or seeds.

A real safety-critical threshold must be chosen using domain costs and validated data, not by selecting the prettiest metric after seeing the test set.

## Product connection

**Concept:** How do we evaluate a classifier on unseen data, and how does changing the decision threshold change its behavior?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Fraud alert systems use precision and recall to reason about false alarms and missed events.

## Check yourself

- Why use training statistics to normalize the test set?
- Define TP, TN, FP and FN.
- When can high precision and low recall be desirable?
- Why does a threshold of 0.7 usually reduce positive predictions?
- What is stored inside `model[0].weight`?
- What changes between training and inference?
