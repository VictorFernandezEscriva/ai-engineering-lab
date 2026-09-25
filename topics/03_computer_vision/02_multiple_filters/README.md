# Experiment 06 — Multiple Convolution Filters

## Objective

What happens when a convolutional layer contains several filters instead of only one?

The previous experiment used one manually defined convolution filter and produced one feature map.

This experiment extends that idea:

```text
1 filter
→ 1 feature map

3 filters
→ 3 feature maps
```

The objective is to understand how several filters can extract different spatial information from the same input image.

## Concepts

### One image, multiple filters

The input image is the same `5 × 5` grayscale image used in the previous experiment:

```text
0 0 0 0 0
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
0 0 0 0 0
```

Its original shape is:

```text
[5, 5]
```

Before passing it to `Conv2d`, batch and channel dimensions are added:

```python
image = image.unsqueeze(0).unsqueeze(0)
```

The final input shape becomes:

```text
[1, 1, 5, 5]
```

which represents:

```text
1 image
1 input channel
5 pixels high
5 pixels wide
```

### Multiple output channels

The convolution layer is defined as:

```python
conv = nn.Conv2d(
    in_channels=1,
    out_channels=3,
    kernel_size=2,
    stride=1,
    padding=0,
    bias=False
)
```

The key parameter in this experiment is:

```python
out_channels=3
```

This means the layer contains three output filters.

Each filter produces its own feature map.

Conceptually:

```text
                    filter 1
                  ↗
input image ──────→ filter 2
                  ↘
                    filter 3

        ↓

3 output feature maps
```

Therefore:

```text
number of filters
=
number of output channels
=
number of feature maps
```

### Filter 1

The first filter is:

```text
[-1  1]
[-1  1]
```

It responds positively to one direction of horizontal intensity change.

For example:

```text
[0 1]
[0 1]
```

produces:

```text
0 × -1
+
1 × 1
+
0 × -1
+
1 × 1
=
2
```

This filter responds strongly to one orientation of a vertical edge.

### Filter 2

The second filter is:

```text
[ 1 -1]
[ 1 -1]
```

It is exactly the negative of the first filter:

```text
filter_2 = -filter_1
```

Therefore, its feature map should also be the negative of the first feature map:

```text
feature_map_2
=
-feature_map_1
```

A transition that produces:

```text
+2
```

with the first filter should produce:

```text
-2
```

with the second filter.

This demonstrates that filters can respond differently to the orientation of the same type of spatial pattern.

### Filter 3

The third filter is:

```text
[-1 -1]
[ 1  1]
```

This filter compares the upper part of a local region with the lower part.

For example:

```text
[0 0]
[1 1]
```

produces:

```text
0 × -1
+
0 × -1
+
1 × 1
+
1 × 1
=
2
```

This means that the filter responds to vertical intensity changes and therefore detects horizontal edges.

### Filter weights

The weights of a `Conv2d` layer have the shape:

```text
[out_channels, in_channels, kernel_height, kernel_width]
```

In this experiment:

```text
[3, 1, 2, 2]
```

because there are:

```text
3 output filters
1 input channel
2 × 2 kernel per filter
```

The filters are manually assigned using:

```python
with torch.no_grad():
    conv.weight[0, 0] = filter_1
    conv.weight[1, 0] = filter_2
    conv.weight[2, 0] = filter_3
```

The first index selects the output filter.

The second index selects the input channel.

For example:

```python
conv.weight[2, 0]
```

means:

```text
output filter 2
input channel 0
```

### Output tensor shape

The output shape is:

```text
[1, 3, 4, 4]
```

PyTorch image tensors use:

```text
[batch, channels, height, width]
```

Therefore:

```text
[1, 3, 4, 4]

1 → batch size
3 → output channels / feature maps
4 → height
4 → width
```

The spatial dimensions are still `4 × 4` because:

```text
input size = 5
kernel size = 2
stride = 1
padding = 0
```

and therefore:

```text
5 - 2 + 1 = 4
```

### Feature maps

Each filter produces its own spatial output:

```text
filter 1
→ feature map 1

filter 2
→ feature map 2

filter 3
→ feature map 3
```

The three maps represent different responses to the same original image.

This allows the convolutional layer to build a richer representation than a single filter could provide.

