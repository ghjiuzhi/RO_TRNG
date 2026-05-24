# Fast Mode 总状态 - 2026-05-14

更新时间：2026-05-14 17:49。

## 当前阶段

项目已经从“能不能采到数据”进入“证据链补强和论文可复现打包”阶段。

当前硬件短队列已经全部完成：

- 队列：`data/experiments/fast_mode/hardware_queue_short_20260514.csv`
- 状态文档：`doc/fast_mode_short_queue_status_20260514.md`
- 已完成：`random1_repeat03`、`random3_repeat03`、`random1_ro_freq_fixed_run04_5mib`、`random3_ro_freq_fixed_run04_5mib`

短队列已经结束，不需要再重跑整条 short queue。

## 已完成硬件证据

主 fast-mode 硬件队列已经完成，详见：

- `doc/fast_mode_hardware_status_20260513.md`
- `doc/fast_mode_tdc_pair_status_20260514.md`
- `data/experiments/tdc_pair_dynamics/tdc_pair_dynamics_20260514.md`

已经完成的数据类型：

- TRNG placement matrix：`compact`、`checker`、`sparse`、`far`、`same_column`、`cross_region`、`random1/2/3`、`row` 等。
- 原始 `fpga1` baseline：10 MiB formal 和 5 MiB repeat。
- RO_FREQ：`random1/random3` 多次 repeat。
- TDC near/far baseline。
- Pair-specific TDC：6 个重点 pair，全部完成。

6 个 pair-specific TDC：

- `random1_ro4_ro5`
- `random1_ro0_ro1`
- `random1_ro2_ro4`
- `random3_ro3_ro7`
- `random3_ro3_ro5`
- `random3_ro0_ro6`

## 主要结论边界

可以主张：

- 同一块 Zynq-7020 FPGA、同一 RO-TRNG 结构、同一 UART 采集链路下，placement 会显著改变原始随机性。
- `random1` 是稳定坏例：10 MiB formal 中 `p1 = 0.337315512`，快速 bit min-entropy 为 `0.593605945`。
- `random3` 是稳定好例：10 MiB formal 中 `p1 = 0.499968565`，快速 bit min-entropy 为 `0.999909299`。
- 原始 `fpga1` baseline 表现也较好：10 MiB `p1 = 0.500035894`，快速 bit min-entropy 为 `0.999896436`。
- TDC/RO_FREQ 可作为机制诊断工具，而不是只做黑盒随机性测试。

不能主张：

- 不能说已经证明“近距离 RO 必然强锁定”。
- 不能把未校准 TDC bin 当作绝对线性时间。
- 不能把单板、常温、默认电压结果直接推广到所有 FPGA/PVT 条件。
- 不能把 smoke 90B 或 STS 结果写成完整 SP800-90B 认证。

## TDC Pair 结果

当前 pair-specific TDC 是一个重要的负结果：

- pair runs：6
- total windows：96
- strong-lock windows：0
- max small-lag abs correlation：约 0.0318
- mean diff std：约 2040 ps 到 2043 ps

论文中应表述为：在当前观测方式和实验条件下，没有检测到强 pair-level phase locking。它不能证明完全没有耦合，也不能证明随机性差异来自单个近邻 pair 的强同步。

更稳妥的机制叙事是：placement 改变多 RO 网络的动态相互作用、频率接近程度、采样相位覆盖、局部布线延迟和序列相关结构。

## SP800-90B 当前进展

MinGW 路线已经跑通：

- build script：`scripts/build_90b_mingw.ps1`
- executables：`sim/SP800-90B_EntropyAssessment/cpp/ea_non_iid.exe`、`ea_iid.exe`、`ea_restart.exe`
- input preparation：`scripts/prepare_90b_inputs.py`
- smoke runner：`scripts/run_90b_smoke.ps1`
- result parser：`scripts/summarize_90b_results.py`
- summary：`data/sp800_90b/results_smoke_20260514/summary.md`
- status：`doc/sp800_90b_blocker_20260514.md`

已经完成 11 个布局的 1,000,000-symbol non-IID smoke，包含 MSB-first 和 LSB-first 两种 bit-order 敏感性检查。另对 `random1/random3/original` 做了 IID smoke 诊断，三个流都未通过 IID 路线的 LRS 检查，因此论文主线应使用 non-IID 估计。
核心 8M bit-symbol non-IID 也已补完：

- `random1_run01`：`H_original = 0.389520`
- `random3_run01`：`H_original = 0.902345`
- `original_fpga1_run01_10mib`：`H_original = 0.877727`

