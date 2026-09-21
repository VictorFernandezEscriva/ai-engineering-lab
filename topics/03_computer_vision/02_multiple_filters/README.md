# Experiment 06 — Multiple Convolution Filters

## Objective

What happens when one convolution layer contains several filters?

## Concepts

A convolution layer can learn many filters. Each output filter produces its own feature map.

Conceptually:

```text
one input image
      ↓
filter 1 → feature map 1
filter 2 → feature map 2
filter 3 → feature map 3
```

## Hypothesis

Three kernels should produce three output channels with different signed responses.

## Implementation

The experiment uses one single-channel image and a `Conv2d` layer with:

```python
in_channels=1
out_channels=3
```

Three hand-written kernels respond to different transitions.

## Run

Run from the repository root after installing `requirements.txt`:

```bash
python topics/03_computer_vision/02_multiple_filters/main.py
```

## Observed results

Not verified yet on the current environment.

Historical evidence retained from the supplied notes (environment, dependency versions and raw logs were not recorded):

Previously recorded output shape:

```text
torch.Size([1, 3, 4, 4])
```

The second dimension is `3` because the layer produces three feature maps.

The three maps contain different signed patterns, confirming that different kernels extract different local features from the same input.

## Interpretation

The historical tensor shape separates batch size, output channels, height and width. Opposite kernels yield opposite responses.

## Conclusion

The recorded output supports one feature map per output channel for these manually assigned filters.

## Limitations

The filters are manually chosen. A trained CNN learns useful filters from an optimization objective.

## Product connection

**Concept:** What happens when one convolution layer contains several filters?

**Implementation:** The small demonstration in `main.py`, described above.

**Product:** Vision models combine multiple feature channels to construct richer representations.

## Check yourself

- Why is the output shape `[1, 3, 4, 4]`?
- What does each of the four dimensions mean?
- What is the relationship between a filter and an output channel?
- Why can later layers benefit from several different feature maps?
