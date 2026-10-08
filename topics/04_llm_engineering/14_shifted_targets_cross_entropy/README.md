# Experiment 26 — Shifted Targets and CrossEntropyLoss

## Objective

How does a causal language model know what the correct next token should have been, and how can we measure how wrong its predictions are?

Previous experiments produced vocabulary logits and probabilities.

This experiment introduces:

```text
shifted next-token targets
```

and:

```text
CrossEntropyLoss
```

The model can now compare its predictions against the correct next tokens and produce a scalar error value.

---

## Training Text

The training text is:

```text
hell
```

For causal next-token prediction, the sequence is split into:

```text
input:
hel

target:
ell
```

The target is the original sequence shifted one token to the left.

---

## Shifted Targets

The alignment is:

```text
training text:

h e l l
```

Input:

```text
h e l
```

Target:

```text
  e l l
```

Therefore:

```text
h → e
e → l
l → l
```

Because causal attention makes every position represent all available previous context, a more precise interpretation is:

```text
"h"   → "e"
"he"  → "l"
"hel" → "l"
```

These are three next-token training examples extracted from one sequence.

---

## Target IDs

The vocabulary is:

```text
0 → '\n'
1 → ' '
2 → 'a'
3 → 'd'
4 → 'e'
5 → 'h'
6 → 'i'
7 → 'l'
8 → 'm'
9 → 'o'
```

Therefore:

```text
target tokens:
['e', 'l', 'l']
```

become:

```text
target IDs:
[4, 7, 7]
```

The target tensor has shape:

```text
[3]
```

PyTorch does not require one-hot encoded target vectors.

It only needs the index of the correct vocabulary token for each position.

---

## Model Logits

The previously verified model logits were:

```text
tensor([
    [-0.7904, -0.0962,  0.0973, -0.2796, -0.1874,
     -0.0152,  0.6590,  0.0118,  0.2709, -0.8143],

    [ 1.0319,  0.8185, -0.1385,  1.0284, -0.8016,
     -0.1323, -0.5960, -0.5799,  0.3414, -0.7369],

    [-0.1707,  0.0467, -0.3556,  0.6598, -0.6396,
     -0.0453,  0.5186, -0.3606, -0.0852, -0.8803]
])
```

with shape:

```text
[3, 10]
```

This means:

```text
3 prediction positions
×
10 vocabulary candidates
```

---

## Logits and Targets

CrossEntropyLoss receives:

```text
logits:
[3, 10]
```

and:

```text
targets:
[3]
```

The target IDs are:

```text
[4, 7, 7]
```

Therefore PyTorch interprets the problem as:

```text
logits row 0 → correct vocabulary index = 4
logits row 1 → correct vocabulary index = 7
logits row 2 → correct vocabulary index = 7
```

---

## CrossEntropyLoss

The experiment uses:

```python
nn.CrossEntropyLoss()
```

Importantly, CrossEntropyLoss receives the raw logits directly.

Do not manually apply Softmax before passing the values to `CrossEntropyLoss`.

Conceptually, CrossEntropyLoss performs the equivalent of:

```text
logits
↓
log-probabilities
↓
select correct target
↓
negative log-likelihood
```

using a numerically stable implementation.

---

## Probability of the Correct Token

For educational inspection, Softmax was calculated separately.

The correct-token probabilities were:

```text
"h"   → "e" → 0.085185
"he"  → "l" → 0.042869
"hel" → "l" → 0.071740
```

or approximately:

```text
"h"   → "e" → 8.52 %
"he"  → "l" → 4.29 %
"hel" → "l" → 7.17 %
```

The randomly initialized model therefore assigns relatively low probabilities to the correct targets.

---

## Negative Log-Likelihood

For one correct-token probability:

```text
p
```

the corresponding loss is:

```text
-loss
=
-log(p)
```

More precisely:

```text
loss = -log(correct_token_probability)
```

This means:

```text
high correct-token probability
→ small loss

low correct-token probability
→ large loss
```

---

## Loss Per Position

The verified losses were:

```text
tensor([
    2.4629,
    3.1496,
    2.6347
])
```

Specifically:

```text
"h"   → "e"
loss = 2.462929
```

```text
"he"  → "l"
loss = 3.149600
```

```text
"hel" → "l"
loss = 2.634701
```

The second prediction received the largest loss because the model assigned the lowest probability to its correct target.

---

## Manual Verification

For:

```text
"hel" → "l"
```

the correct-token probability was:

```text
0.07174044847488403
```

Therefore:

```text
loss
=
-log(0.07174044847488403)
```

which produced:

```text
2.6347005367279053
```

PyTorch produced:

```text
2.6347007751464844
```

The small difference is floating-point precision.

The experiment verified:

```text
FINAL-POSITION LOSS MATCH:
True
```

---

## All Position Losses