20 MiB repeat 已补完并分析：

- `random1_repeat03`：p1 仍偏置，90B repeat smoke MSB `0.390399`，LSB `0.390783`。
- `random3_repeat03`：20 MiB TRNG p1 `0.499915`，快速 bit min-entropy `0.999755`，90B repeat smoke MSB `0.856158`，LSB `0.894588`。

这进一步说明：坏 placement 和好 placement 的差异不是一次采集偶然，也不是 bit order 假象。
关键观察：

- `random1` 在 MSB/LSB 下都是明显低熵离群点：约 0.385/0.384。
- `random3`、`random2`、`compact`、`checker` 等在 MSB-first smoke 下约 0.86 到 0.87。
- `sparse`、`row` 较低，说明 placement 差异不仅表现为单比特偏置，也会被 90B non-IID 估计器捕捉。

仍然缺口：

- 这是 smoke，不是完整 formal 90B。
- `ea_restart.exe` 已经能编译，但还没有真正的 restart dataset；现有顺序 `.bin` 不能替代 restart 矩阵。
- 最终投稿前建议用更现代的 MSYS2/WSL 工具链复现 headline 结果。

Restart 执行更新：

- 新增 `scripts/capture_90b_restart_dataset.ps1` 和 `scripts/run_90b_restart.ps1`。
- 已完成 `random3` 的真实硬件 restart smoke：2 restarts x 16 symbols，SHA256 为 `29CE915227539459DEC278043F2A9E96A92D459FF175B6EDD5B3C0928DE532A9`。
- 已完成 `random3` 的 10x1000 restart pilot：10,000 bytes，SHA256 为 `65DB9381346C2CCB782DE4DD6425F80498A74F6C90437F10B751AA53D8E500AC`，0 次重试。
- 已完成 `random1` 的 10x1000 restart pilot：10,000 bytes，SHA256 为 `C96F94F6529ACD50A7E70D20154F4E25DDC111732BC066F4ACB05352A2FF3428`，0 次重试。
- 这些 restart smoke/pilot 只验证流程，不是正式 SP800-90B restart 结果。
- reprogram-based restart 在 `random3` 10x1000 pilot 中约 57.57 分钟，在 `random1` 10x1000 pilot 中约 42.33 分钟；按实测均值估算，正式 1000x1000 约需 70-96 小时。因此需要决定：安排约三到四天独占板子的正式 run，或先改 RTL 增加可审计 design-level reset。
- 详情见 `doc/sp800_90b_restart_execution_status_20260514.md`。

Restart fast-path 新进展：

- 已新增 restart-only auto-stream 顶层：`rtl/restart/RO_TRNG_restart_auto_top.v`
- 已新增对应 base XDC：`data/experiments/xdc_restart/restart_sysclk_base.xdc`
- 已新增 in-memory Vivado flow：`scripts/vivado/run_fpga1_ro_trng_restart_auto_inmem.tcl`
- 已扩展 `scripts/capture_90b_restart_dataset.ps1`，支持 `-RestartMethod auto_stream_once`
- 这条新路径的目标是：**每个 bitstream 只下载一次，然后板上自动输出完整 row-major restart 矩阵**
- 当前 `random3` 的小规模 build smoke 已成功产出 bitstream：`data\vivado_runs\restart_auto_random3_smoke\RO_TRNG_restart_auto_top.bit`
- 已完成真实硬件 auto-stream smoke：`random3_restart_auto_smoke_4x64_20260514.bin`，SHA256 为 `64C9A4405903F888115729018B532EE7B837E0F7AC72F73DB0FC89BFE070F340`
- 这证明 restart fast-path 已经从 RTL/脚本推进到真实板级链路，不再只是设计草图
- 详情见 `doc/restart_auto_stream_plan_20260514.md`

2026-05-15 更新：

- auto-stream formal-size 长流已经打通，不再停留在 smoke。
- `1000 x 1000` byte-symbol 真实硬件采集成功：
  - 文件：`data\hardware\20260511_fpga1_board1\restart\random3_restart_auto_formal_1000x1000_header_delay60s_20260515.bin`
  - header：`A55A03E803E801D0`
  - 大小：`1000000` bytes
  - SHA256：`7789491D1DFE5E3C21225F6574D3C00D85800258B4CE930C89545CD3BA59E3D6`
