# Experiment 08 — Shape CNN Evaluation and Feature Maps

## Objective

Does the trained shape classifier generalize to unseen generated images, and what is happening inside its convolution layers?

## Concepts

This experiment adds two missing pieces to the previous CNN:

1. independent train/test evaluation,
2. inspection of learned filters and intermediate feature maps.

A neural network is easier to reason about when we inspect not only its final prediction but also intermediate tensor shapes and representations.

## Hypothesis

Held-out accuracy may differ from training accuracy; internal maps should expose the network tensor shapes.

## Implementation

The script:

- generates the synthetic circle/square dataset,
- performs an 80/20 train/test split,
- trains the CNN on the training data only,
- computes training and test accuracy,
- prints a confusion matrix,
- inspects example probabilities,
- prints the learned first-layer filters,
- visualizes first- and second-layer feature maps.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/03_computer_vision/04_shapes_evaluation/main.py
```

## Observed results

Not verified yet on the current environment.

No numerical result is claimed. See the [verification log](../../../docs/verification.md) for current execution blockers.

## Interpretation

No measured generalization outcome is available here. Feature maps can reveal computation without proving that the network uses human-like shape reasoning.

## Conclusion

The implementation includes held-out evaluation and internal inspection. Its empirical outcome remains unverified.

## Limitations

Synthetic circles and squares are far simpler than natural images. High accuracy here would validate the mechanics of the pipeline, not prove robustness on real computer-vision tasks.

The images have fixed sizes and brightness, one seed, and possible duplicate generated images across samples. Shape area can be a shortcut; there is no independent generator or validation set. Training uses 1000 full-batch CPU epochs. Plot windows are interactive. `torch.no_grad()` disables gradient recording; it is not a substitute for `model.eval()` in architectures with dropout or batch normalization (neither is used here).

## Product connection

**Concept:** Does the trained shape classifier generalize to unseen generated images, and what is happening inside its convolution layers?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Vision evaluation dashboards compare predictions and inspect intermediate representations when diagnosing errors.

## Check yourself

- Why use `torch.no_grad()` during inspection?
- What is the difference between a filter tensor and a feature map?
- Why do spatial dimensions shrink after pooling?
- How could you save figures instead of opening interactive windows?