### Why multiple filters are useful

An image can contain many different spatial patterns.

A single filter can only respond strongly to one type or family of patterns.

A convolutional layer can therefore use many filters:

```text
input image
   │
   ├── filter 1 → vertical edge feature
   ├── filter 2 → opposite edge orientation
   ├── filter 3 → horizontal edge feature
   ├── filter 4 → another learned pattern
   └── ...
```

The resulting feature maps are passed together to later layers.

Those later layers can combine information from several channels to construct more complex representations.

## Hypothesis

Three manually defined filters should produce three separate output feature maps.

Because the first two filters are exact opposites:

```text
filter_2 = -filter_1
```

their feature maps should also contain opposite values.

The third filter should respond to horizontal edges rather than the vertical-edge orientations emphasized by the first two filters.

The expected output shape is:

```text
[1, 3, 4, 4]
```

because there is:

```text
1 input image
3 output filters
4 × 4 spatial output
```

## Implementation

The experiment:

1. Creates a synthetic `5 × 5` grayscale image.
2. Adds batch and channel dimensions.
3. Creates a convolutional layer with three output channels.
4. Defines three different `2 × 2` filters.
5. Manually assigns each filter to one output channel.
6. Applies all three filters to the same input image.
7. Prints the complete output tensor shape.
8. Prints each feature map independently.

No training takes place.

The filters are manually selected so their behavior can be inspected directly.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/02_multiple_filters/main.py
```

## Observed results

A verified run produced the original image:

```text
tensor([[0., 0., 0., 0., 0.],
        [0., 1., 1., 1., 0.],
        [0., 1., 1., 1., 0.],
        [0., 1., 1., 1., 0.],
        [0., 0., 0., 0., 0.]])
```

The original image shape was:

```text
torch.Size([5, 5])
```

After adding batch and channel dimensions:

```text
torch.Size([1, 1, 5, 5])
```

The convolution layer produced:

```text
torch.Size([1, 3, 4, 4])
```

Therefore:

```text
batch size       = 1
output channels  = 3
feature-map size = 4 × 4
```

The number of output feature maps was:

```text
3
```

### Feature map 1

The first filter produced:

```text
tensor([[ 1.,  0.,  0., -1.],
        [ 2.,  0.,  0., -2.],
        [ 2.,  0.,  0., -2.],
        [ 1.,  0.,  0., -1.]])
```

This is the same edge response observed in the previous convolution experiment.

### Feature map 2

The second filter produced:

```text
tensor([[-1.,  0.,  0.,  1.],
        [-2.,  0.,  0.,  2.],
        [-2.,  0.,  0.,  2.],
        [-1.,  0.,  0.,  1.]])
```

This feature map is exactly the negative of feature map 1.

For example:

```text
feature map 1 →  2
feature map 2 → -2
```

and:

```text
feature map 1 → -2
feature map 2 →  2
```

This is expected because:

```text
filter_2 = -filter_1
```

### Feature map 3

The third filter produced:

```text
tensor([[ 1.,  2.,  2.,  1.],
        [ 0.,  0.,  0.,  0.],
        [ 0.,  0.,  0.,  0.],
        [-1., -2., -2., -1.]])
```

The strong responses appear at the top and bottom boundaries of the bright square.

This demonstrates that the third filter responds to horizontal edges.

### Comparison

The three filters extract different information from exactly the same input image:

```text
same input image
      │
      ├── feature map 1
      │   vertical-edge orientation
      │
      ├── feature map 2
      │   opposite vertical-edge orientation
      │
      └── feature map 3
          horizontal edges
```

This confirms the hypothesis that several filters can create different feature channels from the same input.

## Interpretation

The most important result is the tensor shape:

```text
[1, 3, 4, 4]
```

Compared with the previous experiment:

```text
previous:
[1, 1, 4, 4]

current:
[1, 3, 4, 4]
```

The spatial dimensions did not change because the kernel size, stride and padding remained the same.

The difference is the number of output channels:

```text
1 → 3
```

because the convolution layer now contains three filters.

This demonstrates the relationship:

```text
out_channels
=
number of filters
=
number of output feature maps
```

The first and second feature maps also confirm that opposite kernels produce opposite responses.

The third feature map demonstrates that a different kernel can detect a different spatial orientation.

## Conclusion

This experiment demonstrates how a convolutional layer creates multiple feature maps from the same input image.

A convolutional layer does not need to represent an image using only one spatial feature.

Instead:

```text
one input
    ↓