- bit-symbol formal restart 路线也已完成：
  - `1000 x 125` packed-byte 采集成功，展开为 `1000 x 1000` one-byte-per-bit symbols。
  - MSB 输入 SHA256：`8C927742F11564F08722BDCC09616A2A15619038E4AC362D0C327C5B81706726`
  - LSB 输入 SHA256：`25A3C2E95789FF3AB9A7B93EFE544B76C46068FC439B30ECDA6182E8641E07A4`
- `ea_restart` 已在 Windows/MinGW 下跑通，但 `random3` restart sanity check 未通过：
  - MSB：`H_I=0.902345`，`X_cutoff=605`，`X_max=685`，失败来源为 `column 7`。
  - LSB：`H_I=0.828444`，`X_cutoff=632`，`X_max=685`，失败来源为 `column 0`。
- 行列诊断显示所有 row 都未超阈值，失败由固定 column 偏置触发。这是重要机制证据：连续流 non-IID 高熵估计不能保证 restart 初期固定相位/固定输出位置稳定。
- 已补 `random1` 同协议 formal bit-symbol restart：
  - packed 输入 SHA256：`A9A4FFEAD5EA6CA15E74F13B3A068FFC59A156AEF28112F7D4B968E10470C512`
  - MSB bit-symbol SHA256：`20BA93F6C3330A3DF9167BB590209A3BEB7BD57A420E3EB2B9BCF1236D37DE16`
  - LSB bit-symbol SHA256：`6961FEA5A07AED881C91DEAB6C0BAB8A27451F84FFCC4DAE7086EF9239444314`
  - `ea_restart` 通过：MSB `H_I=0.389520`、`X_cutoff=821`、`X_max=680`；LSB `H_I=0.383737`、`X_cutoff=824`、`X_max=680`。
  - 但列诊断仍显示最坏原始位置为 `byte0 bit0`，`ones=320`，`zeros=680`。
- 已补 `random3` repeat02 formal bit-symbol restart：
  - packed 输入 SHA256：`7CE2161474009731EA7AC3C7ACBD7E38443DD55AC6881DAA5D2F2FAAB4D10ED5`
  - MSB bit-symbol SHA256：`FDE530F346A969CC9BF1469184CDB417879654F16DABCDC698AC17755F1224D5`
  - LSB bit-symbol SHA256：`78E5F2C380E7383214A26034EDC03245B6EE5EF0796A45202BC0B4922BA76AE4`
  - `ea_restart` 再次失败：MSB `X_cutoff=605`、`X_max=680`；LSB `X_cutoff=632`、`X_max=680`。
  - 最坏位置变为 `byte2 bit7`，`byte0 bit0` 仍超 MSB cutoff。机制表述应写成“restart 初期若干固定采样位置的偏置热点”，不要写成单一列绝对不变。
- 新增诊断脚本与表格：
  - `scripts/analyze_restart_matrix_columns.py`
  - `scripts/make_restart_mechanism_table.py`
  - `data\experiments\paper_artifacts_20260515\table_restart_mechanism_link.csv`
- 已补 `random3` warmup8 formal bit-symbol restart：
  - packed 文件：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup8_header_delay60s_20260515.bin`
  - header：`A55A03E8007D01D0`
  - packed 大小：`125000` bytes
  - packed SHA256：`4ECD7CCE25B950BE4F1B6715BD877B2D7A4CA1286D04B6B397D2BC0FB4357423`
  - MSB bit-symbol SHA256：`C99D78E132F6CF6C01A9E29D80A7705960B7BA2478B05F02AD292ACA1C13C8E2`
  - LSB bit-symbol SHA256：`20B43E5E28B65FFAED027F9931A212AC2A703A084E012C00A5A26CEA76532785`
  - `ea_restart` 仍失败：MSB `H_I=0.902345`、`X_cutoff=605`、`X_max=721`；LSB `H_I=0.828444`、`X_cutoff=632`、`X_max=721`。
  - 最坏位置为 `byte2 bit2`，`ones=279`，`zeros=721`，`p1=0.279`；MSB 展开后 `column 21`，LSB 展开后 `column 18`。
  - overall `p1=0.374385`，`positions_over_x_cutoff=893`。
- warmup8 的初步结论要谨慎：它不支持“简单丢弃最早 8 packed bytes 即可修复”的说法，反而提示 restart 后状态/相位窗口可能随 warmup 改变，并在新的窗口暴露更强偏置。
- 已补 `random3` warmup10 formal-size bit-symbol restart：
  - packed 文件：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup10_header_delay60s_20260515.bin`
  - header：`A55A03E8007D01D0`
  - packed 大小：`125000` bytes
  - packed SHA256：`90810C80B5936DF71B184D37E357E85FE05D33ED83CB0E5D0748906FF9BC6597`
  - MSB bit-symbol SHA256：`597D930EACFFEACD5E18662DD668379B354B598BAB6C366CE718FED57EC13658`
  - LSB bit-symbol SHA256：`65D98ED5D6B7F4E0DE0735D19559B7FB3C8A6C8817759452A5A197AB3102519D`
  - `ea_restart` 仍失败：MSB `H_I=0.902345`、`X_cutoff=605`、`X_max=650`；LSB `H_I=0.828444`、`X_cutoff=632`、`X_max=650`。
  - 列诊断：overall `p1=0.415017`，`positions_over_x_cutoff=106`；最坏位置为 `byte1 bit4`，`ones=350`，`zeros=650`，`p1=0.350`，`x=650`；MSB 展开后 `column 11`，LSB 展开后 `column 12`。
