# Experiment 23 — Stacked Transformer Blocks

## Objective

What does it mean for a Transformer language model to contain multiple layers?

The previous experiment implemented one reusable `TransformerBlock`.

This experiment stacks several independent Transformer blocks so that token representations are transformed repeatedly through depth.

The main goals are to verify that:

1. each Transformer block owns independent trainable parameters,
2. the output of one block becomes the input of the next,
3. token representations evolve from layer to layer,
4. `[sequence_length, d_model]` is preserved through the entire stack.

---

## Architecture

The experiment uses three Transformer blocks:

```text
token + position embeddings
↓
Transformer Block 1
↓
Transformer Block 2
↓
Transformer Block 3
↓
final contextual representations
```

For this experiment:

```text
sequence_length = 3
d_model = 8
num_heads = 2
head_dimension = 4
ffn_hidden_dimension = 32
num_layers = 3
```

The external tensor shape is therefore:

```text
[3, 8]
```

throughout the stack.

---

## Independent Blocks

Each block is created independently:

```python
TransformerBlock(...)
TransformerBlock(...)
TransformerBlock(...)
```

Therefore each block owns its own parameters.

Conceptually:

```text
Block 1:
Wq₁
Wk₁
Wv₁
Wo₁
FFN₁
LayerNorm₁
...

Block 2:
Wq₂
Wk₂
Wv₂
Wo₂
FFN₂
LayerNorm₂
...

Block 3:
Wq₃
Wk₃
Wv₃
Wo₃
FFN₃
LayerNorm₃
...
```

The blocks do not normally share these parameters.

---

## Parameter Verification

The experiment directly compared the Query projection parameter objects from Block 1 and Block 2.

The result was:

```text
BLOCK 1 AND BLOCK 2 SHARE THE SAME QUERY WEIGHT OBJECT:
False
```

This confirms that they are different `Parameter` objects.

The values were also compared:

```text
BLOCK 1 AND BLOCK 2 QUERY WEIGHTS HAVE IDENTICAL VALUES:
False
```

Therefore the two blocks were independently initialized.

---

## TransformerStack

The blocks are registered using:

```python
nn.ModuleList
```

Conceptually:

```python
self.blocks = nn.ModuleList(
    [
        TransformerBlock(...),
        TransformerBlock(...),
        TransformerBlock(...),
    ]
)
```

`nn.ModuleList` allows PyTorch to register all submodules and their parameters as part of the complete model.

This becomes important when optimizers later receive:

```python
model.parameters()
```

because the parameters from every Transformer block must be discoverable.

---

## Sequential Processing

The stack forward pass is:

```python
for block in self.blocks:
    x = block(x)
```

This means:

```text
x0
↓ Block 1
x1
↓ Block 2
x2
↓ Block 3
x3
```

Block 2 does not receive the original embedding representation.

It receives the output of Block 1.

Block 3 receives the output of Block 2.

---

## Initial Stack Input

The stack began with:

```text
tensor([
    [-1.5467,  0.6569, -2.2205, -1.1865,
     -0.7380,  2.6474, -0.0935, -0.4363],

    [-0.6407, -1.3528, -1.2728,  2.3213,
     -1.4034, -1.2523,  1.6404, -0.2911],

    [-3.9128,  0.5240,  0.7211,  0.7043,
      0.5429,  2.4278, -0.1176,  0.9334]
])
```

with shape:

```text
[3, 8]
```

---

## Output After Block 1

The first block produced:

```text
tensor([
    [-1.2723,  0.6544, -0.8338, -0.5770,
     -0.1231,  2.1768,  0.2798, -0.3049],

    [-0.5057, -1.3353, -0.1308,  1.4769,
     -0.4240, -0.7330,  1.7428, -0.0908],

    [-2.2827,  0.0940,  0.7709,  0.2790,
     -0.2535,  1.3803, -0.2572,  0.2692]
])
```

with shape:

