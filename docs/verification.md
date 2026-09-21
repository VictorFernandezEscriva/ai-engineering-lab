# Verification Log

Historical entries below were supplied with the repository. They are preserved as prior observations, not runs performed during the current reorganization. The original environment, dependency versions and raw logs were not recorded.

The purpose is to separate **observed evidence** from claims made in notes.

## Current reorganization — 2026-09-21

Environment: Windows 11, Python 3.13.2. NumPy and pandas are available; scikit-learn, PyTorch, torchvision and matplotlib are absent. Original requirements are retained without version pins.

All nine documented experiment commands were attempted from the repository root. Both ML scripts stopped at import with `ModuleNotFoundError: No module named 'sklearn'`. The seven deep-learning and vision scripts stopped with `ModuleNotFoundError: No module named 'torch'`. No training or dataset download occurred in these attempts.

**Not verified yet on the current environment.** This applies to all nine experiment outcomes, including the historical results below. Install the dependencies using the root README before rerunning; no result is inferred from an import failure.

`python tools/hardware_report.py` completed successfully: it reported 15.42 GiB system RAM, an NVIDIA GeForce RTX 2060 with Max-Q Design with 6.0 GiB VRAM, driver 555.97, and PyTorch not installed. This verifies the diagnostic on this machine only, not inference performance or CUDA availability in a future PyTorch installation.

Static validation parsed all ten Python source files successfully without generating bytecode. All Markdown link targets and documented Python script paths resolve. No obsolete directory references, bytecode caches or empty topic placeholders remain. Nine educational scripts were relocated; executable logic and requirements were preserved. Three explanatory comments were added, without changing computation.

## Historical observations from the supplied notes

### Decision tree

Observed:

```text
Accuracy: 1.0
Prediction: [1]
```

Important limitation: the test split contains only two samples, so this result is not evidence of a generally 100%-accurate classifier.

### Overfitting / generalization experiment

Observed:

```text
Training accuracy: 0.9714285714285714
Test accuracy: 0.9166666666666666
```

That recorded run demonstrates a measurable training/test gap on the synthetic noisy dataset.

### Binary PyTorch classifier

Observed loss decreased from approximately `0.70` to near zero during training. The selected test motor produced a very large positive logit and a sigmoid probability displayed as `1.0`.

Limitation: this version trains on ten manually defined examples and scores a supplied motor without an independent test set, so it is a learning exercise rather than a generalization benchmark.

### PyTorch train/test + thresholds

Recorded on one seeded run:

| Threshold | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.3 | 0.667 | 0.667 | 0.667 |
| 0.5 | 0.600 | 0.500 | 0.545 |
| 0.7 | 1.000 | 0.500 | 0.667 |

Training accuracy was `1.0` while test mistakes remained. This is useful evidence that a perfect training score does not imply perfect behavior on unseen samples and that the decision threshold changes the precision/recall trade-off.

### Manual convolution

The fixed horizontal-transition kernel produced positive responses on one edge, zero in uniform regions and negative responses on the opposite edge.

### Multiple convolution filters

Three fixed filters produced three distinct feature maps with shape:

```text
torch.Size([1, 3, 4, 4])
```

This verifies that `out_channels=3` produces three learned/fixed output feature maps.

## Historical pending verification

### Synthetic shape CNN

The original script performs 1000 full-batch epochs. It was not fully re-run in the CPU-only rebuild environment because it exceeded the verification time budget.

The code remains available and should be run on the learner's own machine. Its README separates implementation from unverified conclusions.

### Shape CNN evaluation and feature maps

Implemented, including train/test evaluation and feature-map plotting. Full run pending on the learner's machine.

### MNIST dataset loading

The script is valid structurally, but the rebuild environment could not access the public MNIST download servers. Verification should be completed locally where network access is available.

## Rule going forward

A README may say **implemented** when code exists. It should say **verified** only when the stated experiment has actually been run and its result recorded.
