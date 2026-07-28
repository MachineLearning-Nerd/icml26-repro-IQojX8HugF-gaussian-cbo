# Claim 5 method

`summarize_authored_2d.py` reads the four committed NPZ files directly,
requires every expected array and shape, rejects non-finite data, and recomputes
endpoint medians. The independent checker requires all A–D targets; a control
with D removed must fail.