```text
[3, 8]
```

---

## Output After Block 2

The second block received the Block 1 output and produced:

```text
tensor([
    [-1.1564,  0.5727, -0.5083, -0.6945,
     -0.2537,  2.3293,  0.0317, -0.3208],

    [-0.2411, -1.7102,  0.0202,  1.2665,
     -0.4052, -0.7875,  1.6007,  0.2567],

    [-2.2442, -0.2742,  0.6721,  0.0432,
     -0.2156,  1.3184, -0.0996,  0.8000]
])
```

with shape:

```text
[3, 8]
```

---

## Output After Block 3

The third block produced:

```text
tensor([
    [-1.3041,  0.7977, -0.3282, -0.6011,
     -0.1883,  2.1906,  0.0324, -0.5990],

    [-0.4163, -1.6652,  0.0709,  1.3738,
     -0.5926, -0.6755,  1.4719,  0.4330],

    [-2.3539, -0.1997,  0.7744,  0.1195,
     -0.1179,  1.2173,  0.0040,  0.5562]
])
```

with shape:

```text
[3, 8]
```

---

## Tracking Token `e`

The experiment tracked token `"e"` through the stack.

### Before Transformer Blocks

```text
[-0.6407, -1.3528, -1.2728,  2.3213,
 -1.4034, -1.2523,  1.6404, -0.2911]
```

### After Block 1

```text
[-0.5057, -1.3353, -0.1308,  1.4769,
 -0.4240, -0.7330,  1.7428, -0.0908]
```

### After Block 2

```text
[-0.2411, -1.7102,  0.0202,  1.2665,
 -0.4052, -0.7875,  1.6007,  0.2567]
```

### After Block 3

```text
[-0.4163, -1.6652,  0.0709,  1.3738,
 -0.5926, -0.6755,  1.4719,  0.4330]
```

The token position is the same throughout the stack.

Its internal representation changes after every block.

---

## Representation Evolution

The experiment verified:

```text
BLOCK 1 OUTPUT DIFFERENT FROM INPUT:
True
```

```text
BLOCK 2 OUTPUT DIFFERENT FROM BLOCK 1:
True
```

```text
BLOCK 3 OUTPUT DIFFERENT FROM BLOCK 2:
True
```

Therefore each Transformer block transforms the representation produced by the previous layer.

A useful mental model is:

```text
representation 0
↓
learned transformation
↓
representation 1
↓
learned transformation
↓
representation 2
↓
learned transformation
↓
representation 3
```

---

## Shape Preservation

Every block preserves:

```text
[sequence_length, d_model]
```

The experiment verified:

```text
ALL LAYERS PRESERVE [sequence_length, d_model]:
True
```

The progression was:

```text
[3, 8]
↓
Block 1
[3, 8]
↓
Block 2
[3, 8]
↓
Block 3
[3, 8]
```

This shape compatibility makes Transformer depth possible.

---

## Causality Across Depth

Every Transformer block contains its own causal attention operation.

For:

```text
h e l
```

each layer maintains the same causal restriction:

```text
h → may attend to h

e → may attend to h, e

l → may attend to h, e, l
```

Adding more layers does not remove the causal constraint.

The mask is applied again inside every block.

---

## Training Across Multiple Blocks

Each block has its own parameters.

During training, the final loss backpropagates through the entire stack:

```text
loss
↓
Block 3
↓
Block 2
↓
Block 1
↓
embeddings
```

Gradients are therefore calculated for parameters throughout the complete model.

However:

```text
Block 1 parameters
≠
Block 2 parameters
≠
Block 3 parameters
```

so each layer can learn different transformations.

---

## Depth

Adding Transformer blocks increases model depth.

With one block:

```text
embeddings
↓
Block 1
↓
representation
```

With multiple blocks:

```text
embeddings
↓
Block 1
↓
representation 1
↓
Block 2
↓
representation 2
↓
Block 3
↓
representation 3
```

