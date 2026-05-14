# RO-TRNG 的 SP800-90B Restart Dataset 采集协议

日期：2026-05-14

本文档面向后续实验执行者，说明如何为 RO-TRNG 补做 NIST SP 800-90B 所需的 restart dataset。目标是生成一个可被 `ea_restart` 直接读取、可复现、可审计的数据集，并在论文中清楚地区分它与现有连续采集数据的作用。

## 1. 目的

SP 800-90B 的 restart test 用来检查熵源在反复启动、复位、重新进入采样状态后，输出是否仍然满足预期随机性假设。它关注的是“启动后的同一位置样本”在大量独立重启之间是否存在偏置、固定模式或状态残留。

对 RO-TRNG 而言，restart dataset 主要回答以下问题：

- 每次 FPGA 配置或系统复位后，环振、采样触发、FIFO、串口输出链路是否会产生可重复的早期模式。
- 熵源启动瞬间是否受初始相位、复位释放时序、PLL/时钟稳定时间、采样控制状态机影响。
- 连续运行时通过的统计测试，是否掩盖了每次启动前若干 symbol 的弱随机性。

因此，restart dataset 不是为了替代普通长序列随机性测试，而是为了补充证明：该熵源在重复启动场景下也没有明显的启动偏差。

## 2. 为什么现有顺序 bin 不能替代 restart dataset

现有顺序 `.bin` 文件通常来自一次或少数几次连续运行，例如打开串口后连续读取若干 MB 数据。这类数据可以用于 IID/non-IID 熵估计、NIST STS、Dieharder、PractRand 或项目内部统计分析，但它不能替代 SP 800-90B restart dataset。

原因如下：

- 顺序 `.bin` 的相邻样本来自同一次运行，主要反映运行态随机性，而 restart test 需要比较“第 k 次 restart 后的第 j 个 symbol”。
- 连续数据中只有一次启动过程，最多包含一个启动瞬态；restart test 需要大量独立启动过程，例如 1000 次。
- 顺序 `.bin` 不能区分启动偏置和运行态偏置。例如前 10 个 symbol 若每次启动都趋同，连续长文件中该问题会被后续大量运行态数据稀释。
- `ea_restart` 需要二维矩阵语义：行代表 restart 次数，列代表每次 restart 后的 symbol 位置。普通顺序文件通常没有这种行列边界信息。

简言之：普通顺序 bin 证明“持续运行时像随机”，restart dataset 证明“每次重新启动后也像随机”。两者服务的问题不同，不能互相替代。

## 3. 建议采集矩阵

建议优先采用 NIST SP 800-90B restart test 常用规模：

- restart 次数：1000 次
- 每次 restart 后采集 symbol 数：1000 个
- 总 symbol 数：1,000,000 个
- 文件大小：1,000,000 字节
- symbol 定义：一字节一个 symbol，取值范围 0 到 255

若串口或人工复位成本较高，可先做小规模 smoke run：

- 10 restarts x 1000 symbols：验证脚本、文件格式、metadata 和 SHA256 流程。
- 100 restarts x 1000 symbols：检查是否存在明显流程问题。
- 1000 restarts x 1000 symbols：作为论文和正式 `ea_restart` 结果使用。

正式论文结果应以 1000 x 1000 为主。若最终规模不同，论文中必须明确写出 restart 次数、每次采样 symbol 数、symbol 位宽和原因。

## 4. 串口、bitstream 与复位策略

### 4.1 总原则

每一行数据必须对应一次独立 restart。每次 restart 后只保存该次 restart 的前 1000 个有效 symbol，并按顺序写入输出文件。

推荐将一次 restart 定义为以下任一方式，按实验条件选择并固定：

1. FPGA 重新配置 bitstream。
2. 板级硬复位或按键复位，使熵源、采样状态机、FIFO 和串口发送逻辑回到初始状态。
3. 设计内提供的全局同步复位，且已确认它覆盖 RO-TRNG 采样路径、后处理路径、FIFO/缓冲区和输出控制状态机。

不建议只关闭并重新打开串口作为 restart。串口重连通常只重置主机侧连接状态，不一定重置 FPGA 内部熵源和采样状态机。

### 4.2 Bitstream 策略

正式采集时应固定 bitstream：

- 使用同一个 `.bit` 文件完成全部 restart dataset 采集。
- 记录 bitstream 文件名、生成时间、Git commit 或工程版本。
- 记录 bitstream 的 SHA256。
- 不要在 1000 次 restart 中途更换 bitstream。

