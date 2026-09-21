# LLM fundamentals

**IN PROGRESS — introductory concepts, not a completed practical study.** No language model has been executed as part of this lesson.

## Objective

What lies between application text and a generated token, and which component is responsible for each step?

## Model vocabulary

| Term | Introductory meaning |
|---|---|
| Model | A parameterized mathematical function; a trained model combines a computation structure with learned numerical values. |
| Architecture | The structure of operations and connections, such as layers in a neural network. |
| Parameters | Numerical values that training can adjust, including weights and biases. |
| Weights | Learned parameter values controlling contributions within the computation. Downloaded artifacts typically include parameter tensors and configuration. |
| Training | Computing a loss from examples and adjusting parameters through an optimization procedure. |
| Inference | Computing outputs with existing parameters, normally without updating them. |
| Tokenizer | Rules/software mapping text to token IDs and decoding token sequences to text. |
| Tokens | Units represented by IDs; they can be word pieces, punctuation or other units, not necessarily words. |
| Embeddings | Numerical vectors representing tokens; a learned lookup maps token IDs to vectors used by the network. This introduction does not implement semantic search. |
| Logits | Raw scores for candidate next tokens before normalization. |
| Sampling | Selecting a next token using a distribution derived from logits; greedy selection instead takes the highest-scoring candidate. |
| Context window | The supported token context for a model/runtime configuration. Inputs and generated continuation consume context; this is not unlimited persistent memory. |

## Components with different responsibilities

- **MODEL:** architecture and learned parameters define the transformation.
- **RUNTIME:** software loads a compatible model representation and executes inference.
- **APPLICATION:** software decides what input to send, how to present output and what actions are permitted.
- **HARDWARE:** processors and memory support the numerical computation.

See the [ecosystem map](../../../docs/ecosystem-map.md) for the API and compute layers. Runtime tooling and model families are examples there, not completed experiments.

## Conceptual generation loop

```text
Application text → tokenizer → token IDs → embeddings → model computation
    → next-token logits → selection/sampling → append token → repeat
```

The runtime performs the computation on hardware; the application receives decoded output. This simplified loop omits implementation details. Generating more text does not normally retrain the weights. Detailed architecture, sampling controls and context handling remain future study.

## Hypothesis and practical follow-up

A later tokenization experiment should show that token counts differ from word counts. A later inference experiment should make the application/runtime/model boundary observable. Neither is implemented here yet; follow the [roadmap](../../../ROADMAP.md).

## Evidence and limitations

Not verified yet on the current environment.

This is conceptual documentation, with no `main.py`, model download, measured output or practical conclusion. Earlier neural-network experiments illustrate parameters and logits, but do not establish LLM behavior.

## Product connection

**Concept:** inference uses learned parameters. **Implementation:** this lesson traces the intended computation only. **Product:** a text application needs a compatible runtime, input/output handling, resource limits and evaluation beyond the model itself.

## Check yourself

- How do architecture, parameters and trained weights differ?
- What changes during training but normally stays fixed during inference?
- Why is a token not necessarily a word?
- How do embeddings differ from token IDs and logits?
- Where does next-token selection happen in the conceptual loop?
- Why are runtime, application and hardware separate from the model?
- Why does a context window not imply permanent memory?
