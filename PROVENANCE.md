# Sources, contribution boundaries, and assistance

Record date: **12 October 2026**. This document preserves the source audit performed before the v0.1 editorial revision. The revision itself is not a new literature search. The mathematical paper and the search record have different purposes.

## Contribution boundaries

| Source | Contribution used here | What this manuscript adds |
| --- | --- | --- |
| Bertschinger, Hoefer and Schmand, *Flow Allocation Games*, MOR 50(1):68–89 (2025), [DOI](https://doi.org/10.1287/moor.2022.0355), [author PDF](https://algo.rwth-aachen.de/team/hoefer/papers/Bertschinger23Flow.pdf) | Model, greatest clearing, strongly polynomial TopCycleIncrease, strong NP-hardness, conditional alarm at positive input; Remark 3 leaves the precise classification open. | A completed Σ₂ᵖ-hardness reduction for that same all-strategic model, matching the existing upper bound. |
| Public problem-107 progress note; author identity unverified | Guarded quantified-Boolean architecture, constants R/K/B/S, selectors, tester, guards, collectors, fixed-priority overflow construction, and corrected zero-input alarm behavior. | Strategic threshold implementation with a uniform strict-dominance margin, plus global correctness for arbitrary tester and fanout orders. |
| Kanellopoulos, Kyropoulou and Zhou, *On priority-proportional payments in financial networks*, TCS 1014:114767 (2024), [DOI](https://doi.org/10.1016/j.tcs.2024.114767), [accepted manuscript](https://repository.essex.ac.uk/38989/1/Project_1_PPFN_TCS%20%2814%29.pdf) | Section 6 already uses a lossy private pair for subtraction, with priority incentives. The basic threshold mechanism is prior work. | A bound comparing at least M versus at most T across different feedback states, used under greatest clearing and outgoing-flow utility to complete the original ER-NE reduction. |
| Guha, Kupferman and Vardi, *Multi-Player Flow Games*, AAMAS 2018, pp. 104–112, [paper](https://www.ifaamas.org/Proceedings/aamas2018/pdfs/p104.pdf) | Prior Σ₂ᵖ-completeness in a different flow-game model: multi-vertex control, designated-target utility, and general allocation policies on acyclic graphs. | Classification for one vertex per player, strict edge permutations, outgoing-flow utility, and greatest clearing. |

The result is a completion using established methods. Neither the guarded QBF architecture nor the formula `(t-H)+` is claimed to be invented here. The manuscript does not claim a universal compiler for arbitrary prescribed priorities.

## Pinned public progress note

- Title: *Progress on Nash-Existence in Edge-Ranking Flow Allocation Games: A Rigorous Conditional Σ₂ᵖ-Hardness Reduction*.
- Note date: **23 June 2026**; repository upload: **26 June 2026**.
- Repository: `ai-in-math-or/open-problems-in-or`.
- Path: `data/llm_math_export/solution_progress/W4391111008_p0/partial_progress/107.pdf`.
- Inspected snapshot: `3b2de3237c29623f479c52c31db54fd60b97fd3c`.
- Path-history commit: `8f63022a1bf4081897ad169e78b5966871c9e0fa`.
- PDF blob: `0babdce1e2e2d4abe0fbddcbe9f20a564b4d2fe6`.
- [Pinned GitHub view](https://github.com/ai-in-math-or/open-problems-in-or/blob/3b2de3237c29623f479c52c31db54fd60b97fd3c/data/llm_math_export/solution_progress/W4391111008_p0/partial_progress/107.pdf).
- [Pinned direct download](https://raw.githubusercontent.com/ai-in-math-or/open-problems-in-or/3b2de3237c29623f479c52c31db54fd60b97fd3c/data/llm_math_export/solution_progress/W4391111008_p0/partial_progress/107.pdf).

The full eight-page progress note was read in the preceding research and audit. Its fixed-priority assumption is not silently treated as an already proved all-strategic result. Its author's identity has not been verified; the repository name is not substituted for an individual author. The PDF is linked, not redistributed in this release package.

## Search coverage and retained evidence

The source audit checked the original paper, the full problem-107 progress note, targeted later papers, author publication listings, and the problem directory history. The checked GitHub branches were `main`, `rad`, `pete`, and `Pranav`. Main and rad contained the same partial-progress PDF; pete contained a problem record but no progress PDF; Pranav had no matching problem path. The recursive tree responses were not truncated. The checked repository endpoints returned zero issues, pull requests, and forks. These statements concern the inspected snapshot, not all GitHub content.

OpenAlex returned four citing records and Semantic Scholar ten, with version overlap. They were discovery aids, not a complete census or proof of priority. The existing alternative-model results were checked for applicability, rather than dismissed because their terminology differed.

| Audit item | Preserved material in `provenance/evidence/` |
| --- | --- |
| Four branches, SHAs and problem-path hits | `branches.json`, `branch107_summary.json` |
| Directory commit history | `commits107.json` |
| Issues, pull requests, forks | `issues.json`, `pulls.json`, `forks.json` |
| Repository README search | `repo_search.json`; a zero result is **not** a global code-search result |
| Citation discovery | `openalex_work.json`, `openalex_citing.json`, `semantic_citing.json`, `citation_lookup_summary.json` |
| Source problem and targeted sources | `problem107.json`, `source_manifest.json` |
| Public endpoint lookup scripts | `fetch_audit.py`, `fetch_citations.py`; these query live endpoints and may change, fail or be rate limited |

The raw tree responses are not duplicated here; the SHA-pinned filtered summaries retain all matching problem-107 paths. `source_manifest.json` is a historical internal audit manifest: some filenames refer to the earlier research archive, not to files in this release folder. Its research timing fields concern earlier runs only.

Related work screened includes [Seniorities and Minimal Clearing in Financial Network Games](https://arxiv.org/abs/2205.15628), [Computing Tarski Fixed Points in Financial Networks](https://doi.org/10.4230/LIPIcs.STACS.2026.14), [Dynamic Debt Swapping in Financial Networks](https://arxiv.org/abs/2302.11250), [Algorithms for Claims Trading](https://arxiv.org/abs/2402.13627), and [A Strategic Analysis of Prepayments in Financial Credit Networks](https://www.ijcai.org/proceedings/2024/0337.pdf). These targeted checks did not yield an earlier classification of the same ER-NE decision problem.

Access limitations were recorded rather than counted as negative results: global authenticated GitHub code search returned 401; the singleton-liability journal PDF could not be obtained (502, and an institutional conference PDF returned 403); the claims-trading full text inspected was the 2024 arXiv v1, not its 2026 journal version. Private, unpublished, unindexed, or missed results are not excluded. The audit supports a result-level novelty claim within the inspected sources; it does not certify absolute priority.

## AI assistance and responsibility

OpenAI's Codex assistant substantially assisted the mathematical derivation, source search and comparison, proof drafting and revision, code generation, finite checks, and preparation of this package. Successive proof audits in the recorded workflow were performed by the same assistant; no independent external referee review is claimed. The MILP check uses a different clearing algorithm but shares the graph generator with the exact checker.

The author is Zhiyan Lin, as supplied on 12 October 2026. No affiliation, ORCID, or repository URL has been supplied or invented. Publication and licensing decisions remain with the authors; this package was not uploaded to a public repository and no author was contacted.