- 已补 `random3` warmup12 formal-size bit-symbol restart：
  - packed 文件：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup12_header_delay60s_20260515.bin`
  - header：`A55A03E8007D01D0`
  - packed 大小：`125000` bytes
  - packed SHA256：`E5F690CF5545F5EBF7271175472F2B2D36033E750C060F569B196CC08CB3B2C0`
  - MSB bit-symbol SHA256：`BDB6521AFF45F2FDC9F489CDB4AF2E4019E33241BA6D0EAE72CC20EE1FB6D297`
  - LSB bit-symbol SHA256：`E32B02B0E8ECA8FB0CF31B6803F3B4E545279640E35D30B2E2BB08FD2F22D299`
  - `ea_restart` 通过：MSB `H_I=0.902345`、`X_cutoff=605`、`X_max=562`、`H_r=0.867146`、`H_c=0.849807`、`min=0.849807`；LSB `H_I=0.828444`、`X_cutoff=632`、`X_max=562`、`H_r=0.866043`、`H_c=0.836130`、`min=0.828444`。
  - 列诊断：overall `p1=0.499478`，`positions_over_x_cutoff=0`；最坏位置为 `byte88 bit3`，`ones=562`，`zeros=438`，`p1=0.562`，`x=562`；MSB 展开后 `column 708`，LSB 展开后 `column 707`。
- 已补 `random3` warmup16 formal-size bit-symbol restart：
  - packed 文件：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup16_header_delay60s_20260515.bin`
  - header：`A55A03E8007D01D0`
  - packed 大小：`125000` bytes
  - packed SHA256：`8084E1AB95062564ACE582113520A54163CADA96E12C1A2211DE2C044AC860E7`
  - MSB bit-symbol SHA256：`16776DFF817D178B05C8479C634469C55B130740F7719412A5D0257DBD384D0B`
  - LSB bit-symbol SHA256：`EFF66AE869332A04F38FE3F1FB93DCE1D398ACAEC57C6126CFDECBA0AF3DD1B5`
  - `ea_restart` 通过：MSB `H_I=0.902345`、`X_cutoff=605`、`X_max=549`、`H_r=0.871037`、`H_c=0.868735`、`min=0.868735`；LSB `H_I=0.828444`、`X_cutoff=632`、`X_max=549`、`H_r=0.820090`、`H_c=0.830192`、`min=0.820090`。
  - 列诊断：overall `p1=0.499126`，`positions_over_x_cutoff=0`；最坏位置为 `byte43 bit7`，`ones=547`，`zeros=453`，`p1=0.547`，`x=547`；MSB 展开后 `column 344`，LSB 展开后 `column 351`。
- 已补 `random3` warmup11 formal-size bit-symbol restart：
  - packed 文件：`data/hardware/20260511_fpga1_board1/restart/random3_restart_auto_formal_bits_1000x125_warmup11_header_delay60s_20260515.bin`
  - header：`A55A03E8007D01D0`
  - packed 大小：`125000` bytes
  - packed SHA256：`4418C3D6550684637B56121F96A906F48B128B63139991A3B8C827D2C30A6BA9`
  - MSB bit-symbol SHA256：`4EBF7244063138838227327180911E4F2F69D4D30299A8D9D5875810ECF7E5A1`
  - LSB bit-symbol SHA256：`573A87D6E22F0B14485AD3657BB9E0C4A2C9B4FB3AD499065100F9E0AD248E33`
  - `ea_restart` 通过：MSB `H_I=0.902345`、`X_cutoff=605`、`X_max=583`、`H_r=0.743385`、`H_c=0.756293`、`min=0.743385`；LSB `H_I=0.828444`、`X_cutoff=632`、`X_max=583`、`H_r=0.753865`、`H_c=0.759525`、`min=0.753865`。
  - 列诊断：overall `p1=0.469088`，`positions_over_x_cutoff=0`；最坏位置为 `byte1 bit3`，`ones=417`，`zeros=583`，`p1=0.417`，`x=583`；MSB 展开后 `column 12`，LSB 展开后 `column 11`。
