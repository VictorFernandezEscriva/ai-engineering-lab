# Experiment 27 — Backpropagation and Gradients

## Objective

What happens when `loss.backward()` is called on a language-model loss?

The previous experiment introduced a scalar CrossEntropyLoss.

This experiment follows that error backward through the complete language model and inspects the resulting gradients.

The key distinction is:

```text
backward()
→ calculates gradients

optimizer.step()
→ changes parameters
```

This experiment performs only the first operation.

---

## Roadmap Position

```text
CrossEntropyLoss ✅
↓
Backpropagation + Gradients ✅
↓
Optimizer Update ← NEXT
↓
Training Loop
```

---

## Training Example

The training text is:

```text
hell
```

The causal language-model training pair is:

```text
input:
hel

target:
ell
```

The token IDs are:

```text
input:
[5, 4, 7]

target:
[4, 7, 7]
```

Therefore the model learns the relationships:

```text
"h"   → "e"
"he"  → "l"
"hel" → "l"
```

---

## Complete Tiny Language Model

Unlike the previous loss experiment, this experiment rebuilds the complete differentiable model:

```text
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
LM Head
↓
vocabulary logits
↓
CrossEntropyLoss
```

The loss was:

```text
2.7490451335906982
```

The small difference from the previous experiment comes from using the model's full-precision logits instead of previously printed logits rounded to four decimal places.

---

## Computational Graph

PyTorch records the operations used during the forward pass.

Conceptually:

```text
parameters
↓
embeddings
↓
Transformer calculations
↓
LM Head
↓
logits
↓
CrossEntropyLoss
↓
loss
```

Calling:

```python
loss.backward()
```

traverses this graph in reverse:

```text
loss
↓
LM Head
↓
Transformer Block 3
↓
Transformer Block 2
↓
Transformer Block 1
↓
embeddings
```

and calculates how the loss changes with respect to trainable parameters.

---

## Gradients Before Backward

Before:

```python
loss.backward()
```

the inspected parameter gradients were:

```text
Token embedding gradient: None
Block 1 query gradient: None
Block 3 FFN gradient: None
LM head gradient: None
```

No backward pass had been performed yet.

---

## Gradients After Backward

After:

```python
loss.backward()
```

the experiment verified:

```text
Token embedding gradient exists: True
Block 1 query gradient exists: True
Block 3 FFN gradient exists: True
LM head gradient exists: True
```

This demonstrates that the final language-model loss propagated through the complete network.

---

## Gradient Norms

The verified gradient norms were:

```text
Token embedding:
0.2918507754802704

Block 1 query projection:
0.05330401659011841

Block 3 FFN output projection:
0.39916500449180603

LM head:
1.6929279565811157
```

A non-zero gradient means that changing the parameter can affect the current loss.

Gradient norms from different tensors should not be interpreted as directly comparable measures of importance because the tensors have different sizes and roles.

---

## Gradient With Respect to Logits

The gradient of the loss with respect to the vocabulary logits was:

```text
tensor([
    [ 0.0155,  0.0311,  0.0377,  0.0259, -0.3049,
      0.0337,  0.0662,  0.0347,  0.0449,  0.0152],

    [ 0.0716,  0.0579,  0.0222,  0.0714,  0.0114,
      0.0224,  0.0141, -0.3190,  0.0359,  0.0122],

    [ 0.0289,  0.0359,  0.0240,  0.0663,  0.0181,
      0.0328,  0.0576, -0.3094,  0.0315,  0.0142]
])
```

with shape:

```text
[3, 10]
```

There is one gradient value for every vocabulary logit at every training position.

---

## CrossEntropy Gradient

For CrossEntropyLoss with mean reduction, the gradient with respect to each logit is:

```text
(probability - target_one_hot)
/
number_of_positions
```

The experiment independently calculated this expression and compared it with PyTorch autograd.

The result was:

```text
LOGIT GRADIENT MATCH:
True
```

---

## Correct-Token Gradient

Consider:

```text
"h" → "e"
```

The correct target ID is:

```text
4
```

The gradient for that logit was:

```text
-0.3049
```

while the incorrect vocabulary logits had positive gradients.

This pattern also appeared for:

```text
"he" → "l"
```

where the `"l"` gradient was:

```text
-0.3190
```

and:

```text
"hel" → "l"
```

where the `"l"` gradient was:

```text
-0.3094
```

---

