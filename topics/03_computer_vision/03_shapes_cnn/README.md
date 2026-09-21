# Experiment 07 — CNN for Circles vs Squares

## Objective

Can a CNN learn filters useful for distinguishing simple shapes instead of receiving manually designed kernels?

## Concepts

The network combines learned convolutions, nonlinearities and pooling:

```text
32×32 grayscale image
        ↓
Conv2d 1→16
        ↓
ReLU
        ↓
MaxPool
        ↓
Conv2d 16→32
        ↓
ReLU
        ↓
MaxPool
        ↓
Flatten
        ↓
Linear → logit
```

Unlike the previous experiments, convolution weights are trainable parameters.

## Hypothesis

Learned convolution filters should reduce training loss on the generated shapes.

## Implementation

The script generates 1000 synthetic `32 × 32` images containing either a circle or a square at a randomized position.

This makes the learning target simple while still varying position; the experiment does not establish which visual cues the model learns.

The model uses:

- `BCEWithLogitsLoss`,
- Adam,
- 1000 full-batch training epochs.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/03_computer_vision/03_shapes_cnn/main.py
```

## Observed results

Not verified yet on the current environment.

No numerical result is claimed. See the [verification log](../../../docs/verification.md) for current execution blockers.

## Interpretation

No measured learning outcome is available here. Falling loss would indicate training fit only; this script does not print classification accuracy.

## Conclusion

The implementation connects trainable convolutions to a binary loss. Its training outcome remains unverified.

## Limitations

This first version trains on all generated samples and does not evaluate a separate test set. Even if training loss becomes tiny, that alone cannot demonstrate generalization.

The evaluation experiment adds a held-out split, but still uses synthetic data.

The images have fixed sizes and brightness, one seed, and possible duplicate generated images across samples. Shape area can be a shortcut; there is no independent generator or validation set. Training uses 1000 full-batch CPU epochs.

## Product connection

**Concept:** Can a CNN learn filters useful for distinguishing simple shapes instead of receiving manually designed kernels?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Visual inspection software can learn features from images, but needs representative defects and independent evaluation.

## Check yourself

- Why does the second convolution use `in_channels=16`?
- Why is the final linear input `32 * 8 * 8`?
- What information can pooling remove?
- Why can low training loss be misleading here?
