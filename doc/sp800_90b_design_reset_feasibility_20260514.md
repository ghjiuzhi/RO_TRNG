# SP800-90B Design-Level Restart 可行性 - 2026-05-14

更新时间：2026-05-14 19:08。

## 结论

当前 `RO_TRNG_top` 已经有 `por_n_i` 复位输入，但还不能直接把它当作严谨的 SP800-90B design-level restart 证据。

原因是：`por_n_i` 确实复位了 clock wizard、`proc_sys_reset_0` 和 UART TX，但当前 TRNG 数据路径里仍有两处关键问题：

- `entropy_source` 的 `.en` 固定为 `1'b1`，没有被 reset 控制，因此 RO 网络没有被显式停振/重启。
- `fifo_generator_0` 实例当前没有显式连接 reset 端口，restart 后 FIFO 内部状态是否被清空不能从顶层 RTL 直接证明。

因此，若要用 design-level reset 快速采集 1000x1000 restart dataset，需要先做一个小改版，而不是直接把串口重连或普通复位当作 restart。

## 当前 RTL 证据

`rtl\RO_TRNG_top.v` 中：

- 顶层存在 `por_n_i`。
- `clk_wiz_0.reset` 连接 `~por_n_i`。
- `proc_sys_reset_0.ext_reset_in` 连接 `~por_n_i`。
- `rst_n_200m` 连接到 `uart_tx.rst_n`。
- `entropy_source.en` 固定为 `1'b1`。
- FIFO 实例只连接了 `wr_clk`、`rd_clk`、`din`、`wr_en`、`rd_en`、`dout`、`full`、`empty`，没有显式 reset 连接。

`rtl\RO.v` 中：

- RO 的振荡由 `en` 控制。
- 如果 `en=0`，环路入口被门控；如果 `en=1`，RO 振荡。

这说明：加入 reset-controlled enable 是可行的，但当前工程还没这样做。

## 最小可审计改造方案

目标：让一次 host-triggered restart 在 RTL 上清楚覆盖熵源、FIFO 和 UART 输出状态。

建议新增一个 restart-capable 顶层，例如：

- `rtl\RO_TRNG_restart_top.v`
- 或在现有 `RO_TRNG_top.v` 上做一个分支版本，不覆盖已用于前面实验的 bitstream。

关键改动：

1. 新增一个可触发 restart 的输入。

   可选方式：

   - 板上按键或拨码开关连接到 `por_n_i`/`restart_n_i`。
   - 使用 PS GPIO 控制 PL reset。
   - 使用 UART RX 命令触发 restart 状态机。

2. 生成同步 reset。

   - 保留 `proc_sys_reset_0`。
   - 产生 `rst_n_200m` 给 UART、控制状态机、FIFO reset。

3. 控制 RO enable。

   - 将 `entropy_source.en` 从 `1'b1` 改为 `ro_en`。
   - restart 时 `ro_en=0` 保持若干 200 MHz 周期。
   - reset 释放后先让 `ro_en=1`，等待固定 settle 周期，再开始允许 FIFO 写入。

4. 清空 FIFO。

   - 重新定制或确认 `fifo_generator_0` 暴露 `rst`/`wr_rst`/`rd_rst`/`srst`。
   - restart 时 assert FIFO reset。
   - reset busy 结束后再允许写入。

5. 控制写入窗口。

   - `wr_en` 不再固定为 `1'b1`。
   - 改为 `wr_en = capture_en && !fifo_full`。
   - restart 释放后丢弃可配置 warm-up symbols，然后采集正式 1000 symbols。

6. 重置 UART TX。

   - 当前 `uart_tx` 已有 `rst_n`，应接同一个 restart reset。
   - reset 后先保持 TX idle，再从 FIFO 输出 row 数据。

## 对脚本的影响

如果 RTL 支持 host-triggered reset，则 `scripts/capture_90b_restart_dataset.ps1` 可以扩展第二种方法：

- `-RestartMethod design_reset_uart`
- 每行不再调用 Vivado program。
- 脚本发送 UART RX 命令或拉动某个控制引脚触发 restart。
- 等待固定 settle。
- 读取 1000 symbols。

这样 1000x1000 的总耗时会从约 46-50 小时下降到分钟级或十几分钟级，取决于 restart/settle/串口吞吐。

## 论文措辞边界

如果采用 reprogram-based restart：

- 优点：最接近完整 PL 重新启动，审稿解释最直接。
- 缺点：极慢，1000 行约 46-50 小时。

如果采用 design-level restart：

- 优点：快，适合完成正式 1000x1000。
- 缺点：论文中必须证明 reset 覆盖了熵源、FIFO、UART 与采样状态。不能只说“重新打开串口”。

当前状态建议写成：

```text
We implemented and smoke-tested the restart data acquisition protocol using FPGA reconfiguration as the restart method. The smoke run verified row-wise acquisition, metadata generation, and hash logging. A full 1000 x 1000 restart campaign remains future work unless a restart-capable RTL variant is used to reduce the per-row restart latency.
```
