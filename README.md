# Gaussian CBO reproduction — IQojX8HugF

Reproduction of *Variational inference via Gaussian interacting particles in
the Bures--Wasserstein geometry* (arXiv:2601.00632v2).

The primary implementation is pinned at
`borghig/GaussCBO@ab76cce88c44f3d6bd368c76b5c095d115db8787` in
`repro/upstream/`. It is NumPy-only and the source-scale 2D protocol runs on
CPU: targets A--D, 100 independent runs per target, 20 particles, `T=10`, and
`dt=.05`.

## Reproduce the authors' protocol

```bash
source .venv/bin/activate
python repro/src/run_authored_2d.py --targets A --timeout 3600
python repro/src/run_authored_2d.py --targets B --timeout 3600
python repro/src/run_authored_2d.py --targets C --timeout 3600
python repro/src/run_authored_2d.py --targets D --timeout 3600
python repro/src/verify.py
```

The wrapper retains source notebook cells 0--5, which include the authors'
single-run and full repeated comparison. It changes only the documented target
selector in cell 5, then appends one I/O-only cell to retain the already-created
four trajectory matrices as a compressed raw artifact. It writes one completed
notebook and one raw `.npz` atomically per target. This avoids mixing the
separately scoped sensitivity sweeps into the claim-5 artifact while preserving
the released 100-run comparison unchanged.

## Evidence policy

The six active anchored claims are listed verbatim in
[`docs/CLAIMS_PINNED.md`](docs/CLAIMS_PINNED.md). The source labels its
mean-field convergence result *Theorem 3.5*, while the current anchored feed
calls it *Theorem 4.1*. The mismatch is retained in the evidence map; this
package will not represent the numbering as source-faithful.
