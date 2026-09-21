# Living glossary

Terms used in current experiments and introductory notes. Inclusion means introduced, not mastered. Add future terminology when its lesson begins.

## Feature / target

An input measurement / the label or value a supervised model learns to predict.

## Train / test split

Separate data used to fit a model from data used to evaluate it.

## Generalization / overfitting

Performance on unseen data / learning training-specific patterns that transfer poorly.

## Decision tree

A predictor that follows learned feature-based branches to a leaf.

## Hyperparameter

A setting chosen outside parameter fitting, such as maximum tree depth.

## Tensor

A multidimensional numerical array used for data and model computation.

## Standardization

Subtract a feature mean and divide by its standard deviation; fit these statistics on training data for held-out evaluation.

## Model / architecture

A parameterized function / its operation and connection structure.

## Parameter / weight

A numerical model value that training can adjust / a parameter controlling contributions within operations.

## Training / inference

Adjusting parameters using an objective / computing outputs using existing parameters.

## Logit / sigmoid

A raw score / the function mapping a binary logit into a probability-like value between zero and one.

## Loss / gradient / optimizer

An objective measuring error / its local derivatives / the procedure applying parameter updates.

## ReLU

An activation that returns zero for negative inputs and the input otherwise.

## Threshold

A cutoff that converts a continuous binary score into a class decision.

## Precision / recall / F1

The fraction of predicted positives that are correct / the fraction of actual positives found / their harmonic mean.

## Confusion matrix

Counts of predicted versus actual classes; binary errors are false positives and false negatives.

## Convolution / kernel / feature map

A local weighted operation / its weights / the resulting output grid; PyTorch Conv2d uses cross-correlation without flipping the kernel.

## Pooling

Spatial aggregation that reduces resolution, such as taking a maximum over each local region.

## Tokenizer / token

Text encoding software / a unit represented by an ID, not necessarily a word.

## Embedding

A numerical vector representation; the introductory LLM lesson describes token embeddings.

## Sampling

Selecting an output token from a distribution derived from logits.

## Context window

The supported token context of a model/runtime configuration.

## Runtime / application

Software executing model inference / software defining user-facing behavior and domain logic.

## RAM / VRAM

System memory / memory associated with a GPU; the hardware tool reports what its interfaces can detect.