The same manual calculation was applied to every position:

```text
manual_loss_i
=
-log(correct_probability_i)
```

The experiment verified:

```text
MANUAL LOSSES MATCH CROSS-ENTROPY:
True
```

Therefore the relationship between probability and CrossEntropyLoss was reproduced explicitly.

---

## Mean Loss

By default:

```python
nn.CrossEntropyLoss()
```

uses mean reduction.

Therefore:

```text
mean loss
=
(loss_1 + loss_2 + loss_3) / 3
```

The verified mean loss was:

```text
2.7490768432617188
```

The manual mean of the individual losses produced exactly the same result:

```text
2.7490768432617188
```

The experiment verified:

```text
MEAN LOSS MATCH:
True
```

---

## Shape Progression

The training relationship is:

```text
input token IDs
[3]

↓ model

logits
[3, 10]

+

target IDs
[3]

↓ CrossEntropyLoss

scalar loss
[]
```

The complete training objective therefore collapses many vocabulary predictions into one scalar value.

---

## Why One Scalar?

Training requires one objective that tells the optimizer whether the model is improving.

The individual position losses:

```text
loss_1
loss_2
loss_3
```

are reduced to:

```text
mean loss
```

This scalar will later be used with:

```python
loss.backward()
```

to compute gradients throughout the model.

---

## Training vs Generation

During training:

```text
"h"   → predict "e"
"he"  → predict "l"
"hel" → predict "l"
```

All positions contribute to the training loss simultaneously.

During generation, only the final position is required to choose the next token for the complete current context.

This allows training to use sequence data efficiently.

---

## Hypothesis

Shifted next-token training should:

1. create one correct next-token target per input position,
2. represent targets as vocabulary indices,
3. align `[sequence_length, vocabulary_size]` logits with `[sequence_length]` targets,
4. produce one loss per position,
5. assign larger loss when the correct token receives lower probability,
6. reduce the position losses to one scalar mean loss,
7. match manual `-log(correct_probability)` calculations.

---

## Implementation

The experiment:

1. starts from `hell`,
2. creates input text `hel`,
3. creates target text `ell`,
4. maps target tokens to IDs,
5. uses the previously verified vocabulary logits,
6. calculates CrossEntropyLoss per position,
7. calculates the mean loss,
8. converts logits to probabilities for inspection,
9. extracts each correct-token probability,
10. calculates `-log(probability)` manually,
11. verifies the result against PyTorch.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/14_shifted_targets_cross_entropy/main.py
```

---

## Verified Results

```text
INPUT TEXT:
'hel'

TARGET TEXT:
'ell'

TARGET IDS:
[4, 7, 7]
```

Losses:

```text
[2.4629, 3.1496, 2.6347]
```

Mean:

```text
2.7490768432617188
```

Verified:

```text
MEAN LOSS MATCH:
True

MANUAL LOSSES MATCH CROSS-ENTROPY:
True

FINAL-POSITION LOSS MATCH:
True
```

---

## Interpretation

The model now has an objective.

Previously it could only produce:

```text
scores
```

and:

```text
probabilities
```

Now it can compare those predictions against reality.

The progression is:

```text
prediction
+
correct target
↓
loss
```

The loss tells us how incompatible the model's predictions currently are with the training data.

It does not yet change any parameters.

That requires backpropagation and an optimizer.

---

## Conclusion

The educational model now has a complete next-token training objective:

```text
input sequence
↓
model
↓
vocabulary logits
+
shifted targets
↓
CrossEntropyLoss
↓
scalar loss
```

For the current untrained predictions:

```text
mean loss ≈ 2.7491
```

The next step is to propagate this error backward through the entire computational graph and calculate gradients for the trainable parameters.

---

## Limitations

This experiment does not yet include:

- `loss.backward()`,
- gradients,
- optimizer updates,
- repeated training steps,
- decreasing loss,
- learned next-token predictions,
- text generation.

The model parameters have not changed.

---

## Check Yourself

### Why is the target for `"h"` equal to `"e"`?

Because causal language modeling predicts the token immediately to the right.

### Why is the target after `"he"` equal to `"l"`?

Because the next character in the training text is `"l"`.

### What are shifted targets?

The original sequence moved one position relative to the input so every input position is paired with its next token.

### What shape do the logits have?

```text
[3, 10]
```

### What shape do the targets have?

```text
[3]
```

### Why do targets contain IDs instead of probability vectors?

CrossEntropyLoss expects the vocabulary index of the correct class.

### Should Softmax be applied before `nn.CrossEntropyLoss`?

No.

CrossEntropyLoss expects raw logits.

### What does a low probability for the correct token produce?

A larger loss.

### What was the verified mean loss?

Approximately:

```text
2.7491
```

### Does calculating loss change the model parameters?

No.

### What comes next?

Backpropagation and gradients.