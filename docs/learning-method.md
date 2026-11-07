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

## Incremental delivery

Larger future experiments are decomposed so that each meaningful commit or PR-sized increment either delivers user value or creates a deliberate, verified technical milestone:

```text
problem → small milestone → acceptance criterion → implementation → tests / evaluation → evidence → next milestone
```

For a non-trivial experiment, write down the scope and acceptance criteria first, commit in small steps, add tests, record README / result evidence, and state known limitations and the next step. Do not manufacture commits for tiny exercises; a ten-line concept check is one unit.

## Outcome-oriented engineering

Every relevant automation or AI experiment answers: What problem are we solving? What is the baseline? What metric defines success? What changed? What evidence shows improvement? What failure modes remain? What is the simplest architecture that works? The aim is a record of engineering outcomes, not demos.

## Prompts, evaluation and technologies

Prompts are engineering artifacts: define expected behavior, write the prompt, build evaluation cases, observe and classify failures, change prompt / context / tools, rerun the evaluations, then version the improvement. Do not tune wording ad hoc.

Do not create a curriculum node for every product. Concepts and capabilities are nodes; technologies we will practice are registered with a tier (`hands-on`, `compare`, `awareness`, `enterprise-mapping`) in the Cockpit `technologies` registry. See [Professional capabilities and technology tiers](professional-capabilities.md).

## Experiment numbering

Two numbers exist and mean different things:

- **Local folder sequence** — the order inside one topic directory, e.g. `topics/04_llm_engineering/02_embeddings/` is the second folder of that topic.
- **Global Experiment NN** — the order across the whole Lab curriculum, as used by the roadmap and the Cockpit, e.g. that same folder is **Experiment 14**.

The global number is the position of the experiment in the Cockpit catalog's ordered `exercises` list; it is derived, not stored in a second registry. Existing folder names are historical and are not renamed. The Cockpit shows "Experiment NN — title"; repository paths keep the local number. Phase experiment indexes (for example [Phase 04](../topics/04_llm_engineering/README.md#experiment-index)) list both.

## Keeping the lab navigable

Prefer one canonical source and derived views over synchronized copies: the roadmap holds the order, `catalog.json` holds machine-readable relations and one `content_path` per concept, experiment READMEs hold theory and results, SQLite holds personal progress. Write theory when a phase begins; until then a concept honestly shows "Theory: planned". Do not generate documentation in advance to fill the map.

## Growing the lab

Organize by technical domain. Keep future subjects in the [roadmap](../ROADMAP.md) until they have real study material. Learn the underlying concepts here before combining them into larger systems in independent repositories. This lab does not plan or catalog those repositories. Extend the glossary only when concepts appear in actual notes or code. Finish a study pass by answering its “Check yourself” questions without copying definitions.

Use the [AI Engineering Map](ai-engineering-map.md) to locate a concept in the field and the roadmap to choose the next step. The lab contains theory, concept explanations, small focused experiments and small exercises. Complex areas such as RAG, coding agents, MCP, LangGraph, n8n, voice and multimodal AI can have small controlled lab experiments. Group related operations around a meaningful question rather than creating an experiment for every line of code.

**Fundamentals first, framework second:** understand the primitive, build a minimal version, understand its limitations, then compare a framework when it answers a real question. **ZERO EXTRA COST:** prefer open-source software, local models, local execution and free official resources; paid services are not prerequisites.
