# Experiment 24 — Language-Model Head and Vocabulary Logits

## Objective

How does a Transformer convert an internal contextual representation into scores for actual vocabulary tokens?

Previous experiments produced final Transformer representations with shape:

```text
[sequence_length, d_model]
```

For the sequence:

```text
hel
```

the final Transformer stack produced:

```text
[3, 8]
```

This experiment introduces the language-model head:

```text
d_model
↓
Linear
↓
vocabulary_size
```

which converts each contextual representation into one score for every token in the vocabulary.

These scores are called:

```text
logits
```

---

## Vocabulary

The character-level vocabulary is:

```text
['\n', ' ', 'a', 'd', 'e', 'h', 'i', 'l', 'm', 'o']
```

Therefore:

```text
vocabulary_size = 10
```

The token IDs are:

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

---

## Transformer Output

The input sequence is:

```text
hel
```

After embeddings and three Transformer blocks, the final representations were:

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

Each row corresponds to one sequence position.

Because of causal attention:

```text
position 0 → contextual representation of "h"

position 1 → contextual representation of "he"

position 2 → contextual representation of "hel"
```

---

## Language-Model Head

The language-model head is:

```python
lm_head = nn.Linear(
    d_model,
    vocabulary_size,
    bias=False
)
```

With the current model dimensions:

```text
Linear(8 → 10)
```

Therefore each token representation:

```text
[8]
```

becomes:

```text
[10]
```

one score for every vocabulary token.

For the complete sequence:

```text
[3, 8]
↓
LM Head
[3, 10]
```

---

## Vocabulary Logits

The experiment produced:

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

Conceptually:

```text
"h"   → 10 vocabulary logits

"he"  → 10 vocabulary logits

"hel" → 10 vocabulary logits
```

---

## Why Are There Three Logit Rows?

The Transformer produces one contextual representation for every input position.

The same language-model head is applied to every position.

Therefore:

```text
3 contextual representations
×
10 vocabulary scores
=
[3, 10]
```

Each row can be interpreted as a next-token prediction from a different amount of context.

For:

```text
h e l
```

causal attention gives:

```text
position 0:
context = "h"

position 1:
context = "he"

position 2:
context = "hel"
```

Therefore the three output rows conceptually ask:

```text
after "h", what comes next?

after "he", what comes next?

after "hel", what comes next?
```

---

## Training vs Generation

This distinction is fundamental.

### During Training

All positions are useful.

For part of the training text:

```text
hello
```

the model can learn several next-token predictions simultaneously:

```text
input context    target

"h"              "e"
"he"             "l"
"hel"            "l"
"hell"           "o"
```

A sequence therefore provides many training examples at once.

---

### During Generation

Suppose the current prompt is:

```text
hel
```

The model only needs to answer:

```text
what token comes after the full context "hel"?
```

Therefore only the final position is needed:

```python
next_token_logits = logits[-1]
```

The transformation is:

```text
all sequence logits
[3, 10]

↓ select final row

next-token logits
[10]
```

The first two rows are not needed to choose the continuation of the complete prompt.

---

## Final-Context Logits

For:

```text
hel
```

the final-position logits were:

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

These correspond to:

```text
'\n' → -0.1707
' '  →  0.0467
'a'  → -0.3556
'd'  →  0.6598
'e'  → -0.6396
'h'  → -0.0453
'i'  →  0.5186
'l'  → -0.3606
'm'  → -0.0852
'o'  → -0.8803
```

The largest current logit is:

```text
'd' → 0.6598
```

so greedy selection from the untrained model would currently produce:

```text
hel → d
```

This is not expected to be linguistically correct because the model has not been trained.

---

## What Is a Logit?

A logit is an unrestricted score.

For example:

```text
0.6598
```

does not mean:

```text
65.98%
```

and it does not represent a probability.

Logits can be:

```text
positive
negative
zero
greater than one
smaller than minus one
```

What matters is their relative magnitude.

A later softmax operation can convert the logits into a probability distribution.

---

## LM Head Weight Matrix

The language-model head contains:

```text
vocabulary_size × d_model
```

weights.

In this experiment:

```text
[10, 8]
```

Conceptually:

```text
'\n' → [8 weights]
' '  → [8 weights]
'a'  → [8 weights]
'd'  → [8 weights]
'e'  → [8 weights]
'h'  → [8 weights]
'i'  → [8 weights]
'l'  → [8 weights]
'm'  → [8 weights]
'o'  → [8 weights]
```