- 当前 warmup 扫描结论：warmup0/8/10 失败、warmup11/12/16 通过，说明 restart 初期至少前若干 packed bytes 属于不稳定/偏置窗口，存在可通过 sufficient warmup 消除的相变。阈值目前在本板、本 placement、本 auto-stream restart 协议下收窄为 `10 < WARMUP_BYTES <= 11`。该结论只覆盖本板、本 placement 的 formal-size restart 结果，不应写成最终认证。
- 论文用汇总表已刷新：`data/experiments/paper_artifacts_20260515/table_restart_mechanism_link.csv` 和 `data/experiments/paper_artifacts_20260515/table_restart_warmup_transition.csv`。
- 已完成 `random3` warmup boundary repeat02 硬件补采：
  - 覆盖 `WARMUP_BYTES=10,11,12`，每档 `1000 x 125` packed bytes，展开为 `1000 x 1000` bit symbols。
  - repeat02 结果复现第一轮边界：warmup10 仍失败，MSB/LSB `X_max=633`；warmup11 通过，MSB/LSB `X_max=588`；warmup12 通过，MSB/LSB `X_max=556`。
  - 这把论文表述从“单次观察”加强为“两次边界重复观察”：本板、本 placement、本 auto-stream restart 协议下，观察到的通过边界仍为 `10 < WARMUP_BYTES <= 11`。
  - 新增/刷新产物：`doc/restart_warmup_repeat02_status_20260515.md`、`data/experiments/paper_artifacts_20260515/table_restart_warmup_transition_with_repeats.csv`、`data/experiments/paper_artifacts_20260515/fig_restart_warmup_transition.png`。
  - 当前没有 Vivado/program/capture/ea_restart 硬件任务在跑，只有常驻 `hw_server`。

## 短队列收尾

短队列已经全部完成，不再需要重跑。

## 下一步优先级

P0：持续更新 GitHub export，给 GPT/Claude 分析使用，但不上传大体积原始 `.bin`、`.bit`、`.dcp`。
P0：把 SP800-90B smoke 结果纳入论文证据表，措辞为“non-IID smoke supports the placement-dependent gap”，不要写成认证。
P1：设计 restart capture protocol。现有顺序流不能直接冒充 restart dataset。
P1：如果冲更高水平，后续补多板、温度/电压/运行时间漂移；如果做不到，写成 limitation 和 future validation。

## 2026-05-23 机制假设更新

- 已完成 `random1` sampler-island 20MiB programmed confirmation：
  - 文件：`data/hardware/20260511_fpga1_board1/trng/random1_sampler_island_local_x45y39_regs_x45y31_program_20mib_20260523.bin`
  - SHA256：`C42E39A9BC46909105678F20EE918D054C82564FA344FA2F8E1A761D0E0D95E4`
  - `p1=0.5000507474`
  - bit min-entropy `0.9998535814`
  - runs p-value `0.6489840131`
  - adjacent-equal ratio `0.4999824375`
  - XADC：`46.0 C -> 46.3 C`，`VCCINT=1.000 V`，`VCCAUX=1.796 V -> 1.794 V`
- 结论：这把 sampler-island 修复从 5MiB smoke 提升为 20MiB 稳定证据。保持 `random1` data RO placement 不变，仅改变 sampler-side placement，就能把强偏置源修复到近理想连续流。
- 已新增 TDC 机制实验计划与准备文件：
  - `doc/tdc_sampler_mechanism_experiment_plan_20260523.md`
  - `scripts/generate_tdc_sampler_data_xdc.py`
  - `scripts/build_tdc_sampler_data_bitstreams.ps1`
  - `data/experiments/fast_mode/hardware_queue_tdc_sampler_data_20260523.csv`
- 当前 TDC 策略：不再盲目重复 data-data pair TDC；下一步优先 sampler-data TDC，用来验证 sampler-data 相位结构是否跟 TRNG 修复同步变化。
- 当日状态详见：`doc/fast_mode_status_20260523.md`。
