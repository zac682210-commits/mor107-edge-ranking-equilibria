# Reproducing the supplementary checks

The proof in Sections 2–6 is analytic. These programs check finite instances of the construction. No proof-assistant verification or independent human audit is implied.

## Environment and commands

The release check used Python **3.12.14** on Linux. The two exact programs use only the standard library. The optional optimization check used NumPy **2.3.5** and SciPy **1.17.0**, with the HiGHS implementation bundled with SciPy (`scipy.optimize.milp`); there is no separately installed solver dependency. The exact seed and non-timing-result comparison are tied to the recorded environment; different Python versions can change pseudo-random sampling behavior.

From repository root:

```sh
python3 code/reproduce.py
# Optional numerical optimization check as well:
python3 code/reproduce.py --with-milp
```

The runner writes to `results/rerun/`, preserves the archived baseline in `results/`, and compares **every JSON field except `seconds`**. It exits unsuccessfully on a mismatch. Individual commands can also be run from any chosen output directory using an absolute path to the corresponding script. Do not run Python with `-O`, which disables assertions.

## Mapping from paper to output

| Claim in Appendix A | Program | Archived JSON field or calculation |
| --- | --- | --- |
| 16 alarm profiles | `code/verify107.py` | `verification107.json`: total lengths of `alarm["0"]` and `alarm["2"]` |
| 284 isolated threshold cases | `code/verify107.py` | `isolated_gate_cases` |
| 300 random quantified-CNF instances | `code/verify107.py` | length of `random_reductions.cases`; seed **107** |
| 3,600 normalized profiles | `code/verify107.py` | `random_reductions.normalized_profiles` |
| 57,504 gate-order comparisons | `code/verify107.py` | `random_reductions.gate_deviation_comparisons`; both normalized and unrestricted surrounding orders |
| 18 full unilateral-deviation checks | `code/verify107.py` | `random_reductions.full_pne_checks` |
| 50,688 complete profiles | `code/exhaustive107.py` | sum of `profiles` in `exhaustive107_results.json` |
| 49 different-algorithm checks | `code/independent_milp_check.py` | `independent_milp_results.json`: `count` and full `checks` array; seed **20261012** |

The three exhaustive instances and expected outputs are:

| Name | CNF formula | Profiles | Pure equilibria |
| --- | --- | ---: | ---: |
| `literal_y` | y | 4,608 | 0 |
| `contradiction_y` | y ∧ ¬y | 9,216 | 288 |
| `existential_switch` | x ∧ y | 36,864 | 144 |

All outgoing-edge permutations at every vertex are enumerated. JSON records the nontrivial players, their strategy counts, and all equilibrium profile indices. Enumeration is in the edge-insertion and `itertools.permutations` order of `code/verify107.py`. This makes the indices reconstructible rather than merely aggregate counts.

## What the checks establish

The exact evaluator starts at the capacity vector and iterates the greedy map downward. All values are integers, and a changing step decreases their sum. On termination the result is the greatest fixed point because each iterate dominates every fixed point. This routine is **pseudo-polynomial** in numeric capacities. The membership proof instead cites the original paper's strongly polynomial TopCycleIncrease algorithm.

The random instances have 0–3 existential variables, 1–3 universal variables and 1–6 clauses. Their full formula lists are saved. For each instance the code tests 12 normalized profiles, desired versus reversed gate orders in both normalized and unrestricted surroundings, and fanout reversals. Full equilibrium checks are performed on the selected true instances with at most two universal variables. These finite checks do not prove universal correctness.

The 49 optional checks comprise 3 feedback-margin examples, all 16 alarm profiles, and 30 full-graph profiles (15 normalized, 15 unrestricted). The MILP uses a separately written clearing formulation but **shares the graph generator**. It maximizes total edge flow over the disjunctive fixed-point constraints. The solver uses floating-point arithmetic; rounded solutions are checked against the greedy equations with exact integer arithmetic. This is not a formal optimality certificate, and it is not an independent implementation of the entire reduction.

## Release verification

`results/rerun/release_verification.json` records the fresh execution environment, timestamps and full non-timing comparisons. Associated `.log` files contain the program output. Timing is machine dependent. `MANIFEST.sha256` lists file hashes; regenerate it after authorized edits. The LaTeX source uses TeX Live packages `geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `enumitem`, `hyperref`, `tikz`, `microtype`, `needspace`, and `placeins`.
