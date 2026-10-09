import math

import torch
import torch.nn as nn


# ============================================================
# 1. TRANSFORMER BLOCK
# ============================================================

class TransformerBlock(nn.Module):

    def __init__(
        self,
        d_model,
        num_heads,
        ffn_hidden_dimension,
    ):
        super().__init__()

        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dimension = (
            d_model // num_heads
        )

        self.query_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.key_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.value_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.output_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.layer_norm_1 = nn.LayerNorm(
            d_model
        )

        self.ffn_linear_1 = nn.Linear(
            d_model,
            ffn_hidden_dimension,
        )

        self.ffn_activation = nn.GELU()

        self.ffn_linear_2 = nn.Linear(
            ffn_hidden_dimension,
            d_model,
        )

        self.layer_norm_2 = nn.LayerNorm(
            d_model
        )


    def forward(self, x):

        sequence_length = x.shape[0]

        queries = self.query_projection(x)
        keys = self.key_projection(x)
        values = self.value_projection(x)

        queries = queries.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension,
        ).transpose(0, 1)

        keys = keys.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension,
        ).transpose(0, 1)

        values = values.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension,
        ).transpose(0, 1)

        attention_scores = (
            queries
            @
            keys.transpose(-2, -1)
        )

        attention_scores = (
            attention_scores
            /
            math.sqrt(
                self.head_dimension
            )
        )

        causal_mask = torch.triu(
            torch.ones(
                sequence_length,
                sequence_length,
                dtype=torch.bool,
                device=x.device,
            ),
            diagonal=1,
        )

        attention_scores = (
            attention_scores.masked_fill(
                causal_mask,
                float("-inf"),
            )
        )

        attention_weights = torch.softmax(
            attention_scores,
            dim=-1,
        )

        head_outputs = (
            attention_weights
            @
            values
        )

        multi_head_output = (
            head_outputs
            .transpose(0, 1)
            .reshape(
                sequence_length,
                self.d_model,
            )
        )

        attention_output = (
            self.output_projection(
                multi_head_output
            )
        )

        x = self.layer_norm_1(
            x + attention_output
        )

        ffn_output = self.ffn_linear_2(
            self.ffn_activation(
                self.ffn_linear_1(x)
            )
        )

        x = self.layer_norm_2(
            x + ffn_output
        )

        return x


# ============================================================
# 2. TINY LANGUAGE MODEL
# ============================================================

class TinyLanguageModel(nn.Module):

    def __init__(
        self,
        vocabulary_size,
        max_sequence_length,
        d_model,
        num_heads,
        ffn_hidden_dimension,
        num_layers,
    ):
        super().__init__()

        self.token_embedding = nn.Embedding(
            vocabulary_size,
            d_model,
        )

        self.position_embedding = nn.Embedding(
            max_sequence_length,
            d_model,
        )

        self.blocks = nn.ModuleList(
            [
                TransformerBlock(
                    d_model=d_model,
                    num_heads=num_heads,
                    ffn_hidden_dimension=(
                        ffn_hidden_dimension
                    ),
                )
                for _ in range(num_layers)
            ]
        )

        self.lm_head = nn.Linear(
            d_model,
            vocabulary_size,
            bias=False,
        )


    def forward(self, token_ids):

        sequence_length = token_ids.shape[0]

        position_ids = torch.arange(
            sequence_length,
            device=token_ids.device,
        )

        token_vectors = self.token_embedding(
            token_ids
        )

        position_vectors = self.position_embedding(
            position_ids
        )

        x = (
            token_vectors
            +
            position_vectors
        )

        for block in self.blocks:
            x = block(x)

        logits = self.lm_head(x)

        return logits


# ============================================================
# 3. VOCABULARY
# ============================================================

corpus = "hello ai\nhello model"

vocabulary = sorted(
    set(corpus)
)

token_to_id = {
    token: index
    for index, token
    in enumerate(vocabulary)
}

id_to_token = {
    index: token
    for token, index
    in token_to_id.items()
}

vocabulary_size = len(
    vocabulary
)


print("VOCABULARY:")
print(vocabulary)

print()
print(
    "VOCABULARY SIZE:",
    vocabulary_size
)


# ============================================================
# 4. TRAINING SEQUENCE
# ============================================================

training_text = "hello"

input_text = training_text[:-1]
target_text = training_text[1:]


input_ids = torch.tensor(
    [
        token_to_id[token]
        for token in input_text
    ],
    dtype=torch.long,
)

target_ids = torch.tensor(
    [
        token_to_id[token]
        for token in target_text
    ],
    dtype=torch.long,
)


print()
print("TRAINING TEXT:")
print(repr(training_text))

print()
print("INPUT:")
print(repr(input_text))

print()
print("TARGET:")
print(repr(target_text))

print()
print("INPUT IDS:")
print(input_ids)

print()
print("TARGET IDS:")
print(target_ids)


# ============================================================
# 5. SHOW TRAINING RELATIONSHIPS
# ============================================================