Each vocabulary token therefore owns a learned direction in the language-model head.

---

## Manual Logit Calculation

The experiment inspected token:

```text
'l'
```

whose token ID is:

```text
7
```

Its language-model head weight vector was:

```text
[ 0.0460,
  0.3130,
  0.3037,
 -0.1663,
 -0.0145,
 -0.1781,
  0.1269,
 -0.3426]
```

The contextual representation inspected was:

```text
[-0.4163,
 -1.6652,
  0.0709,
  1.3738,
 -0.5926,
 -0.6755,
  1.4719,
  0.4330]
```

The logit for `"l"` is the dot product:

```text
representation
·
LM-head weight for "l"
```

which means:

```text
x1*w1
+
x2*w2
+
x3*w3
+
x4*w4
+
x5*w5
+
x6*w6
+
x7*w7
+
x8*w8
```

The manual result was:

```text
-0.579900860786438
```

The automatic PyTorch result was:

```text
-0.579900860786438
```

The experiment verified:

```text
MANUAL LOGIT MATCH:
True
```

---

## Important Architectural Separation

Attention does not directly choose vocabulary tokens.

Attention produces contextual representations.

The full flow is:

```text
tokens
↓
embeddings
↓
Transformer blocks
↓
contextual representations
↓
LM Head
↓
vocabulary logits
```

Therefore:

```text
ATTENTION
→ builds contextual information
```

while:

```text
LM HEAD
→ maps contextual information to vocabulary scores
```

---

## Shape Progression

The complete model pipeline currently reaches:

```text
token IDs
[3]

↓ embeddings

[3, 8]

↓ Transformer stack

[3, 8]

↓ LM Head

[3, 10]
```

During generation:

```text
[3, 10]

↓ select final sequence position

[10]
```

These ten values are the next-token logits for the full context.

---

## Hypothesis

The language-model head should:

1. receive one `d_model` representation per sequence position,
2. produce one logit per vocabulary token,
3. preserve the sequence dimension,
4. transform `[3, 8]` into `[3, 10]`,
5. allow an individual logit to be reproduced with a dot product,
6. provide only `[10]` final-context logits when the final sequence position is selected.

---

## Implementation

The experiment:

1. builds token and positional embeddings,
2. passes them through three Transformer blocks,
3. obtains final contextual representations,
4. defines `Linear(d_model, vocabulary_size)`,
5. produces vocabulary logits for every position,
6. inspects one position,
7. maps logits back to vocabulary tokens,
8. identifies the highest logit,
9. inspects one LM-head weight vector,
10. manually reproduces one vocabulary logit,
11. selects the final row for next-token generation.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/12_lm_head_logits/main.py
```

---

## Interpretation

The Transformer stack does not directly output letters or words.

It outputs internal vectors.

The language-model head provides the bridge:

```text
internal representation
↓
vocabulary scores
```

For a vocabulary of ten tokens:

```text
representation [8]
↓
LM Head
↓
10 logits
```

During generation, only the final contextual representation is needed to decide what should come after the complete prompt.

During training, every sequence position can provide a next-token prediction target.

---

## Conclusion

The educational language model can now transform:

```text
"hel"
```

into:

```text
10 scores for the token after "hel"
```

The complete pipeline is now:

```text
text
↓
token IDs
↓
token embeddings
+
position embeddings
↓
Transformer stack
↓
contextual representations
↓
LM Head
↓
vocabulary logits
```

The next step is to convert these raw scores into a probability distribution with softmax.

---

## Limitations

The current model still does not include:

- trained parameters,
- probabilities,
- next-token loss,
- target shifting,
- backpropagation,
- optimizer updates,
- training loop,
- probabilistic sampling,
- generated sequences.

The current logits are produced by randomly initialized parameters.

---

## Check Yourself

### What does the Transformer stack output?

Contextual vectors with dimension `d_model`.

### What does the LM Head output?

One logit for every vocabulary token.

### What shape transformation does the LM Head perform?

```text
[sequence_length, d_model]
→
[sequence_length, vocabulary_size]
```

### Why are there three rows of logits for `"hel"`?

Because the model produces a next-token prediction for every sequence position.

### What context does the final row represent?

```text
"hel"
```

### Which row is used to generate the next token after `"hel"`?

The final row:

```python
logits[-1]
```

### Are logits probabilities?

No.

They are unrestricted scores.

### How is one logit calculated?

By taking the dot product between the contextual representation and the LM-head weight vector associated with one vocabulary token.

### What comes next?

Softmax and next-token probabilities.