如果因实验原因更换 bitstream，应停止当前数据集，另起一个新的 dataset，并在 metadata 中明确区分。

### 4.3 复位策略

推荐策略从强到弱如下：

1. 重新配置 FPGA：最接近完整 restart，但耗时最长。
2. 板级全局复位：适合自动化和高重复次数。
3. 设计内全局复位：可用，但需要确认复位覆盖范围。

每次 restart 的建议流程：

1. 执行配置或复位。
2. 等待固定 settle time，例如 100 ms、500 ms 或 1 s。具体值应根据板卡和时钟稳定情况确定，并写入 metadata。
3. 清空主机串口缓冲区。
4. 开始读取。
5. 丢弃可选 warm-up symbol，若设计或评估策略要求。例如丢弃前 0、16、64 或 256 个 symbol。正式使用前必须固定该值。
6. 保存接下来的 1000 个 symbol。
7. 进入下一次 restart。

注意：如果论文要证明“启动早期也可用”，则不应丢弃 warm-up symbol，或至少同时报告不丢弃版本的结果。如果实际系统会在启动后丢弃前 N 个 symbol，则 restart dataset 应与实际系统策略一致，并在论文中说明。

### 4.4 串口策略

建议：

- 固定串口号、波特率、数据位、停止位、校验位和流控设置。
- 每次 restart 后清空主机端输入缓冲区，避免上一轮残留字节进入下一行。
- 每行必须采满 1000 个 symbol；不足则该行作废并重采。
- 若读取到协议头、计数器、换行符或调试文本，不得写入 restart dataset。
- 若硬件输出的是 bit 而不是 byte，应先定义如何打包为 symbol，并保持全数据集一致。

如果当前硬件输出已经是一字节随机 symbol，则最简单：串口每读取一个字节，就作为一个 symbol。

## 5. 文件格式

正式 restart dataset 使用原始二进制文件：

```text
文件名建议：restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.bin
总大小：1,000,000 bytes
编码：raw binary
symbol：uint8
矩阵布局：row-major
```

row-major 含义：

```text
第 0 行：restart 0 的 symbol 0..999
第 1 行：restart 1 的 symbol 0..999
...
第 999 行：restart 999 的 symbol 0..999
```

文件偏移计算：

```text
offset = restart_index * 1000 + symbol_index
```

例如：

- byte 0 是第 0 次 restart 后的第 0 个 symbol。
- byte 999 是第 0 次 restart 后的第 999 个 symbol。
- byte 1000 是第 1 次 restart 后的第 0 个 symbol。

不要在 `.bin` 文件中加入 CSV 分隔符、换行、文件头、JSON、时间戳或注释。所有说明信息放入单独的 metadata 文件。

## 6. Metadata 与 SHA256

每个正式 dataset 至少保存两个附属文件：

```text
restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.bin
restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.metadata.json
restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.sha256.txt
```

metadata 建议包含：

```json
{
  "dataset_type": "SP800-90B restart dataset",
  "date": "YYYY-MM-DD",
  "operator": "",
  "board": "",
  "fpga_part": "",
  "bitstream_path": "",
  "bitstream_sha256": "",
  "git_commit": "",
  "serial_port": "",
  "baud_rate": 0,
  "restart_method": "fpga_reconfiguration | board_reset | design_global_reset",
  "restart_count": 1000,
  "symbols_per_restart": 1000,
  "symbol_bits": 8,
  "symbol_format": "uint8 raw byte",
  "matrix_layout": "row-major",
  "settle_time_ms": 0,
  "warmup_symbols_discarded": 0,
  "host_os": "",
  "capture_script": "",
  "capture_script_sha256": "",
  "dataset_sha256": "",
  "notes": ""
}
```

Windows PowerShell 计算 SHA256 示例：

```powershell
Get-FileHash -Algorithm SHA256 .\restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.bin
Get-FileHash -Algorithm SHA256 .\design.bit
Get-FileHash -Algorithm SHA256 .\capture_restart.py
```

Linux 示例：

```bash
sha256sum restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.bin
sha256sum design.bit
sha256sum capture_restart.py
```

建议将 `.sha256.txt` 写成以下形式：

```text
<sha256>  restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.bin
<sha256>  design.bit
<sha256>  capture_restart.py
```

采集完成后必须检查：

