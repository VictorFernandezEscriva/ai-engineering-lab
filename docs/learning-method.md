# Learning method

**Concept → Question → Hypothesis → Implementation → Experiment → Evidence → Conclusion → Limitations → Product connection**

1. **Concept:** explain the mechanism in plain language and define the terms needed to understand it.
2. **Question:** identify a specific uncertainty that a small experiment can address.
3. **Hypothesis:** state the expected behavior before running, including what would contradict it.
4. **Implementation:** connect the idea to executable code when practical. Explain important decisions in the README and non-obvious behavior in comments.
5. **Experiment:** run the root-relative command. Record data, split, seed, dependency versions and relevant hardware. Change one variable when making a comparison.
6. **Evidence:** record actual outputs or measurements and their provenance. Separate expected behavior, historical observations and current runs. Use “Not verified yet on the current environment.” when applicable.
7. **Conclusion:** answer the question only as far as the evidence allows. Two correct test predictions do not establish general accuracy.
8. **Limitations:** name weak spots such as synthetic data, duplicate samples, tiny test sets, a single seed, missing validation, hardware dependence or absent baselines.
9. **Product connection:** distinguish the concept, the small implementation and the engineering work required to use the idea in a real product.

## Recording a run

Include the date, command, Python/dependency versions, seed, dataset/split, relevant hardware, observed output and interpretation. Failed execution is useful evidence about the environment, not about model quality. Do not convert an expected tensor shape into a measured result.

Use validation data to select settings and reserve test data for final evaluation. Mark comparisons proposed for later work explicitly; do not describe them as implemented.

## Growing the lab

Organize by technical domain. Keep future subjects in the [roadmap](../ROADMAP.md) until they have real study material. Larger integrations go in [projects](../projects/README.md). Extend the glossary only when concepts appear in actual notes or code. Finish a study pass by answering its “Check yourself” questions without copying definitions.
