# Reduced-XOR / Data-RO Direction Counterfactual Plan 2026-05-26

## Goal

验证 `sampler_island_local warmup10` 的 near-cutoff 行为是否真的由同一 `data_ro` 跨多个 sample line 的相关增强控制，而不是只来自单个 sampled bit marginal bias 或两路 RO hard locking。

核心反事实：

- 原始输出：`all64 = XOR(sampled_data[0..63])`
- data_ro 方向 reduced-XOR：`data_ro[j] = XOR(sampled_data[line][j], line=0..7)`
- line 方向 reduced-XOR：`line[i] = XOR(sampled_data[i][data_ro], data_ro=0..7)`
- data_ro complement：`except_data_ro[j] = all64 XOR data_ro[j]`

如果 `w10` 的偏置主要来自 same-data-RO 跨 line 相关结构，那么选择异常最强的 `data_ro` 方向 reduced-XOR 时，`w10` 应比 `w5/w11` 更偏；如果没有这个差异，则说明 snapshot 相关结构不一定控制最终 restart 输出，需要把机制进一步推向完整 FIFO/packing/时序链路。

## Implementation

新增 RTL：

- `rtl/entropy_source_reduced_probe.v`
- `rtl/restart/RO_TRNG_restart_reduced_xor_top.v`

设计原则：

- 保留原 restart auto-stream 状态机、UART、FIFO、header、row-major payload。
- 仍使用 `u_entropy_source` 实例名和原始 generate 名字，兼容 sampler-island XDC。
- 在 FPGA 中注册 `all64/data_ro/line` reduced bits 后送入 FIFO，避免只用 PC 端 snapshot 事后 XOR 带来的 cycle-alignment 歧义。
- `except_data_ro` 用来验证抵消链路：如果单个 `data_ro[j]` 强偏但 `except_data_ro[j]` 接近互补方向，最终 `all64` 可能仍接近理想；如果某个 warmup 窗口两者抵消变弱，则会形成 restart cutoff。
- header 仍保持 `A5 5A RESTART_COUNT ROW_BYTES 01 D0`，mode/index 由 bitstream 路径和 manifest 记录。

构建脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_restart_reduced_xor_20260526.ps1 `
  -VariantsCsv sampler_island_local `
  -WarmupsCsv 10 `
  -ModesCsv data_ro `
  -IndexesCsv 2
```

## First Smoke

第一优先级只做一个硬件 smoke：

- placement: `sampler_island_local`
- warmup: `10`
- mode: `data_ro`
- index: `2`
- restart matrix: `1000 x 125 bytes`
- capture bytes: `125008` including 8-byte header

选择 `data_ro2` 的原因：w10 snapshot 中 `line1/ro2` 是 worst sampled bit，且 data_ro-direction XOR 在事后诊断中表现出强偏置方向。

## Expansion Matrix

如果 `w10 data_ro2` smoke 成功且输出偏置明显，再扩展：

- warmup: `5,10,11`
- data_ro index: `0,2,5,6,7`
- optional line index: 先不跑，除非 data_ro 方向不能解释差异

最小投稿级判断：

- 若 `data_ro2` 在 w10 明显偏而 w5/w11 不偏：支持 same-data-RO cross-line correlation 控制 near-cutoff 输出。
- 若多个 data_ro 在 w10 偏而 w5/w11 不偏：支持 startup window 改变 data-RO direction correlation structure。
- 若 data_ro reduced-XOR 不分离，但 all64/restart 分离：说明最终偏置来自更高层组合、FIFO packing 或输出时序，不是单一 data_ro 方向。

## Postprocess

reduced-XOR payload 仍是 row-major restart byte matrix，因此可复用：

```powershell
python scripts\extract_restart_payload_with_header.py ...
python scripts\summarize_restart_formal_output_profile.py ...
python scripts\convert_restart_bytes_to_bits.py ...
powershell -ExecutionPolicy Bypass -File scripts\run_90b_restart.ps1 ...
```

后续可以补一个专用 summary 脚本，把 `variant,warmup,mode,index,p1,min_entropy,X_max,restart_status` 汇总成反事实表。