multiple filters
    ↓
multiple feature maps
    ↓
richer internal representation
```

Each output channel represents the response of one filter across the spatial dimensions of the input.

In this experiment the filters are manually selected.

In a trained CNN, the same general structure remains:

```text
many filters
    ↓
many feature maps
```

but the kernel values are learned automatically using:

```text
loss
↓
backpropagation
↓
gradients
↓
optimizer
↓
learned convolution filters
```

## Limitations

This experiment is intentionally simple.

It uses:

* one synthetic image,
* one grayscale input channel,
* three manually selected filters,
* `2 × 2` kernels,
* stride `1`,
* padding `0`,
* no bias,
* no activation function after convolution,
* no pooling,
* no training.

The filters are not learned from data.

A real CNN can contain tens, hundreds or more output channels and multiple convolutional layers.

The meaning of learned filters is also not necessarily as simple or human-readable as the manually designed edge filters used here.

## Product connection

### Concept

A useful visual representation usually requires more than one type of spatial feature.

### Implementation

The same image is processed by three different convolution filters.

Each filter creates a separate output channel containing its own feature map.

### Product

Real computer-vision models use many learned convolution filters to build richer image representations.

Early layers may learn filters responding to patterns such as:

```text
edges
orientations
textures
simple local structures
```

Later convolutional layers receive several feature maps simultaneously and can combine those signals into more complex representations.

Conceptually:

```text
pixels
  ↓
multiple simple feature maps
  ↓
combined features
  ↓
more complex patterns
  ↓
visual representation
  ↓
prediction
```

This principle is used in applications such as:

```text
image classification
object detection
industrial defect detection
medical imaging
autonomous perception
```

## Check yourself

### Why is the output shape `[1, 3, 4, 4]`?

PyTorch convolution outputs use the structure:

```text
[batch, channels, height, width]
```

Therefore:

```text
[1, 3, 4, 4]
```

means:

```text
1 image
3 output feature maps
4 pixels high
4 pixels wide
```

There are three channels because:

```python
out_channels=3
```

The spatial size becomes `4 × 4` because a `2 × 2` kernel is applied to a `5 × 5` input with stride `1` and padding `0`.

### What does each of the four dimensions mean?

For:

```text
[1, 3, 4, 4]
```

the dimensions mean:

```text
1 → batch size
3 → output channels
4 → feature-map height
4 → feature-map width
```

### What is the relationship between a filter and an output channel?

Each output filter creates one output feature map.

Therefore:

```text
1 filter
→ 1 output channel

3 filters
→ 3 output channels

64 filters
→ 64 output channels
```

In PyTorch:

```python
out_channels
```

specifies how many filters the convolutional layer contains.

### Why are feature maps 1 and 2 exact opposites?

The filters are:

```text
filter 1:

[-1  1]
[-1  1]
```

and:

```text
filter 2:

[ 1 -1]
[ 1 -1]
```

Therefore:

```text
filter_2 = -filter_1
```

Because convolution is based on weighted sums, multiplying every filter weight by `-1` also multiplies every output value by `-1`.

Therefore:

```text
feature_map_2
=
-feature_map_1
```

### Why can later layers benefit from several different feature maps?

Each feature map can represent a different pattern found in the input.

Instead of receiving only the original pixel values, a later layer can receive information such as:

```text
channel 1 → one edge orientation
channel 2 → opposite orientation
channel 3 → horizontal edge
...
```

The next convolutional layer can combine information from these different channels.

This allows deeper CNN layers to construct increasingly complex visual representations.

### Are these three filters learned?

No.

The filters are manually assigned using:

```python
with torch.no_grad():
    conv.weight[0, 0] = filter_1
    conv.weight[1, 0] = filter_2
    conv.weight[2, 0] = filter_3
```

There is no:

```text
loss
backpropagation
optimizer
```

in this experiment.

Therefore, the convolution weights remain fixed.

A later CNN experiment will allow convolution filters to become trainable parameters.