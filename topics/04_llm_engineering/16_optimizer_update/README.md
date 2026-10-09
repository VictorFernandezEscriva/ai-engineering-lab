# Experiment 28 — Optimizer Update

## Objective

How are the gradients produced by backpropagation actually used to change a language model's parameters?

The previous experiment established that:

```text
loss.backward()
```

calculates gradients but does not modify model weights.

This experiment introduces:

```text
optimizer.step()
```

and verifies an actual parameter update numerically.

---

## Roadmap Position

```text
Backpropagation + Gradients ✅
↓
Optimizer Update ✅
↓
Training Loop ← NEXT
```

---

## Training Example

The training example is:

```text
'hel' → 'ell'
```

This represents the causal next-token relationships:

```text
"h"   → "e"
"he"  → "l"
"hel" → "l"
```

---

## Optimizer

The experiment uses stochastic gradient descent:

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.1,
)
```

The learning rate is:

```text
0.1
```

The basic SGD update rule is:

```text
new_parameter
=
old_parameter
-
learning_rate × gradient
```

---

## Learning Rate

The gradient provides a direction of change.

The learning rate controls the size of the update.

Conceptually:

```text
gradient
→ direction and local sensitivity

learning rate
→ step size
```

A larger learning rate produces larger parameter updates for the same gradient.

---

## Loss Before the Update

Before changing any parameters, the model produced:

```text
LOSS BEFORE UPDATE:
2.7490451335906982
```

---

## Inspected Parameter

The experiment follows one exact scalar parameter in the LM Head.

The inspected vocabulary token is:

```text
'l'
```

with token ID:

```text
7
```

The selected LM-head parameter is:

```text
row = 7
column = 0
```

Its initial value was:

```text
0.04597398638725281
```

---

## Clearing Gradients

Before the backward pass, the experiment calls:

```python
optimizer.zero_grad()
```

The inspected gradient was:

```text
GRADIENT AFTER ZERO_GRAD:
None
```

PyTorch accumulates gradients across backward passes unless they are cleared.

This means gradient clearing is an essential part of a normal training loop.

---

## Backpropagation

The experiment then calls:

```python
loss_before.backward()
```

The gradient of the inspected parameter became:

```text
0.8159642815589905
```

However, the parameter itself had still not changed.

The experiment verified:

```text
WEIGHT UNCHANGED AFTER BACKWARD:
True
```

Therefore:

```text
backward()
→ calculates gradients
```

but does not update weights.

---

## Manual SGD Calculation

The inspected values were:

```text
old weight:
0.04597398638725281

gradient:
0.8159642815589905

learning rate:
0.1
```

The expected SGD update is:

```text
new_weight
=
0.04597398638725281
-
0.1 × 0.8159642815589905
```

which gives approximately:

```text
-0.03562244027853012
```

The experiment printed:

```text
EXPECTED WEIGHT AFTER SGD STEP:
-0.03562244027853012
```

---

## Optimizer Step

The actual update is performed with:

```python
optimizer.step()
```

After the step, the inspected parameter became:

```text
-0.03562244400382042
```

The experiment verified:

```text
WEIGHT CHANGED:
True
```

and:

```text
MANUAL SGD UPDATE MATCH:
True
```

The tiny numerical difference between the manually calculated and stored values is due to floating-point precision.

---

## What Changed?

The optimizer was created using:

```python
model.parameters()
```

Therefore it does not update only the inspected LM-head value.

It has access to all trainable model parameters, including:

```text
token embeddings
position embeddings
attention projections
output projections
LayerNorm parameters
FFN parameters
LM Head parameters
```

Any parameter with a gradient can be updated by the optimizer.

---

## Transformer Parameter Update

The experiment also inspected the gradient magnitude of the Query projection in Transformer Block 1.

The expected SGD update norm was:

```text
0.005330401938408613
```

This is consistent with:

```text
learning_rate × gradient_norm
```

and demonstrates that optimization is not limited to the final LM Head.

Earlier Transformer layers also participate in learning.

---

## Gradients After Optimizer Step

After:

```python
optimizer.step()
```

the gradient still existed:

```text
GRADIENT STILL EXISTS AFTER OPTIMIZER STEP:
True
```

Therefore:

```text
optimizer.step()
```

updates parameters but does not automatically clear their gradients.

This distinction is important:

```text
optimizer.zero_grad()
→ clears old gradients