print()
print("TRAINING RELATIONSHIPS:")

for position_index in range(
    len(input_text)
):

    context = input_text[
        :position_index + 1
    ]

    target = target_text[
        position_index
    ]

    print(
        repr(context),
        "->",
        repr(target),
    )


# ============================================================
# 6. CREATE MODEL
# ============================================================

torch.manual_seed(42)

model = TinyLanguageModel(
    vocabulary_size=vocabulary_size,
    max_sequence_length=20,
    d_model=8,
    num_heads=2,
    ffn_hidden_dimension=32,
    num_layers=3,
)


# ============================================================
# 7. LOSS AND OPTIMIZER
# ============================================================

criterion = nn.CrossEntropyLoss()

learning_rate = 0.1

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=learning_rate,
)


# ============================================================
# 8. HELPER FOR CURRENT PREDICTIONS
# ============================================================

def inspect_predictions(
    model,
    input_ids,
    input_text,
    target_text,
):

    model.eval()

    with torch.no_grad():

        logits = model(
            input_ids
        )

        probabilities = torch.softmax(
            logits,
            dim=1,
        )

        predicted_ids = torch.argmax(
            logits,
            dim=1,
        )

    print()

    for position_index in range(
        len(input_text)
    ):

        context = input_text[
            :position_index + 1
        ]

        correct_token = target_text[
            position_index
        ]

        correct_token_id = token_to_id[
            correct_token
        ]

        predicted_token = id_to_token[
            predicted_ids[
                position_index
            ].item()
        ]

        correct_probability = (
            probabilities[
                position_index,
                correct_token_id
            ].item()
        )

        print(
            repr(context),
            "-> predicted:",
            repr(predicted_token),
            "| target:",
            repr(correct_token),
            "| target probability:",
            correct_probability,
        )


# ============================================================
# 9. PREDICTIONS BEFORE TRAINING
# ============================================================

print()
print(
    "PREDICTIONS BEFORE TRAINING:"
)

inspect_predictions(
    model=model,
    input_ids=input_ids,
    input_text=input_text,
    target_text=target_text,
)


# ============================================================
# 10. TRAINING CONFIGURATION
# ============================================================

num_steps = 100

checkpoints = {
    0,
    1,
    2,
    5,
    10,
    20,
    50,
    100,
}


print()
print("TRAINING CONFIGURATION:")

print(
    "Optimizer: SGD"
)

print(
    "Learning rate:",
    learning_rate
)

print(
    "Training steps:",
    num_steps
)


# ============================================================
# 11. TRAINING LOOP
# ============================================================

print()
print("TRAINING:")

model.train()

for step in range(
    num_steps + 1
):

    # Forward pass
    logits = model(
        input_ids
    )

    # Measure prediction error
    loss = criterion(
        logits,
        target_ids
    )

    # Inspect selected checkpoints before
    # performing the next update.
    if step in checkpoints:

        predicted_ids = torch.argmax(
            logits.detach(),
            dim=1,
        )

        predicted_text = "".join(
            id_to_token[
                token_id
            ]
            for token_id
            in predicted_ids.tolist()
        )

        print(
            "Step:",
            step,
            "| Loss:",
            loss.item(),
            "| Predictions:",
            repr(predicted_text),
        )

    # Step 100 is the final evaluation state.
    if step == num_steps:
        break

    # Remove gradients left from the
    # previous training iteration.
    optimizer.zero_grad()

    # Compute gradients.
    loss.backward()

    # Update model parameters.
    optimizer.step()


# ============================================================
# 12. FINAL LOSS
# ============================================================

model.eval()

with torch.no_grad():

    final_logits = model(
        input_ids
    )

    final_loss = criterion(
        final_logits,
        target_ids
    )


print()
print("FINAL LOSS:")
print(
    final_loss.item()
)


# ============================================================
# 13. PREDICTIONS AFTER TRAINING
# ============================================================

print()
print(
    "PREDICTIONS AFTER TRAINING:"
)

inspect_predictions(
    model=model,
    input_ids=input_ids,
    input_text=input_text,
    target_text=target_text,
)


# ============================================================
# 14. VERIFY GREEDY TRAINING PREDICTIONS
# ============================================================

with torch.no_grad():

    final_predicted_ids = torch.argmax(
        final_logits,
        dim=1,
    )


all_training_predictions_correct = (
    torch.equal(
        final_predicted_ids,
        target_ids,
    )
)


print()
print(
    "ALL TRAINING PREDICTIONS CORRECT:"
)

print(
    all_training_predictions_correct
)


# ============================================================
# 15. SHOW FINAL PREDICTED TARGET SEQUENCE
# ============================================================

predicted_target_text = "".join(
    id_to_token[
        token_id
    ]
    for token_id
    in final_predicted_ids.tolist()
)


print()
print(
    "EXPECTED TARGET SEQUENCE:"
)

print(
    repr(target_text)
)


print()
print(
    "PREDICTED TARGET SEQUENCE:"
)

print(
    repr(predicted_target_text)
)