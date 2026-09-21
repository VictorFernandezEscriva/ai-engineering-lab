# AI Engineering Lab

A hands-on AI Engineering Lab focused on understanding AI systems through implementation and experiments. This repository is both a personal technical notebook and an engineering portfolio: the code, evidence and limitations should make it clear what was studied and what remains untested.

**Concept → Implementation → Experiment → Evidence → Engineering conclusion → Product connection**

Experiments are deliberately small so mechanisms remain visible. Their existence does not imply professional mastery or production readiness.

## Structure

- [topics/01_machine_learning](topics/01_machine_learning/README.md): decision trees and generalization.
- [topics/02_deep_learning](topics/02_deep_learning/README.md): binary neural classifiers and evaluation.
- [topics/03_computer_vision](topics/03_computer_vision/README.md): convolutions, shape CNNs and dataset loading.
- [topics/04_llm_engineering](topics/04_llm_engineering/README.md): LLM fundamentals, in progress.
- [docs](docs/learning-method.md): learning method, [ecosystem map](docs/ecosystem-map.md), [glossary](docs/glossary.md) and [verification evidence](docs/verification.md).
- [tools/hardware_report.py](tools/hardware_report.py): reusable local hardware diagnostic.
- [projects](projects/README.md): larger integrations combining studied concepts; none implemented yet.
- [ROADMAP.md](ROADMAP.md): future study, without placeholder topic or project folders.

Folders group technical domains, not past versus future learning. Numeric prefixes support navigation; roadmap phases do not prescribe directory creation.

## Progress

| Domain | Status |
|---|---|
| Machine Learning | Two existing experiments reviewed; historical results retained |
| Deep Learning | Two existing experiments reviewed; historical results retained |
| Computer Vision | Five implementations reviewed; two have historical outputs, CNN runs and MNIST download remain unverified |
| LLM Engineering | In progress: conceptual introduction |
| Local inference | Planned |
| RAG | Planned |
| Agents | Planned |
| Product integration | Planned |

Current execution blockers are recorded in the [verification log](docs/verification.md). Completed learning exercises are not evidence that a whole field has been mastered.

## Setup and run

From the repository root:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python topics/01_machine_learning/01_decision_tree/main.py
python tools/hardware_report.py
```

Each experiment README gives its root-relative command. MNIST downloads into ignored `data/`; the shape CNNs perform 1000 full-batch epochs, and the evaluation script opens plots. Requirements preserve the original unpinned dependencies; identical results across installations are not guaranteed. No paid service is required by the current code.

## Evidence and growth

Follow the [learning method](docs/learning-method.md): state a question and hypothesis, inspect the implementation, run it, record observations, and limit conclusions to the evidence. Historical observations are labelled separately from current verification. Fixed seeds help comparisons but do not guarantee identical results across platforms.

Larger systems belong in [projects/](projects/README.md) once work begins. Keep model weights, downloaded datasets, secrets and generated caches outside Git.

## License

No open-source license is provided for this repository.

The source code and documentation are published as part of a personal learning and engineering portfolio.
