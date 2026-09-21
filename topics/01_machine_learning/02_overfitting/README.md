# Experiment 02 — Overfitting and Generalization

## Objective

Why do we evaluate a model on data that was not used to fit it?

## Concepts

A model generalizes when it performs well on unseen samples, not merely on the examples it memorized during training.

Overfitting occurs when a model learns details of the training set that do not transfer reliably to new data.

## Hypothesis

A depth-limited tree should have a training/test gap on noisy synthetic labels; its size must be measured.

## Implementation

The script generates 200 synthetic motors. The underlying failure rule depends on temperature and vibration, then 5% label noise is introduced.

A decision tree with `max_depth=2` is trained on 70% of the data and evaluated independently on the remaining 30%.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/01_machine_learning/02_overfitting/main.py
```

## Observed results

Not verified yet on the current environment.

Historical evidence retained from the supplied notes (environment, dependency versions and raw logs were not recorded):

Previously recorded run:

```text
Training accuracy: 0.9714285714285714
Test accuracy: 0.9166666666666666
```

## Interpretation

The historical training/test gap is consistent with imperfect generalization. There is no unconstrained-tree comparison, so this run does not establish that limiting depth improved performance.

## Conclusion

The recorded run supports evaluating held-out data separately. The benefit of a depth constraint remains untested.

## Limitations

The dataset is synthetic and generated from a very simple known rule. Real-world data can contain drift, correlations, missing data, sensor faults and much more complex relationships.

One train/test split also has sampling variance. Later experiments should introduce validation and repeated evaluation where appropriate.

Each label has a 5% chance of flipping; the realized fraction need not equal exactly 5%. Only one tree depth is run.

## Product connection

**Concept:** Why do we evaluate a model on data that was not used to fit it?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Monitoring systems need held-out evaluation to estimate behavior on future measurements.

## Check yourself

- Why must test data stay outside training?
- What does a training/test gap tell us?
- Why can reducing model capacity help?
- What is label noise?
- Why is one random split not the final word on performance?