loss.backward()
→ calculates new gradients

optimizer.step()
→ updates parameters
```

---

## Second Forward Pass

After the parameter update, the same training example was evaluated again.

The new loss was:

```text
LOSS AFTER ONE UPDATE:
2.091325521469116
```

The experiment verified:

```text
LOSS DECREASED:
True
```

The loss changed from:

```text
2.7490451335906982
```

to:

```text
2.091325521469116
```

after one optimization step.

---

## Important Interpretation

A lower loss on this same example does not mean the model has learned language or generalizes to unseen text.

It only demonstrates that the gradient-based update moved the current model parameters in a direction that reduced the training objective for this example.

Repeated optimization over training data is required for actual training.

---

## The Complete Learning Step

The core pieces are now:

```text
input
↓
forward pass
↓
logits
↓
CrossEntropyLoss
↓
loss
↓
zero_grad()
↓
backward()
↓
gradients
↓
optimizer.step()
↓
updated parameters
```

All fundamental operations required for gradient-based neural-network training have now been introduced individually.

---

## Hypothesis

The optimizer step should:

1. use gradients produced by backpropagation,
2. leave weights unchanged before `optimizer.step()`,
3. change trainable parameters after `optimizer.step()`,
4. match the manual SGD update equation,
5. preserve gradients until they are explicitly cleared,
6. produce different model outputs after the update,
7. reduce the loss for the current training example.

---

## Verified Results

```text
LOSS BEFORE UPDATE:
2.7490451335906982
```

```text
WEIGHT BEFORE:
0.04597398638725281
```

```text
GRADIENT:
0.8159642815589905
```

```text
WEIGHT UNCHANGED AFTER BACKWARD:
True
```

Expected update:

```text
-0.03562244027853012
```

Actual update:

```text
-0.03562244400382042
```

Verified:

```text
WEIGHT CHANGED:
True

MANUAL SGD UPDATE MATCH:
True
```

The gradient remained available:

```text
GRADIENT STILL EXISTS AFTER OPTIMIZER STEP:
True
```

The loss after the update was:

```text
2.091325521469116
```

and:

```text
LOSS DECREASED:
True
```

---

## Interpretation

The previous experiment answered:

```text
Which direction would reduce the loss?
```

This experiment answers:

```text
How do we actually move the parameters in that direction?
```

The optimizer converts gradient information into parameter updates.

This is the point where the model's stored trainable state actually changes.

---

## Conclusion

The complete distinction is now explicit:

```text
forward()
→ predictions

CrossEntropyLoss
→ error

backward()
→ gradients

optimizer.step()
→ parameter updates
```

A manually calculated SGD update exactly matched PyTorch's optimizer update.

The next experiment will repeat these operations inside a training loop so that the model can learn over many optimization steps.

---

## Limitations

This experiment performs only one optimization step.

It does not yet include:

- repeated training iterations,
- loss curves,
- training convergence,
- multiple training sequences,
- validation data,
- generalization,
- Adam or AdamW,
- learning-rate schedules,
- text generation.

---

## Check Yourself

### What does `loss.backward()` do?

It calculates gradients.

### Does `loss.backward()` change weights?

No.

### What does `optimizer.step()` do?

It updates parameters using their gradients.

### What is the basic SGD equation?

```text
new_parameter
=
old_parameter
-
learning_rate × gradient
```

### What does the learning rate control?

The size of the parameter update.

### Does `optimizer.step()` clear gradients?

No.

### Why is `optimizer.zero_grad()` needed?

Because PyTorch accumulates gradients by default.

### Did the inspected weight change?

Yes.

It changed from approximately:

```text
0.04597
```

to:

```text
-0.03562
```

### Did the manual SGD calculation match PyTorch?

Yes.

```text
MANUAL SGD UPDATE MATCH:
True
```

### Did the loss decrease?

Yes.

```text
2.7490
→
2.0913
```

### Does one lower training loss prove that the model understands language?

No.

It only verifies that one optimization step reduced the objective for the current example.

### What comes next?

A complete repeated training loop.