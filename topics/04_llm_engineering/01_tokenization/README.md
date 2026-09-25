# Experiment 13 — Character Tokenization and Token IDs

## Objective

How can raw text be converted into numerical identifiers that a neural network can process?

Neural networks do not directly operate on strings such as:

```text
hello ai
```

Text must first be transformed into a numerical representation.

This experiment introduces the first stages of a language-model input pipeline:

```text
text
↓
tokens
↓
token IDs
```

No neural network is trained in this experiment.

## Concepts

### Text

The experiment begins with a small corpus:

```text
hello ai
hello model
```

The corpus is simply the text collection used to build the tokenizer vocabulary.

### Character-level tokenization

This experiment uses character-level tokenization.

Each character becomes one token.

For example:

```text
hello ai
```

becomes:

```text
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']
```

The space character is also a token.

The newline character in the corpus is another token.

Character-level tokenization is intentionally simple and is used here to understand the mechanics of tokenization.

Modern language models often use subword tokenization instead.

### Vocabulary

The vocabulary contains every unique token known by the tokenizer.

The experiment creates it with:

```python
vocabulary = sorted(set(corpus))
```

The verified vocabulary was:

```text
['\n', ' ', 'a', 'd', 'e', 'h', 'i', 'l', 'm', 'o']
```

Therefore:

```text
Vocabulary size = 10
```

Each unique token appears only once in the vocabulary.

### Token IDs

Neural networks cannot use character strings directly as model inputs.

Each token is therefore assigned an integer identifier.

The verified mapping was:

```text
'\n' → 0
' '  → 1
'a'  → 2
'd'  → 3
'e'  → 4
'h'  → 5
'i'  → 6
'l'  → 7
'm'  → 8
'o'  → 9
```

These integers are identifiers.

They do not represent semantic magnitude.

For example:

```text
"h" → 5
"e" → 4
```

does not mean that `h` is mathematically larger or more important than `e`.

### Encoding

Encoding converts tokens into token IDs.

The text:

```text
hello ai
```

was tokenized as:

```text
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']
```

and encoded as:

```text
[5, 4, 7, 7, 9, 1, 2, 6]
```

Conceptually:

```text
text
↓
tokens
↓
token IDs
```

### Token ID tensor

The token IDs were converted to a PyTorch tensor:

```text
tensor([5, 4, 7, 7, 9, 1, 2, 6])
```

with:

```text
shape:
[8]

dtype:
torch.int64
```

PyTorch also refers to `torch.int64` as:

```text
torch.long
```

Integer token IDs will later be used as indices into an embedding table.

### Decoding

The inverse mapping converts token IDs back into tokens.

The verified sequence:

```text
[5, 4, 7, 7, 9, 1, 2, 6]
```

was decoded into:

```text
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']
```

and then reconstructed as:

```text
hello ai
```

The verified result was:

```text
Matches original: True
```

This confirms that the encode/decode mappings are consistent for known tokens.

### Token vs token ID

A token and a token ID are different concepts.

For example:

```text
token:
"h"

token ID:
5
```

The token is the textual unit.

The token ID is the integer used to identify it.

### What is still missing?

Token IDs alone are not meaningful learned representations.

For example:

```text
5
```

only identifies token `"h"`.

The next stage will introduce embeddings:

```text
token ID
↓
embedding lookup
↓
vector
```

For example:

```text
5
↓
[0.21, -0.82, 0.14, 0.37, ...]
```

Those vectors can become trainable numerical representations used by neural networks.

## Hypothesis

A character-level vocabulary should allow known text to be:

1. split into tokens,
2. converted into integer token IDs,
3. stored as a PyTorch integer tensor,
4. decoded back into the original text.

## Implementation

The experiment:

1. Defines a small text corpus.
2. Extracts all unique characters.
3. Creates a vocabulary.
4. Assigns one integer ID to every token.
5. Creates a reverse ID-to-token mapping.
6. Tokenizes `hello ai`.
7. Encodes the tokens as integer IDs.
8. Converts the IDs into a PyTorch tensor.
9. Inspects individual token mappings.
10. Decodes the token IDs back into text.
11. Verifies that the reconstructed text matches the original.

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/01_tokenization/main.py
```

## Observed Results

The verified corpus was:

```text
hello ai
hello model
```

The vocabulary was:

```text
['\n', ' ', 'a', 'd', 'e', 'h', 'i', 'l', 'm', 'o']
```

with:

```text
Vocabulary size: 10
```

The token-to-ID mapping was:

```text
{
    '\n': 0,
    ' ': 1,
    'a': 2,
    'd': 3,
    'e': 4,
    'h': 5,
    'i': 6,
    'l': 7,
    'm': 8,
    'o': 9
}
```

The original text was:

```text
hello ai
```

The tokens were:

```text
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']
```

The token IDs were:

```text
[5, 4, 7, 7, 9, 1, 2, 6]
```

The PyTorch tensor was:

```text
tensor([5, 4, 7, 7, 9, 1, 2, 6])
```

with:

```text
Tensor shape: torch.Size([8])
Tensor dtype: torch.int64
```

The individual mappings were:

```text
'h' → 5
'e' → 4
'l' → 7
'l' → 7
'o' → 9
' ' → 1
'a' → 2
'i' → 6
```

Decoding reconstructed:

```text
hello ai
```

and verification produced:

```text
Matches original: True
```

## Interpretation

The experiment demonstrates that tokenization and numerical encoding are separate operations.

The full transformation is:

```text
RAW TEXT
"hello ai"

↓ tokenization

TOKENS
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']

↓ encoding

TOKEN IDs
[5, 4, 7, 7, 9, 1, 2, 6]

↓ PyTorch tensor

tensor([5, 4, 7, 7, 9, 1, 2, 6])
```

The resulting integers are now compatible with PyTorch operations.

However, they should not be treated as numerical features directly.

Their purpose is to identify vocabulary entries.

The next representation layer will convert those IDs into embedding vectors.

## Conclusion

This experiment establishes the first part of a language-model input pipeline:

```text
text
↓
tokenization
↓
tokens
↓
vocabulary lookup
↓
token IDs
```

The verified tokenizer successfully encoded and decoded:

```text
hello ai
```

without information loss for the known vocabulary.

This provides the foundation for the next experiment:

```text
token IDs
↓
embeddings
```

## Limitations

This tokenizer is deliberately simple.

Limitations include:

* character-level tokenization only,
* vocabulary built from a tiny corpus,
* no unknown-token handling,
* no special tokens,
* no padding,
* no batching,
* no subword tokenization,
* no real tokenizer algorithm,
* no learned representations,
* no language model,
* no training.

If a character is not present in the vocabulary, encoding it will currently fail.

Modern LLM tokenizers use substantially more sophisticated vocabulary and tokenization strategies.

## Product Connection

### Concept

Language models require text to be converted into numerical model inputs.

### Implementation

The pipeline begins with:

```text
text
↓
tokenizer
↓
token IDs
```

### Product

A production LLM system may receive:

```text
"Explain convolution"
```

but the neural network internally operates on something closer to:

```text
[15496, 2437, 318, ...]
```

The exact IDs depend on the tokenizer and vocabulary used by the model.

Tokenization is therefore part of the model interface and must remain compatible with the model's trained vocabulary.

## Check Yourself

### What is a token?

A token is one unit produced by a tokenizer.

In this experiment, each character is one token.

### What is a vocabulary?

The vocabulary is the collection of all tokens known by the tokenizer.

### What is a token ID?

A token ID is an integer that identifies one token in the vocabulary.

### Does token ID `9` mean that token `"o"` has numerical value 9?

No.

The number is only an identifier.

### Why use integer token IDs?

They provide an efficient way to reference vocabulary entries and later perform embedding lookups.

### Why is the tensor dtype `torch.int64`?

Embedding layers use integer indices to select rows from an embedding table.

PyTorch commonly represents these indices using `torch.long`, equivalent to `torch.int64`.

### What does decoding do?

Decoding converts token IDs back into tokens and reconstructs text.

### Why does `Matches original: True` matter?

It confirms that encoding and decoding are consistent for this text and vocabulary.

### What happens if the text contains an unknown character?

The current implementation will fail because no token ID exists for that character.

Handling unknown tokens will require additional tokenizer logic.

### What comes next?

The next stage is:

```text
token ID
↓
embedding vector
```

This will convert identifiers into vectors that can be learned and processed by a neural network.