Each layer receives contextual representations produced by the previous one.

It is not correct to assign simple fixed meanings such as:

```text
Layer 1 = syntax
Layer 2 = semantics
Layer 3 = reasoning
```

The learned behavior of individual layers is more complex.

---

## Hypothesis

Stacking independent Transformer blocks should:

1. preserve `[sequence_length, d_model]`,
2. produce different representations after each block,
3. use different parameters in different layers,
4. preserve causal attention at every depth,
5. allow the final representation to be passed directly to later language-model components.

---

## Implementation

The experiment:

1. defines a reusable `TransformerBlock`,
2. defines a `TransformerStack`,
3. registers multiple blocks using `nn.ModuleList`,
4. verifies that different blocks own different Query projection parameters,
5. passes the sequence through three blocks sequentially,
6. stores every intermediate layer output,
7. tracks token `"e"` through the stack,
8. verifies that representations change,
9. verifies that all layers preserve `[sequence_length, d_model]`.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/11_stacked_transformer_blocks/main.py
```

---

## Final Stack Output

The final output was:

```text
tensor([
    [-1.3041,  0.7977, -0.3282, -0.6011,
     -0.1883,  2.1906,  0.0324, -0.5990],

    [-0.4163, -1.6652,  0.0709,  1.3738,
     -0.5926, -0.6755,  1.4719,  0.4330],

    [-2.3539, -0.1997,  0.7744,  0.1195,
     -0.1179,  1.2173,  0.0040,  0.5562]
])
```

with shape:

```text
[3, 8]
```

---

## Interpretation

The model no longer performs only one contextual transformation.

The representation is repeatedly refined through multiple independently parameterized Transformer blocks.

Conceptually:

```text
token identity + position
↓
contextual representation
↓
deeper contextual representation
↓
deeper contextual representation
```

Because the model has not been trained, these numerical transformations do not yet represent meaningful learned language structure.

The experiment demonstrates architectural depth rather than linguistic understanding.

---

## Conclusion

The Transformer architecture now contains depth.

The model pipeline has progressed to:

```text
text
↓
token IDs
↓
token embeddings
+
position embeddings
↓
Transformer Block 1
↓
Transformer Block 2
↓
Transformer Block 3
↓
final contextual representations
```

Each layer owns independent parameters.

Each layer receives the previous layer's output.

The external representation shape remains constant:

```text
[sequence_length, d_model]
```

The next step is to convert these final `d_model` representations into vocabulary scores.

---

## Limitations

The model still does not include:

- language-model head,
- vocabulary logits,
- next-token probabilities,
- next-token targets,
- cross-entropy loss,
- training loop,
- optimizer updates,
- text generation,
- batching,
- dropout.

All weights remain randomly initialized.

---

## Product Connection

Real decoder-only language models stack many Transformer blocks.

Model depth allows representations to undergo repeated attention and nonlinear transformation before a next-token prediction is produced.

The number of layers is therefore one of the major architectural dimensions of a Transformer language model.

The next component will connect the final internal representations to the vocabulary itself.

---

## Check Yourself

### Does Block 2 receive the original embeddings?

No.

It receives the output of Block 1.

### Does Block 3 receive the output of Block 1?

Not directly.

It receives the output produced by Block 2.

### Do all blocks normally share their parameters?

No.

Each block normally owns independent parameters.

### Why use `nn.ModuleList`?

So PyTorch registers every Transformer block and its parameters as part of the model.

### Does stacking blocks change `d_model`?

No.

The external shape remains:

```text
[sequence_length, d_model]
```

### Does the causal mask disappear after the first layer?

No.

Every Transformer block performs causal attention.

### What does increasing the number of blocks increase?

Model depth.

### What changes as token `e` passes through the layers?

Its internal vector representation.

### What comes next?

The language-model head.

It will map each final `d_model` representation to one score for every token in the vocabulary.