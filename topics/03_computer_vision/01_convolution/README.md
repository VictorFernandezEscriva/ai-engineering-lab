# Experiment 05 — Manual Convolution Kernel

## Objective

What does a convolution filter actually compute before we ask a Convolutional Neural Network (CNN) to learn filters automatically?

The previous experiments used fully connected neural-network layers.

This experiment introduces a different type of operation designed specifically to exploit spatial structure in data such as images:

```text
convolution
```

The objective is to understand how a small kernel moves across an image and transforms local groups of pixels into a new representation called a **feature map**.

## Concepts

### Image as a tensor

The experiment starts with a simple `5 × 5` grayscale image:

```text
0 0 0 0 0
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
0 0 0 0 0
```

The values can be interpreted as:

```text
0 → dark pixel
1 → bright pixel
```

The image therefore contains a bright square surrounded by dark pixels.

Its initial shape is:

```text
[5, 5]
```

which represents:

```text
[height, width]
```

### Conv2d input dimensions

PyTorch `Conv2d` expects image data using the shape:

```text
[batch, channels, height, width]
```

Our original image only has:

```text
[height, width]

[5, 5]
```

Therefore, two dimensions are added:

```python
image = image.unsqueeze(0).unsqueeze(0)
```

The final shape becomes:

```text
[1, 1, 5, 5]
```

meaning:

```text
batch    = 1 image
channels = 1 grayscale channel
height   = 5
width    = 5
```

### Batch dimension

The batch dimension represents how many images are processed together.

In this experiment:

```text
batch = 1
```

because only one image is processed.

A larger training batch could have a shape such as:

```text
[32, 1, 5, 5]
```

meaning:

```text
32 images
1 channel each
5 × 5 pixels
```

### Channel dimension

The channel dimension represents different input channels.

A grayscale image usually contains:

```text
1 channel
```

while an RGB image normally contains:

```text
3 channels

Red
Green
Blue
```

For example:

```text
[1, 3, 224, 224]
```

could represent:

```text
1 RGB image
3 channels
224 × 224 pixels
```

### Kernel

The experiment manually defines the following `2 × 2` kernel:

```text
[-1   1]
[-1   1]
```

A kernel is a small matrix of weights that is applied repeatedly to local regions of the image.

Conceptually:

```text
image
  ↓
small local window
  ↓
kernel weights
  ↓
weighted sum
  ↓
one output value
```

The same kernel is reused at every spatial position.

This weight sharing is an important characteristic of convolutional neural networks.

### Local receptive field

At each position, the kernel only sees a small part of the image.

Because the kernel has size:

```text
2 × 2
```

each output value initially depends on only four nearby pixels.

For example:

```text
image window

[0 0]
[0 1]
```

is combined with:

```text
kernel

[-1  1]
[-1  1]
```

Element-wise multiplication gives:

```text
0 × -1
0 ×  1
0 × -1
1 ×  1
```

Adding these values gives:

```text
0 + 0 + 0 + 1 = 1
```

Therefore, that location produces:

```text
1
```

in the feature map.

### Feature map

The kernel is applied repeatedly across the image.

Each local calculation produces one output value.

The collection of those values forms a new grid called a:

```text
feature map
```

Conceptually:

```text
input image
     ↓
sliding kernel
     ↓
local weighted sums
     ↓
feature map
```

The feature map represents where the pattern detected by the kernel appears in the image.

### Uniform regions

Consider a completely bright `2 × 2` region:

```text
[1 1]
[1 1]
```

Applying the kernel:

```text
[-1  1]
[-1  1]
```

produces:

```text
(1 × -1)
+
(1 × 1)
+
(1 × -1)
+
(1 × 1)

= 0
```

Therefore, uniform regions produce:

```text
0
```

for this particular kernel.

### Edge response

Now consider:

```text
[0 1]
[0 1]
```

Applying the kernel gives:

```text
0 + 1 + 0 + 1 = 2
```

The opposite transition:

```text
[1 0]
[1 0]
```

produces:

```text
-1 + 0 -1 + 0 = -2
```

Therefore, the filter responds differently depending on the direction of the intensity transition.

Conceptually:

```text
dark → bright
→ positive response

bright → dark
→ negative response

uniform region
→ approximately zero
```

### Stride

Stride controls how far the kernel moves between positions.

This experiment uses:

```python
stride=1
```

meaning that the kernel moves one pixel at a time.

Conceptually:

```text
position 1
   ↓ move 1 pixel
position 2
   ↓ move 1 pixel
position 3
```

A larger stride would skip positions and usually produce a smaller output.

### Padding

This experiment uses:

```python
padding=0
```

meaning that no extra pixels are added around the image.

Because the kernel must remain completely inside the image, it cannot be centered on pixels at the outer boundary in the same way.

This causes the spatial output dimensions to become smaller.

### Why does the output become `4 × 4`?

The input image has:

```text
5 × 5
```

and the kernel has:

```text
2 × 2
```

With:

```text
stride = 1
padding = 0
```

the kernel has four valid horizontal positions and four valid vertical positions.

Therefore:

```text
5 × 5
  ↓
2 × 2 kernel
  ↓
4 × 4 feature map
```

For this simple configuration:

```text
output size =
input size - kernel size + 1
```

Therefore:

```text
5 - 2 + 1 = 4
```

### PyTorch `Conv2d` and cross-correlation

Strict mathematical convolution normally flips the kernel before applying it.

PyTorch `Conv2d` does not perform that flip.

It computes an operation technically called **cross-correlation**.

Therefore, the kernel:

```text
[-1  1]
[-1  1]
```

is applied exactly in the orientation in which it was supplied.

Deep-learning libraries commonly use this operation while still calling the layer a convolutional layer.

### Manual weights vs learned weights

The convolutional layer is created using:

```python
conv = nn.Conv2d(
    in_channels=1,
    out_channels=1,
    kernel_size=2,
    stride=1,
    padding=0,
    bias=False
)
```

Normally, the values inside:

```text
conv.weight
```

would be trainable parameters.

In this experiment, training is deliberately disabled.

Instead, the kernel is manually inserted:

```python
with torch.no_grad():
    conv.weight[0, 0] = kernel
```

This allows the exact operation to be inspected before introducing learned convolution filters.

In a real CNN:

```text
kernel values
↓
start from initialization
↓
training
↓
backpropagation
↓
optimizer
↓
learned filters
```

## Hypothesis

The manually selected kernel should respond strongly to vertical intensity transitions.

Uniform regions should produce zero because the positive and negative kernel weights cancel each other.

Opposite edge directions should produce outputs with opposite signs.

Because the input is `5 × 5`, the kernel is `2 × 2`, stride is `1` and padding is `0`, the expected feature map shape is:

```text
4 × 4
```

## Implementation

The experiment:

1. Creates a synthetic `5 × 5` grayscale image.
2. Defines a fixed `2 × 2` kernel.
3. Adds batch and channel dimensions.
4. Creates a `Conv2d` layer.
5. Explicitly uses stride `1`.
6. Explicitly uses padding `0`.
7. Disables the convolution bias.
8. Manually replaces the convolution weights with the known kernel.
9. Applies the convolution.
10. Prints the resulting feature map and its dimensions.

No training takes place in this experiment.

The purpose is to inspect the convolution operation directly.

## Run

Run from the repository root:

```bash
python topics/03_computer_vision/01_convolution/main.py
```

## Observed results

A verified run produced the following original image:

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

The manually defined kernel was:

```text
tensor([[-1.,  1.],
        [-1.,  1.]])
```

After adding the batch and channel dimensions, the input shape expected by `Conv2d` became:

```text
torch.Size([1, 1, 5, 5])
```

This represents:

```text
1 image
1 channel
5 pixels high
5 pixels wide
```

The resulting feature map was:

```text
tensor([[[[ 1.,  0.,  0., -1.],
          [ 2.,  0.,  0., -2.],
          [ 2.,  0.,  0., -2.],
          [ 1.,  0.,  0., -1.]]]])
```

The complete output tensor shape was:

```text
torch.Size([1, 1, 4, 4])
```

This represents:

```text
1 batch
1 output channel
4 pixels high
4 pixels wide
```

The spatial feature map is therefore:

```text
[[ 1,  0,  0, -1],
 [ 2,  0,  0, -2],
 [ 2,  0,  0, -2],
 [ 1,  0,  0, -1]]
```

The result matches the hypothesis.

Uniform regions produce zero because the positive and negative kernel contributions cancel.

One direction of the vertical intensity transition produces positive values:

```text
1
2
2
1
```

while the opposite transition produces negative values:

```text
-1
-2
-2
-1
```

This confirms that the manually selected kernel responds to vertical intensity changes and that opposite edge directions produce responses with opposite signs.

## Interpretation

The feature map shows how the fixed kernel responds to different local regions.