## Why the Sign Matters

Gradient descent will later perform updates conceptually similar to:

```text
new_parameter
=
old_parameter
-
learning_rate × gradient
```

Therefore a negative gradient associated with the correct-token score creates pressure for the model to increase that score.

Positive gradients for competing scores create pressure in the opposite direction.

The actual parameter updates happen indirectly through the complete computational graph rather than by directly editing the logits.

---

## LM Head Gradient

The experiment inspected the gradient associated with vocabulary token:

```text
'l'
```

The LM-head gradient vector was:

```text
[ 0.8160,
  0.6207,
 -0.2736,
 -0.4961,
  0.2190,
 -0.0852,
 -0.4697,
 -0.3310]
```

This vector tells us how the loss changes with respect to the eight LM-head weights associated with token `"l"`.

The vector contains contributions from the training positions that influence the shared LM-head parameters.

---

## Backward Does Not Update Parameters

An essential distinction was explicitly verified.

After:

```python
loss.backward()
```

the experiment compared parameters against copies created before backpropagation.

Results:

```text
TOKEN EMBEDDING WEIGHTS UNCHANGED AFTER BACKWARD:
True
```

```text
BLOCK 1 QUERY WEIGHTS UNCHANGED AFTER BACKWARD:
True
```

```text
LM HEAD WEIGHTS UNCHANGED AFTER BACKWARD:
True
```

Therefore:

```text
backward()
→ computes gradients
```

but:

```text
backward()
≠ parameter update
```

---

## Gradients vs Parameters

After backpropagation, each trainable parameter conceptually has:

```text
parameter.data
```

and:

```text
parameter.grad
```

For example:

```text
W
→ current parameter values

W.grad
→ direction of loss change
```

The optimizer will use both in the next experiment.

---

## Hypothesis

Calling `loss.backward()` should:

1. produce gradients for the LM Head,
2. propagate gradients through all Transformer blocks,
3. produce gradients for early model parameters such as embeddings,
4. produce the expected CrossEntropy gradient with respect to logits,
5. leave all parameter values unchanged.

---

## Verified Results

Before backward:

```text
parameter.grad = None
```

After backward:

```text
parameter.grad exists
```

Verified:

```text
LOGIT GRADIENT MATCH:
True
```

and:

```text
TOKEN EMBEDDING WEIGHTS UNCHANGED AFTER BACKWARD:
True

BLOCK 1 QUERY WEIGHTS UNCHANGED AFTER BACKWARD:
True

LM HEAD WEIGHTS UNCHANGED AFTER BACKWARD:
True
```

---

## Interpretation

The model now knows not only:

```text
how wrong was the prediction?
```

through the loss, but also:

```text
which parameter changes would affect that error?
```

through gradients.

This does not yet constitute a complete learning step.

The gradients have been calculated, but the parameters still contain their original values.

---

## Training Step So Far

The learning pipeline currently reaches:

```text
forward pass
↓
logits
↓
CrossEntropyLoss
↓
loss
↓
backward()
↓
gradients
```

The missing operation is:

```text
optimizer.step()
```

which will use those gradients to modify the parameters.

---

## Conclusion

Backpropagation successfully propagated the next-token prediction error through:

```text
LM Head
Transformer blocks
embeddings
```

The experiment demonstrated that:

```text
loss.backward()
```

calculates gradients but does not modify weights.

The next experiment will perform the first actual parameter update.

---

## Limitations

This experiment still does not include:

- optimizer updates,
- gradient clearing with `zero_grad()`,
- repeated training steps,
- decreasing loss over time,
- learned language behavior,
- generation.

Only one forward and backward pass was performed.

---

## Check Yourself

### What does `loss.backward()` do?

It computes gradients of the loss with respect to trainable parameters.

### Does `loss.backward()` modify model weights?

No.

### Where are parameter gradients stored?

In:

```python
parameter.grad
```

### Can the final loss affect early Transformer layers?

Yes.

The experiment found a non-zero gradient in the Query projection of Transformer Block 1.

### Can it affect token embeddings?

Yes.

The token embedding matrix also received gradients.

### Why is the correct-token logit gradient negative?

Because CrossEntropyLoss creates pressure for gradient descent to increase the correct-token score.

### What happens to incorrect logits?

Their gradients are positive in this example, creating pressure in the opposite direction.

### What comes next?

The optimizer will use the gradients to modify the model parameters.