# Experiment 25 — Softmax and Next-Token Probabilities

## Objective

How are raw vocabulary logits converted into an interpretable probability distribution?

The previous experiment produced next-token logits for the full context:

```text
hel
```

The verified logits were:

```text
[-0.1707,
  0.0467,
 -0.3556,
  0.6598,
 -0.6396,
 -0.0453,
  0.5186,
 -0.3606,
 -0.0852,
 -0.8803]
```

These values are scores, not probabilities.

This experiment applies Softmax to convert them into:

```text
next-token probabilities
```

that are:

```text
positive
```

and sum to:

```text
1
```

---

## Vocabulary

The vocabulary is:

```text
['\n', ' ', 'a', 'd', 'e', 'h', 'i', 'l', 'm', 'o']
```

with:

```text
vocabulary_size = 10
```

Therefore both the next-token logits and probabilities have shape:

```text
[10]
```

---

## Starting Logits

The verified next-token logits were:

```text
tensor([
    -0.1707,
     0.0467,
    -0.3556,
     0.6598,
    -0.6396,
    -0.0453,
     0.5186,
    -0.3606,
    -0.0852,
    -0.8803
])
```

Shape:

```text
[10]
```

The highest logit was:

```text
'd' → 0.6598
```

---

## Softmax

Softmax converts a collection of arbitrary logits into a probability distribution.

Conceptually:

```text
logits
↓
exponential
↓
normalize by total
↓
probabilities
```

For every vocabulary token:

```text
probability_i
=
exp(logit_i)
/
sum(exp(all logits))
```

The probabilities are therefore relative to all competing vocabulary tokens.

---

## Numerically Stable Softmax

Directly calculating:

```text
exp(logit)
```

can become numerically problematic when logits are very large.

A stable implementation first subtracts the largest logit:

```text
shifted_logits
=
logits - max(logits)
```

Then:

```text
exp(shifted_logits)
```

is calculated.

Finally:

```text
probabilities
=
exp(shifted_logits)
/
sum(exp(shifted_logits))
```

Subtracting the same constant from every logit does not change the final Softmax probabilities.

---

## Maximum Logit

The maximum verified logit was:

```text
0.6597999930381775
```

corresponding to:

```text
'd'
```

After subtracting the maximum, the logits became:

```text
tensor([
    -0.8305,
    -0.6131,
    -1.0154,
     0.0000,
    -1.2994,
    -0.7051,
    -0.1412,
    -1.0204,
    -0.7450,
    -1.5401
])
```

The maximum shifted logit is therefore:

```text
0
```

---

## Exponentials

The shifted logits produced:

```text
tensor([
    0.4358,
    0.5417,
    0.3623,
    1.0000,
    0.2727,
    0.4941,
    0.8683,
    0.3605,
    0.4747,
    0.2144
])
```

The largest logit becomes:

```text
exp(0) = 1
```

---

## Verified Probabilities

Softmax produced:

```text
tensor([
    0.0867,
    0.1078,
    0.0721,
    0.1990,
    0.0543,
    0.0983,
    0.1728,
    0.0717,
    0.0945,
    0.0427
])
```

with shape:

```text
[10]
```

The probabilities by vocabulary token were:

```text
'\n' →  8.6743 %
' '  → 10.7808 %
'a'  →  7.2100 %
'd'  → 19.9030 %
'e'  →  5.4275 %
'h'  →  9.8333 %
'i'  → 17.2821 %
'l'  →  7.1740 %
'm'  →  9.4486 %
'o'  →  4.2664 %
```

---

## Probability Sum

The experiment verified:

```text
PROBABILITY SUM:
1.0
```

Therefore the Softmax output forms a valid probability distribution.

Conceptually:

```text
8.67 %
+
10.78 %
+
...
+
4.27 %
≈
100 %
```

---

## Manual Probability for `l`

The logit for:

```text
'l'
```

was:

```text
-0.3606
```

The maximum logit was:

```text
0.6598
```

Therefore the shifted logit was:

```text
-0.3606 - 0.6598
=
-1.0204
```

Its exponential was approximately:

```text
exp(-1.0204)
≈
0.3605
```

The sum of the exponentials was approximately:

```text
5.0245
```

Therefore:

```text
P("l")
≈
0.3605 / 5.0245
≈
0.0717
```

or approximately:

```text
7.17 %
```

The verified PyTorch result was:

```text
7.174044847488403 %
```

---

## Highest Logit vs Highest Probability

The token with the highest logit was:

```text
'd'
```

The token with the highest probability was also:

```text
'd'
```

The experiment verified:

```text
ARGMAX LOGIT MATCHES ARGMAX PROBABILITY:
True
```

Softmax changes the scale of the values but preserves their ordering.

Therefore:

