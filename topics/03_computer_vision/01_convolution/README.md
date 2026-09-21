# Experiment 05 — Manual Convolution Kernel

## Objective

What does a convolution filter actually compute before we ask a CNN to learn filters automatically?

## Concepts

A convolution kernel slides across an image. At each position it combines nearby pixel values with kernel weights to produce one output value.

The resulting grid is a **feature map**.

## Hypothesis

The fixed kernel should give opposite signs at opposite edges and zero on uniform patches.

## Implementation

The experiment creates a simple `5 × 5` image containing a bright square and applies the fixed kernel:

```text
[-1,  1]
[-1,  1]
```

The `Conv2d` layer is used as the computation engine, but its weights are manually replaced with the known kernel instead of learned by training.

PyTorch `Conv2d` expects:

```text
[batch, channels, height, width]
```

The original matrix contains only `[height, width]`, so two singleton dimensions are added.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/03_computer_vision/01_convolution/main.py
```

## Observed results

Not verified yet on the current environment.

Historical evidence retained from the supplied notes (environment, dependency versions and raw logs were not recorded):

Previously recorded feature map:

```text
[[ 1, 0, 0,-1],
 [ 2, 0, 0,-2],
 [ 2, 0, 0,-2],
 [ 1, 0, 0,-1]]
```

## Interpretation

The historical signs follow weighted sums of local pixels. PyTorch uses cross-correlation: it does not flip this kernel.

## Conclusion

The recorded output supports the local weighted-sum mechanism for this fixed image and kernel.

## Limitations

This is not a learned CNN. We manually chose a tiny filter and a synthetic image so the arithmetic is easy to inspect.

## Product connection

**Concept:** What does a convolution filter actually compute before we ask a CNN to learn filters automatically?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Image processing systems use local filters to extract spatial signals.

## Check yourself

- Why does the output become `4 × 4` rather than `5 × 5` here?
- What do batch and channel dimensions mean?
- Why do left and right transitions have opposite signs?
- What would padding change?
