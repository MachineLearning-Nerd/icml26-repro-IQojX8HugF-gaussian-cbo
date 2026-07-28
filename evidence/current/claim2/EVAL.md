# Claim 2 evaluation contract

Run through the inherited experiment command:

`uv run python repro/src/verify.py`

`verify.py` runs the historical cumulative checks, generates the full Claim 2
trajectories, and invokes the independent fail-closed checker. The Claim 2
verdict is accepted only when it is exactly `VERIFIED`; otherwise the process
exits nonzero.

The expected compute requirement is one CPU core and less than five minutes.
The run itself records the visible logical CPU allocation, the one-thread
limit, deterministic seeds, Python version, and measured runtime.