```text
argmax(logits)
=
argmax(softmax(logits))
```

---

## Manual Softmax Verification

The experiment manually implemented the stable Softmax procedure:

```text
logits
↓
subtract maximum
↓
exponential
↓
divide by exponential sum
```

The result matched PyTorch:

```text
MANUAL SOFTMAX MATCH:
True
```

This verifies that `torch.softmax` performs the expected normalization.

---

## Logits vs Probabilities

A logit is an unrestricted score:

```text
-0.3606
```

does not directly represent a percentage.

Softmax converts all competing logits jointly into probabilities.

For example:

```text
logit("l")
=
-0.3606
```

became:

```text
P("l")
≈
0.0717
```

or:

```text
7.17 %
```

The probability cannot be determined from the `"l"` logit alone.

It depends on the logits of every competing vocabulary token.

---

## Why Probabilities Depend on Competition

Softmax compares vocabulary candidates relative to each other.

If the logit for `"l"` stayed constant but the logits for competing tokens increased significantly, the probability of `"l"` would decrease.

Therefore:

```text
probability of token
```

depends on:

```text
its own logit
+
all competing logits
```

This is fundamental to next-token prediction.

---

## Greedy Prediction

If the next token were selected simply using:

```python
torch.argmax(probabilities)
```

the current untrained model would choose:

```text
'd'
```

with probability:

```text
19.90 %
```

This is called:

```text
greedy decoding
```

The model is still untrained, so this prediction has no meaningful linguistic quality.

Later experiments will study alternative sampling strategies.

---

## Hypothesis

Applying Softmax to the next-token logits should:

1. preserve the vocabulary dimension,
2. produce only positive values,
3. make the probabilities sum to one,
4. preserve the ranking of the logits,
5. match a manual stable Softmax implementation.

---

## Implementation

The experiment:

1. starts from the previously verified next-token logits,
2. applies `torch.softmax`,
3. verifies the output shape,
4. verifies that probabilities sum to one,
5. maps probabilities to vocabulary tokens,
6. compares logit argmax and probability argmax,
7. manually implements numerically stable Softmax,
8. compares the manual result with PyTorch,
9. inspects the probability associated with `"l"`.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/13_softmax_probabilities/main.py
```

---

## Verified Flow

```text
next-token logits
[10]

↓ Softmax

next-token probabilities
[10]
```

Verified:

```text
sum(probabilities) = 1.0
```

and:

```text
ARGMAX LOGIT MATCHES ARGMAX PROBABILITY:
True
```

and:

```text
MANUAL SOFTMAX MATCH:
True
```

---

## Interpretation

The model pipeline can now produce an interpretable next-token probability distribution.

The current progression is:

```text
text
↓
tokenization
↓
embeddings
↓
Transformer stack
↓
LM Head
↓
vocabulary logits
↓
Softmax
↓
next-token probabilities
```

However, the model still has no mechanism for knowing whether those probabilities are correct.

That requires comparing its predictions against the actual next-token targets.

---

## CrossEntropyLoss Preview

During training, PyTorch's:

```python
nn.CrossEntropyLoss()
```

will receive the raw logits directly.

It should not receive probabilities that have already passed through Softmax.

CrossEntropyLoss internally combines the required log-probability computation in a numerically stable way.

This will be studied explicitly in the next experiment.

---

## Conclusion

Softmax transforms unrestricted vocabulary scores into a probability distribution.

For the current untrained model:

```text
'd'
```

received the highest probability:

```text
19.90 %
```

while:

```text
'l'
```

received:

```text
7.17 %
```

The experiment manually reproduced Softmax and verified that the resulting probabilities sum to one.

The next step is to introduce the correct next-token targets and measure how wrong the model currently is.

---

## Limitations

The experiment still does not include:

- shifted next-token targets,
- CrossEntropyLoss,
- backpropagation,
- optimizer updates,
- model training,
- learned language behavior,
- temperature,
- top-k sampling,
- top-p sampling,
- autoregressive generation.

The probabilities are derived from randomly initialized model parameters.

---

## Check Yourself

### Are logits probabilities?

No.

They are unrestricted scores.

### What does Softmax produce?

A probability distribution over the vocabulary.

### What must the probabilities sum to?

```text
1
```

### Why subtract the maximum logit?

For numerical stability.

### Does subtracting the maximum change the final probabilities?

No.

### Does Softmax change which token has the highest score?

No.

```text
argmax(logits)
=
argmax(probabilities)
```

### What was the probability of `"l"`?

Approximately:

```text
7.17 %
```

### What was the highest-probability token?

```text
'd'
```

### Is that prediction meaningful yet?

No.

The model has not been trained.

### What comes next?

Shifted next-token targets and CrossEntropyLoss.