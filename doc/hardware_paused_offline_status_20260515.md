# Hardware Paused / Offline Progress Status - 2026-05-15

## Current State

Hardware-connected work is paused because the board is not available right now. No COM3, JTAG, Vivado programming, or capture job should be started until you explicitly reconnect hardware.

The last completed hardware evidence chain remains valid:
- fast-mode queue: completed
- TDC pair captures: completed
- restart warmup repeat02: completed
- restart warmup boundary repeat02: completed

## What Was Just Finished Offline

1. I verified there are no active hardware capture/programming jobs from the RO_TRNG workspace.
2. I checked the repeat02 warmup evidence chain and confirmed it is internally consistent.
3. I created and closed delegated analysis tasks for:
   - offline data consistency audit
   - restart warmup paper-section draft
   - GitHub / GPT / Claude export plan
4. I fixed `scripts/run_restart_warmup_repeat_queue.ps1` so a capture failure now stops post-processing cleanly instead of cascading into missing-file errors.
5. I fixed `scripts/make_restart_mechanism_table.py` so it now auto-discovers existing restart summary files instead of writing an empty table.
6. I refreshed the restart mechanism table and warmup transition figure from the current CSV sources.

## Current Best Paper Narrative

- Placement changes raw TRNG quality strongly.
- TDC pair captures are useful as mechanism evidence, but the current six pair-specific runs do not show conservative strong-lock windows.
- Restart warmup evidence is now the strongest transient-window result:
  - warmup10 fails
  - warmup11 passes
  - warmup12 passes
  - repeat02 reproduces the same boundary

## Immediate Offline Next Steps

- Keep preparing the export package for external model review.
- Make sure the exported package contains the repaired restart mechanism table and the clean warmup-transition figure.
- If hardware becomes available again, the next highest-value experiments remain pair-specific TDC expansions and any new restart contrast that tightens the mechanism story.

## Guardrail

Do not start a new hardware queue until hardware is explicitly available again.