The positive values on one side of the square correspond to one edge orientation:

```text
1
2
2
1
```

The opposite side produces:

```text
-1
-2
-2
-1
```

because the intensity transition occurs in the opposite direction.

Inside uniform areas, the kernel produces:

```text
0
```

because the positive and negative contributions cancel.

The important concept is not the specific numbers themselves.

The important mechanism is:

```text
small local region
      ↓
shared kernel
      ↓
element-wise multiplication
      ↓
sum
      ↓
one feature value
```

and repeating that operation spatially creates a feature map.

## Conclusion

This experiment demonstrates the fundamental operation behind convolutional neural networks.

A convolutional filter:

1. examines a local region,
2. combines pixel values with kernel weights,
3. produces one output value,
4. moves to another spatial position,
5. repeats the same computation.

The result is a feature map showing where a particular spatial pattern produces a strong response.

This experiment also introduces three important CNN ideas:

```text
local connectivity
+
weight sharing
+
feature maps
```

The kernel is manually defined here.

Later, CNN training will allow neural networks to learn useful kernels automatically through backpropagation and optimization.

## Limitations

This experiment is intentionally minimal.

It uses:

* one synthetic image,
* one grayscale channel,
* one manually selected kernel,
* one output channel,
* no bias,
* no padding,
* stride `1`,
* no training.

The filter is not learned.

The experiment therefore demonstrates the mechanics of convolution rather than a complete CNN.

Real convolutional neural networks typically use:

* multiple input channels,
* many learned filters,
* several convolutional layers,
* activation functions,
* pooling or other spatial operations,
* larger datasets,
* backpropagation,
* optimizers,
* classification or detection objectives.

## Product connection

### Concept

Images contain spatial patterns that can often be detected using local operations.

### Implementation

A small kernel is applied repeatedly across an image to produce a feature map.

### Product

Computer-vision systems can use learned convolutional filters to detect increasingly useful visual patterns.

Early layers may respond to relatively simple structures such as:

```text
edges
lines
corners
textures
```

Deeper layers can combine earlier representations into more complex visual features.

These representations can eventually support tasks such as:

```text
image classification
object detection
defect detection
medical-image analysis
autonomous perception
```

## Check yourself

### Why does the output become `4 × 4` rather than `5 × 5`?

The input has size:

```text
5 × 5
```

and the kernel has size:

```text
2 × 2
```

With:

```text
stride = 1
padding = 0
```

the kernel has only four valid positions along each dimension.

Therefore:

```text
5 - 2 + 1 = 4
```

and the output becomes:

```text
4 × 4
```

### What do batch and channel dimensions mean?

PyTorch represents image batches using:

```text
[batch, channels, height, width]
```

The batch dimension indicates how many images are processed together.

The channel dimension represents separate image channels.

For this experiment:

```text
[1, 1, 5, 5]
```

means:

```text
1 image
1 grayscale channel
5 pixels high
5 pixels wide
```

An RGB image normally has three channels.

### Why do left and right transitions have opposite signs?

The kernel contains negative weights on its left side and positive weights on its right side:

```text
[-1  1]
[-1  1]
```

A transition from dark pixels on the left to bright pixels on the right therefore produces a positive result.

The opposite transition places bright pixels under the negative weights and dark pixels under the positive weights, producing a negative result.

Therefore, opposite edge directions produce opposite signs.

### What would padding change?

Padding adds additional values around the image boundary.

For example, zero padding surrounds the original image with zeros.

Padding allows the kernel to operate closer to the original borders and can preserve more of the spatial dimensions.

Without padding:

```text
5 × 5
↓ 2 × 2 kernel
4 × 4
```

Appropriate padding can produce a larger output than the unpadded case.

The exact output size depends on:

```text
input size
kernel size
stride
padding
```

### Is this convolution layer being trained?

No.

Although `nn.Conv2d` normally contains trainable weights, this experiment manually replaces those weights with:

```text
[-1  1]
[-1  1]
```

No loss function, backpropagation or optimizer is used.

Therefore, the filter remains fixed.

### What will change when we train a real CNN?

In a trained CNN, the kernel values will become model parameters.

Training will follow the same general mechanism already introduced for fully connected neural networks:

```text
forward pass
    ↓
loss
    ↓
backpropagation
    ↓
kernel gradients
    ↓
optimizer
    ↓
updated kernel values
```

The important difference is that convolutional layers learn spatial filters that are reused across different locations in an image.