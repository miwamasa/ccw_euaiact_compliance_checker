# Decision Tree Optimization Paper

## Paper: Information-Theoretic Optimization of Regulatory Compliance Decision Trees

This paper presents the theoretical framework and practical results from optimizing the EU AI Act compliance checker.

## Files

| File | Description |
|------|-------------|
| `decision_tree_optimization.tex` | LaTeX source |
| `decision_tree_optimization.pdf` | Compiled PDF (after running make) |

## Requirements

To compile the LaTeX to PDF, you need:

- TeX Live (texlive-latex-base, texlive-latex-extra, texlive-fonts-recommended)
- Or MiKTeX on Windows
- Or MacTeX on macOS

## Compilation

### Linux/macOS
```bash
pdflatex decision_tree_optimization.tex
pdflatex decision_tree_optimization.tex  # Run twice for references
```

### Using Make
```bash
make
```

### Docker (if TeX not installed)
```bash
docker run --rm -v $(pwd):/work -w /work texlive/texlive pdflatex decision_tree_optimization.tex
```

## Paper Contents

1. **Introduction**: Motivation and contributions
2. **Theoretical Foundation**: Information theory basics, entropy, information gain
3. **Related Work**: C4.5, ID3, CART algorithms
4. **Optimization Techniques**: Early termination, question consolidation, lazy evaluation
5. **Case Study**: EU AI Act compliance checker (7,762 paths analyzed)
6. **Results**: 39% question reduction, 20-30% path length improvement
7. **Discussion**: Comparison with C4.5, limitations, generalizability
8. **Conclusion**: Key insights and future work

## Key Results

| Metric | Original | Optimized | Improvement |
|--------|----------|-----------|-------------|
| Total Questions | 33 | 20 | 39% |
| Avg Path Length | 8.6 | 6-7 | 20-30% |
| Question Efficiency Score | 0.91 | 1.30 | 43% |

## Citation

```bibtex
@article{euaiact_optimization_2026,
  title={Information-Theoretic Optimization of Regulatory Compliance Decision Trees},
  author={Decision Tree Optimization Research},
  journal={Technical Report},
  year={2026}
}
```
