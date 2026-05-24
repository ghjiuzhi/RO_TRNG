# Byte-Aligned Restart Sampler Snapshot Summary cap1024 20260524

This is the byte-aligned version of the restart-aligned sampler snapshot. The formal restart design uses a 1-bit write / 8-bit read FIFO; therefore `WARMUP_BYTES=N` discards `8N` raw rand-clock bits. These rows use snapshot warmup bits 32/40/80/88 to match formal restart warmup bytes 4/5/10/11.

| formal warmup bytes | snapshot warmup bits | restart reference | seq ok | rand p1 | rand abs bias | rand min-H | stage_xor H | fixed sampled bits | heavy sampled bits | mean sampled abs bias | worst bit p1 | worst stage p1 |
| ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 32 | restart_fail_global_low | True | 0.470703125 | 0.029296875 | 0.917851 | 7.301296 | 15 | 42 | 0.416321 | 1.000000000 | 0.752929688 |
| 5 | 40 | restart_pass | True | 0.485351562 | 0.014648438 | 0.958341 | 6.642463 | 12 | 43 | 0.415527 | 0.000000000 | 0.071289062 |
| 10 | 80 | restart_pass | True | 0.465820312 | 0.034179688 | 0.904603 | 7.785172 | 0 | 17 | 0.320587 | 0.001953125 | 0.561523438 |
| 11 | 88 | restart_fail_global_high | True | 0.490234375 | 0.009765625 | 0.972094 | 7.758783 | 0 | 4 | 0.292953 | 0.021484375 | 0.541992188 |

## Interpretation

- formal warmup 4 bytes: rand p1=0.470703, stage_xor H=7.301, fixed sampled bits=15, heavy sampled bits=42, restart reference=restart_fail_global_low.
- formal warmup 5 bytes: rand p1=0.485352, stage_xor H=6.642, fixed sampled bits=12, heavy sampled bits=43, restart reference=restart_pass.
- formal warmup 10 bytes: rand p1=0.465820, stage_xor H=7.785, fixed sampled bits=0, heavy sampled bits=17, restart reference=restart_pass.
- formal warmup 11 bytes: rand p1=0.490234, stage_xor H=7.759, fixed sampled bits=0, heavy sampled bits=4, restart reference=restart_fail_global_high.

The byte-aligned diagnostic should be compared directly with the SP800-90B restart passband. If a formal-pass warmup still shows many fixed internal sampled bits, the paper claim should be more precise: the internal sampler state remains highly deterministic, but the emitted XOR/output bit may land in a locally balanced position. If fail warmups show biased emitted rand bits or lower stage-XOR entropy, that supports a startup output-position mechanism.
