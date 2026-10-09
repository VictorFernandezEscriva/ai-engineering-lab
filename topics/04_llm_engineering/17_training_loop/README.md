# Experiment 29 — Language-Model Training Loop

## Objective

How do the individual pieces studied in previous experiments combine into an actual language-model training process?

Previous experiments isolated:

```text
forward pass
CrossEntropyLoss
backpropagation
gradients
optimizer updates
```

This experiment combines them into a repeated training loop.

The goal is to observe a randomly initialized tiny Transformer gradually adapt its parameters to predict the next tokens in a training sequence.

---

## Roadmap Position

```text
CrossEntropyLoss ✅
↓
Backpropagation ✅
↓
Optimizer Update ✅
↓
Training Loop ✅
↓
Autoregressive Generation + Sampling ← NEXT
```

---

## Training Sequence

The training text is:

```text
hello
```

For causal language-model training:

```text
input:
hell

target:
ello
```

Token IDs:

```text
input:
[5, 4, 7, 7]

target:
[4, 7, 7, 9]
```

This creates four next-token training relationships:

```text
"h"    → "e"
"he"   → "l"
"hel"  → "l"
"hell" → "o"
```

---

## Model Architecture

The experiment trains the complete tiny language model:

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

Model configuration:

```text
vocabulary size = 10
d_model         = 8
attention heads = 2
FFN hidden size = 32
Transformer layers = 3
```

---

## Training Configuration

The optimizer is:

```text
SGD
```

with:

```text
learning rate = 0.1
```

The model is trained for:

```text
100 optimizer updates
```

---

## Predictions Before Training

Before any parameter updates, the model was randomly initialized.

Its predictions were:

```text
"h"
predicted: "i"
target:    "e"
target probability: 8.52 %

"he"
predicted: "\n"
target:    "l"
target probability: 4.29 %

"hel"
predicted: "d"
target:    "l"
target probability: 7.17 %

"hell"
predicted: "i"
target:    "o"
target probability: 4.98 %
```

The model had not learned the training sequence.

---

## The Training Loop

The core training process is:

```python
for step in range(num_steps):

    logits = model(input_ids)

    loss = criterion(
        logits,
        target_ids
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()
```

Conceptually:

```text
forward pass
↓
predictions
↓
loss
↓
clear previous gradients
↓
backpropagation
↓
new gradients
↓
optimizer update
↓
new parameters
↓
repeat
```

---

## Step Zero

Step zero represents the initial model state before any optimizer update.

Therefore:

```text
Step 0
=
randomly initialized model
```

After one optimizer update:

```text
Step 1
```

represents the first learned parameter state.

This convention makes the training progression easy to interpret.

---

## Verified Training Progression

The observed training progression was:

```text
Step 0
Loss: 2.8116908073425293
Predictions: 'i\ndi'
```

```text
Step 1
Loss: 2.242645025253296
Predictions: 'idii'
```

```text
Step 2
Loss: 1.8296146392822266
Predictions: 'edie'
```

```text
Step 5
Loss: 1.0700139999389648
Predictions: 'ello'
```

```text
Step 10
Loss: 0.42497342824935913
Predictions: 'ello'
```

```text
Step 20
Loss: 0.12855401635169983
Predictions: 'ello'
```

```text
Step 50
Loss: 0.030630551278591156
Predictions: 'ello'
```

```text
Step 100
Loss: 0.011777641251683235
Predictions: 'ello'
```

The loss decreased dramatically across training.

---

## Correct Predictions Before Minimum Loss

An important observation is that all greedy predictions became correct by approximately:

```text
Step 5
```

where:

```text
Predictions: 'ello'
```

but the loss was still:

```text
1.070014
```

This demonstrates that:

```text
correct argmax
```

is not equivalent to:

```text
very low CrossEntropyLoss
```

A token can already have the highest probability while still having relatively low confidence.

Training continued increasing the probability assigned to the correct targets.

---

## Final Loss

After 100 optimizer updates:

```text
FINAL LOSS:
0.011777641251683235
```

Compared with the initial loss:

```text
2.8116908073425293
```

the training objective decreased substantially.

---

## Predictions After Training

The final model predictions were:

```text
"h"
predicted: "e"
target:    "e"
target probability: 0.9813212752342224
```

```text
"he"
predicted: "l"
target:    "l"
target probability: 0.9937538504600525
```

```text
"hel"
predicted: "l"
target:    "l"
target probability: 0.9924771189689636
```

```text
"hell"
predicted: "o"
target:    "o"
target probability: 0.9856656193733215
```

In percentage form:

```text
P("e" | "h")    ≈ 98.13 %
P("l" | "he")   ≈ 99.38 %
P("l" | "hel")  ≈ 99.25 %
P("o" | "hell") ≈ 98.57 %
```

---

## Final Verification

The expected target sequence was:

```text
'ello'
```

The predicted target sequence was:

```text
'ello'
```

The experiment verified:

```text
ALL TRAINING PREDICTIONS CORRECT:
True
```

---

## What Actually Learned?

The training process did not modify only the LM Head.

Because the optimizer received:

```python
model.parameters()
```

the training step could update all trainable parameters:

```text
token embeddings
position embeddings
attention Q projections
attention K projections
attention V projections
attention output projections
LayerNorm parameters
FFN parameters
LM Head parameters
```

The final behavior therefore emerges from the complete trained network.

---

## Training as Repeated Optimization

One optimizer update performs:

```text
current parameters
↓
forward pass
↓
loss
↓
gradients
↓
parameter update
```

A training loop repeats this process:

```text
parameters₀
↓
parameters₁
↓
parameters₂
↓
...
↓
parameters₁₀₀
```

Each new parameter state is influenced by the errors produced by the previous state.

---

## Why `zero_grad()` Is Required

PyTorch accumulates gradients by default.

Therefore every normal training iteration clears old gradients before calculating new ones:

```python
optimizer.zero_grad()
```

Without this operation, gradients from previous iterations would be added to the current gradients.

The complete sequence is:

```text
forward
↓
loss
↓
zero_grad
↓
backward
↓
optimizer.step
```

and then the process repeats.

---

## Training vs Evaluation

During training:

```python
model.train()
```

is used.

For prediction inspection:

```python
model.eval()
```

and:

```python
torch.no_grad()
```

are used.

The current architecture does not contain Dropout, so `train()` and `eval()` do not currently produce different numerical behavior.

However, keeping the distinction explicit matches normal PyTorch model workflows and becomes important when training-dependent layers are present.

---

## Memorization vs Generalization

The model successfully learned the training sequence.

However, the training dataset consists of only:

```text
hello
```

Therefore this experiment demonstrates:

```text
optimization
and
memorization
```

not meaningful language understanding or generalization.

The model has effectively learned relationships such as:

```text
"h"    → "e"
"he"   → "l"
"hel"  → "l"
"hell" → "o"
```

A useful language model requires much larger and more diverse training data.

---

## Hypothesis

Repeated gradient-based optimization should:

1. begin with mostly incorrect random predictions,
2. reduce CrossEntropyLoss over training,
3. change the model's predictions,
4. eventually make the correct token the highest-scoring candidate,
5. continue reducing loss even after greedy predictions become correct,
6. substantially increase correct-target probabilities.

All six behaviors were observed.

---

## Complete Learning Pipeline

The educational model now contains the full fundamental training pipeline:

```text
text
↓
tokenization
↓
token IDs
↓
embeddings
↓
Transformer blocks
↓
LM Head
↓
vocabulary logits
↓
shifted next-token targets
↓
CrossEntropyLoss
↓
backpropagation
↓
gradients
↓
optimizer updates
↓
repeat
↓
trained parameters
```

---

## Interpretation

For the first time in the LLM experiments, the network's behavior changed through repeated learning.

Initially:

```text
'h' → 'i'
```

After training:

```text
'h' → 'e'
```

Initially:

```text
'hel' → 'd'
```

After training:

```text
'hel' → 'l'
```

These changes were not manually programmed.

They emerged because gradient descent changed the model parameters to reduce the next-token prediction loss.

---

## Conclusion

This experiment combines all previously isolated training mechanics into a functioning language-model training loop.

The model started with:

```text
Loss ≈ 2.8117
```

and random predictions.

After 100 SGD updates it reached:

```text
Loss ≈ 0.01178
```

and correctly predicted:

```text
'ello'
```

for the training contexts derived from:

```text
hello
```

The model can now be trained.

The next step is to use a trained model autoregressively:

```text
predict next token
↓
append token
↓
predict again
↓
append again
↓
...
```

and study deterministic and probabilistic token selection.

---

## Limitations

This experiment uses:

```text
one tiny training sequence
one full-sequence training example
SGD
no mini-batches
no validation set
no train/validation split
no learning-rate scheduler
no Dropout
no realistic dataset
```

The model memorizes the training sequence and does not demonstrate general language ability.

Future experiments will expand beyond this deliberately minimal training setup.

---

## Check Yourself

### What is the core training loop?

```text
forward
↓
loss
↓
zero_grad
↓
backward
↓
optimizer.step
↓
repeat
```

### What did Step 0 represent?

The randomly initialized model before any optimizer updates.

### When did the model first produce all correct greedy predictions?

Approximately Step 5.

### Why did training continue after Step 5?

Because correct argmax predictions can still have low confidence and therefore non-trivial CrossEntropyLoss.

### What was the initial loss?

Approximately:

```text
2.8117
```

### What was the final loss?

Approximately:

```text
0.01178
```

### What was the final prediction sequence?

```text
'ello'
```

### Did only the LM Head learn?

No.

All trainable parameters supplied to the optimizer could receive gradients and be updated.

### Has the model learned English?

No.

It has memorized a tiny training sequence.

### What comes next?

Autoregressive generation and token sampling.