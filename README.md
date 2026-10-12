# Pure Nash Equilibrium Existence in Edge-Ranking Flow Allocation Games is Σ₂ᵖ-Complete

**Author:** Zhiyan Lin

📄 **[Read the paper](paper.pdf)**

**Main result.** Pure Nash equilibrium existence in edge-ranking flow allocation games is Σ₂ᵖ-complete under greatest-fixed-point clearing, with every vertex strategic.

The paper proves that pure Nash equilibrium existence in the original edge-ranking flow allocation model is Σ₂ᵖ-complete. Every vertex is strategic, utility is total outgoing flow, and clearing selects the coordinatewise greatest fixed point. Hardness holds on simple directed graphs with polynomially bounded integral capacities and supplies.

The contribution is a strict-dominance guarantee for lossy threshold gates that remains valid under surrounding feedback, and its use to complete an existing guarded quantified-Boolean reduction. The reduction architecture and the basic lossy-return threshold idea are prior work; see the introduction and [PROVENANCE.md](PROVENANCE.md).

## Read and reproduce

- [paper.pdf](paper.pdf): analytic proof, with supplementary computation in Appendix A.
- [src/paper.tex](src/paper.tex): self-contained LaTeX source, including both figures.
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md): commands, dependencies, seeds, and the mapping from every reported count to its source.
- [code/](code/): construction, exact checks, exhaustive enumeration, and optional MILP cross-check.
- [results/](results/): archived outputs and a fresh release-verification run.
- [PROVENANCE.md](PROVENANCE.md): prior contributions, pinned sources, search coverage, and AI assistance.
- [CITATION.cff](CITATION.cff): citation metadata with the preprint as the preferred citation.

Run the standard-library checks from this directory:

```sh
python3 code/reproduce.py
```

To include the numerical MILP cross-check, install the optional dependencies in an environment of your choice and run:

```sh
python3 -m pip install -r requirements-milp.txt
python3 code/reproduce.py --with-milp
```

Compile the paper:

```sh
cd src
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
cp paper.pdf ../paper.pdf
```

## Before public release

Confirm the intended public license; none has been selected on behalf of an author. This package does not rehost third-party paper PDFs. Source links and public metadata snapshots are included for traceability.

No claim of absolute priority is made. The mathematical claim is the theorem stated in the paper; finite checks are supporting implementation evidence.
