# Random3 Restart Warmup Transition

| warmup bytes | overall p1 | positions over cutoff | worst x | MSB restart | LSB restart |
| ---: | ---: | ---: | ---: | --- | --- |
| 0 | 0.497933000 | 1 | 685 | unknown (Xmax=685) | unknown (Xmax=685) |
| 8 | 0.374385000 | 893 | 721 | failed (Xmax=721) | failed (Xmax=721) |
| 10 | 0.415017000 | 106 | 650 | failed (Xmax=650) | failed (Xmax=650) |
| 11 | 0.469088000 | 0 | 583 | passed (Xmax=583) | passed (Xmax=583) |
| 12 | 0.499478000 | 0 | 562 | passed (Xmax=562) | passed (Xmax=562) |
| 16 | 0.499126000 | 0 | 547 | passed (Xmax=549) | passed (Xmax=549) |

Interpretation: under this board, placement, and auto-stream restart protocol, warmup10 still fails while warmup11/12/16 pass. Treat this as a single-board transition result, not a final cross-PVT certification.