- `.bin` 文件大小是否等于 `restart_count * symbols_per_restart`。
- metadata 中的矩阵参数是否与文件大小一致。
- SHA256 是否已记录。
- 是否保存了采集脚本版本和 bitstream 版本。

## 7. 如何运行 ea_restart

`ea_restart` 的具体命令取决于本地安装的 SP 800-90B EntropyAssessment 版本。正式运行前请先查看本机帮助：

```bash
ea_restart -h
```

或：

```bash
./ea_restart -h
```

运行时需要明确传入：

- 输入文件路径。
- symbol 位宽或 alphabet size。
- restart 次数。
- 每次 restart 的 symbol 数。
- 输入格式为二进制 raw byte。

可按本机帮助将参数替换为实际版本支持的形式。伪命令示例：

```bash
ea_restart restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.bin \
  --bits-per-symbol 8 \
  --rows 1000 \
  --cols 1000 \
  --binary
```

如果本地版本使用位置参数，则按 `ea_restart -h` 给出的顺序填写。不要仅复制本文伪命令而不核对帮助输出。

运行后保存：

```text
restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.ea_restart.stdout.txt
restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.ea_restart.stderr.txt
restart_ro_trng_1000x1000_YYYYMMDD_HHMMSS.ea_restart.version.txt
```

同时记录 EntropyAssessment 的版本、commit 或下载日期。若工具输出 pass/fail、行列测试统计量、最小熵估计或警告信息，应原样保存，并在论文中引用关键结果。

## 8. 论文中怎么表述

论文中建议将 restart dataset 放在“熵源评估”或“SP 800-90B 合规性补充实验”小节，而不是与普通连续流测试混为一谈。

可使用如下表述模板：

```text
To evaluate whether the RO-TRNG exhibits restart-dependent bias, we collected a restart dataset following the NIST SP 800-90B restart-test methodology. The dataset consists of 1000 independent restarts, and for each restart the first 1000 output symbols were recorded as 8-bit raw symbols. The resulting 1000 x 1000 matrix was stored in row-major order and evaluated using the EntropyAssessment ea_restart tool.
```

中文论文可写：

```text
为评估 RO-TRNG 在重复启动条件下是否存在启动相关偏置，本文按照 NIST SP 800-90B restart test 的数据组织方式采集 restart dataset。数据集包含 1000 次独立 restart，每次 restart 后记录 1000 个 8-bit 原始输出 symbol，形成 1000 x 1000 的矩阵，并以 row-major 顺序保存为原始二进制文件。随后使用 EntropyAssessment 工具中的 ea_restart 对该数据集进行评估。
```

如果采用 warm-up 丢弃策略，应补充：

```text
The first N symbols after each restart were discarded to match the operational start-up policy of the entropy source; the following 1000 symbols were used for the restart test.
```

如果未丢弃，应补充：

```text
No start-up symbols were discarded, so the dataset directly includes the earliest output symbols after each restart.
```

结果描述应包含：

- restart 方法：重新配置 FPGA、板级复位或设计内全局复位。
- restart 次数和每次 symbol 数。
- symbol 位宽和文件格式。
- 是否丢弃 warm-up symbols。
- `ea_restart` 版本。
- pass/fail 结果或工具报告的关键统计信息。
- 数据集 SHA256，便于复现实验。

避免过度表述。若只完成了 restart dataset 和 `ea_restart`，可以说“通过了 SP 800-90B restart test”，但不要说“完整通过 SP 800-90B 认证”。SP 800-90B 还涉及噪声源建模、IID/non-IID 路径、健康测试、restart 条件说明和实现层面的安全论证。

## 9. 最小执行清单

正式采集前：

- 固定 bitstream，并记录 SHA256。
- 固定 restart 方法。
- 固定 settle time。
- 固定是否丢弃 warm-up symbol。
- 固定串口参数。
- 确认采集脚本只写入 raw uint8 symbol。

采集时：

- 执行 1000 次 restart。
- 每次 restart 后保存 1000 个有效 symbol。
- 以 row-major 顺序写入一个 1,000,000 字节 `.bin` 文件。
- 若某次 restart 读取失败或字节数不足，重做该行，不要补零。

采集后：

- 检查文件大小。
- 计算 dataset、bitstream、采集脚本 SHA256。
- 填写 metadata。
- 保存 `ea_restart` 命令、版本、stdout 和 stderr。
- 在论文中明确说明 restart dataset 与普通连续 `.bin` 数据集不同。

