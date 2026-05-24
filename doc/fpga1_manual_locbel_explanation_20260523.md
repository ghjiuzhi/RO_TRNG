# fpga1 手工物理布局约束说明

本文档用于说明 `RO_TRNG` 工程从原 `fpga` 工程迁移到 `fpga1` 后，RO-TRNG 熵源部分为什么要做手工物理约束，以及 `LOC`、`BEL` 约束具体是什么意思。

相关文件：

- `E:\Project\MLDSA\RO_TRNG\fpga1\xc7z020clg400\xc7z020clg400.srcs\constrs_1\new\manual_ro_locbel_round1.xdc`
- `E:\Project\MLDSA\RO_TRNG\fpga1\xc7z020clg400\xc7z020clg400.srcs\constrs_1\new\pin.xdc`
- `E:\Project\MLDSA\RO_TRNG\fpga1\xc7z020clg400\xc7z020clg400.srcs\constrs_1\imports\new\timing.xdc`
- `E:\Project\MLDSA\RO_TRNG\rtl\entropy_source.v`

## 1. 为什么 RO-TRNG 需要手工物理约束

普通同步数字电路通常只需要保证逻辑功能正确、时序收敛即可。RTL 写好以后，Vivado 可以自动决定 LUT、FF 放在哪里，也可以自动完成布线。

但 RO-TRNG 的熵源不是普通同步逻辑。它依赖环形振荡器的实际物理延迟产生不确定性。影响随机性的因素包括：

- LUT 本身的延迟；
- LUT 到 LUT 的反馈路径延迟；
- 不同 RO 之间的物理距离；
- 采样寄存器与 RO 输出之间的布线延迟；
- 采样环的振荡频率和相位关系；
- 工艺、电压、温度以及板级环境噪声。

因此，对 RO-TRNG 来说，RTL 只是定义了振荡器和采样结构，真正落到 FPGA 后的物理位置会直接影响输出数据质量。

如果完全交给 Vivado 自动布局，每次重新实现时可能出现：

- RO 被放到不同 Slice；
- 同一个 RO 内的 LUT 被放到不同 BEL；
- 采样寄存器离 RO 更近或更远；
- 最终输出异或逻辑分散到不同区域；
- 随机数 0/1 比例、熵估计和测试结果发生变化。

所以迁移到 `fpga1` 后，关键工作之一就是重新在 ZYNQ-7020 器件上固定熵源关键逻辑的位置，提高工程复现性。

## 2. LOC 和 BEL 分别是什么意思

`LOC` 和 `BEL` 都是 Xilinx XDC 物理约束，但控制粒度不同。

### 2.1 LOC

`LOC` 指定 cell 放到 FPGA 芯片上的哪个物理 Slice。

示例：

```tcl
set_property LOC SLICE_X44Y43 [get_cells ...]
```

含义是：把目标 cell 固定到 `SLICE_X44Y43` 这个 Slice。

`SLICE_X44Y43` 可以理解为 ZYNQ-7020 芯片上一块具体的逻辑资源位置，其中包含多个 LUT 和多个 FF。

### 2.2 BEL

`BEL` 指定 cell 在这个 Slice 内部使用哪个具体基本资源。

示例：

```tcl
set_property BEL A6LUT [get_cells ...]
```

含义是：目标 LUT 必须使用该 Slice 内部的 `A6LUT`。

常见 LUT BEL 包括：

- `A6LUT`
- `B6LUT`
- `C6LUT`
- `D6LUT`

常见 FF BEL 包括：

- `AFF`
- `BFF`
- `CFF`
- `DFF`
- `A5FF`
- `B5FF`
- `C5FF`
- `D5FF`

### 2.3 为什么 LOC 和 BEL 要一起用

如果只使用 `LOC`，Vivado 只知道某个逻辑必须放进某个 Slice，但仍然可以在 Slice 内部自行选择 `A6LUT`、`B6LUT`、`C6LUT` 或 `D6LUT`。

如果同时使用 `LOC` 和 `BEL`，就可以进一步固定：

```text
这个 LUT 放到哪个 Slice；
并且放到这个 Slice 内部的哪个 LUT 位置。
```

所以 `LOC + BEL` 的约束粒度比普通区域约束更细。

## 3. 这个工程里手工约束了哪些逻辑

`manual_ro_locbel_round1.xdc` 主要固定了四类逻辑：

1. 8 个熵源 RO 本体；
2. 64 个 `sampled_data` 采样寄存器；
3. 采样环 `RO_SAMPLE_NAND` 和 `RO_SAMPLE_LOOP`；
4. 最终 `rand_bit` 输出异或逻辑和输出寄存器。

也就是说，这个 XDC 不是只固定几个 RO，而是在 ZYNQ-7020 上固定了一整块熵源关键物理区域。

## 4. 8 个 RO 本体是怎么放的

在 `entropy_source.v` 中，熵源参数为：

```verilog
.RO_NUM(8)
.RO_STAGES(2)
.SAMPLE_STAGES(9)
```

因此当前熵源中有 8 个数据 RO。每个 RO 的主环由两级 LUT 构成：

```text
第一级：LUT6_and2_1，带使能和反馈输入；
第二级：LUT6_not1，反相级；
反馈：第二级输出回到第一级输入。
```

以 RO0 为例，XDC 中的约束形式为：

```tcl
set_property LOC SLICE_X44Y43 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]
set_property BEL A6LUT        [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_AND.u_LUT6_and2_1/u_LUT6}]

set_property LOC SLICE_X44Y43 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
set_property BEL B6LUT        [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_NUM_LOOP[0].RO_STAGE_LOOP[0].u_LUT6_not1/u_LUT6}]
```

含义是：

```text
RO0 第一级 LUT  -> SLICE_X44Y43 / A6LUT
RO0 第二级 LUT  -> SLICE_X44Y43 / B6LUT
```

也就是把 RO0 的两个关键 LUT 压在同一个 Slice 内部，并指定它们分别使用 `A6LUT` 和 `B6LUT`。

8 个 RO 的整体放置方式如下：

```text
       X44          X45          X46          X47
Y44    RO4          RO5          RO6          RO7
Y43    RO0          RO1          RO2          RO3
```

对应 Slice 为：

| RO | Slice | 第一级 BEL | 第二级 BEL |
|---|---|---|---|
| RO0 | `SLICE_X44Y43` | `A6LUT` | `B6LUT` |
| RO1 | `SLICE_X45Y43` | `A6LUT` | `B6LUT` |
| RO2 | `SLICE_X46Y43` | `A6LUT` | `B6LUT` |
| RO3 | `SLICE_X47Y43` | `A6LUT` | `B6LUT` |
| RO4 | `SLICE_X44Y44` | `A6LUT` | `B6LUT` |
| RO5 | `SLICE_X45Y44` | `A6LUT` | `B6LUT` |
| RO6 | `SLICE_X46Y44` | `A6LUT` | `B6LUT` |
| RO7 | `SLICE_X47Y44` | `A6LUT` | `B6LUT` |

这种放置方式属于紧凑布局。它的目的不是让 Vivado 随机摆放 RO，而是人为规定 RO 在芯片中的局部空间关系。

## 5. 为什么同一个 RO 的两个 LUT 要放到同一个 Slice

RO 的振荡频率由环路延迟决定。如果第一级 LUT 和第二级 LUT 被 Vivado 放得很远，反馈路径就会变长，振荡频率和抖动表现也会改变。

把同一个 RO 的两个 LUT 固定到同一个 Slice 内，可以带来三个好处：

1. 单个 RO 内部反馈路径更短；
2. 同类 RO 的物理结构更一致；
3. 重新实现时 RO 的主要物理结构不容易漂移。

这对 RO-TRNG 很重要，因为随机性实验需要尽量区分“设计变量”与“工具随机摆放造成的变化”。

## 6. 采样寄存器为什么也要固定

在 `entropy_source.v` 中，采样逻辑为：

```verilog
for (i = 0; i < SAMPLE_STAGES-1; i = i + 1) begin : SAMPLE_DATA_LINE_LOOP
    for (j = 0; j < RO_NUM; j = j + 1) begin : SAMPLE_DATA_BIT_LOOP
        always @(posedge ro_sample_chain[i]) begin
            sampled_data[i*RO_NUM+j] <= ro_chain[j][RO_STAGES-1];
        end
    end
end
```

当前参数下：

```text
(SAMPLE_STAGES - 1) * RO_NUM = 8 * 8 = 64
```

所以会综合出 `sampled_data_reg[0]` 到 `sampled_data_reg[63]`，共 64 个采样寄存器。

这些寄存器负责在采样环的不同节点上采样 8 个 RO 的输出。最终 64 bit 采样数据通过异或压缩成一个随机位：

```verilog
rand_bit <= ^sampled_data;
```

如果采样寄存器完全由 Vivado 自动放置，RO 输出到寄存器 D 输入之间的路径会不可控，采样关系也会变化。因此工程中也对这些 FF 做了 `LOC + BEL` 约束。

示例：

```tcl
set_property LOC SLICE_X47Y43 [get_cells -hierarchical -filter {NAME =~ *sampled_data_reg[0]}]
set_property BEL AFF          [get_cells -hierarchical -filter {NAME =~ *sampled_data_reg[0]}]
```

含义是：

```text
sampled_data_reg[0] -> SLICE_X47Y43 / AFF
```

采样寄存器数量较多，所以它们不是像 8 个 RO 那样简单排成 4 x 2，而是围绕熵源区域放置到附近多个 Slice 的 FF 资源中。

## 7. 采样环为什么也要固定

熵源中除了 8 个数据 RO，还有一个采样环 `ro_sample_chain`。

当前 `SAMPLE_STAGES = 9`，因此采样环由以下部分构成：

- 1 个 `RO_SAMPLE_NAND`；
- 8 个 `RO_SAMPLE_LOOP[i].u_LUT6_not1`。

采样环的节点用于触发采样寄存器：

```verilog
always @(posedge ro_sample_chain[i])
```

最后一级还通过 BUFG 输出为 `clk_o`，也就是顶层里的 `rand_clk`：

```verilog
BUFG u_BUFG (
    .O(clk_o),
    .I(ro_sample_chain[SAMPLE_STAGES-1])
);
```

所以采样环会影响：

- 采样相位；
- 采样速率；
- FIFO 写时钟；
- 输出随机位节奏。

因此 `manual_ro_locbel_round1.xdc` 也对采样环 LUT 进行了物理定位。

示例：

```tcl
set_property LOC SLICE_X49Y45 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
set_property BEL B6LUT        [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/RO_SAMPLE_NAND.u_LUT6_nand2_1/u_LUT6}]
```

含义是：

```text
采样环 NAND LUT -> SLICE_X49Y45 / B6LUT
```

## 8. 为什么最终 rand_bit 逻辑也要固定

RTL 中最终随机位写法很简单：

```verilog
rand_bit <= ^sampled_data;
```

但 64 bit 的归约异或综合到 FPGA 上以后，会形成多级 LUT 网络。综合后的 cell 名称通常类似：

```text
rand_bit_i_1
rand_bit_i_2
...
rand_bit_i_13
rand_bit_reg
```

这些逻辑是熵源输出路径的一部分。如果完全自动放置，异或树可能被分散到较远位置。

所以工程中也对它们做了物理定位，例如：

```tcl
set_property LOC SLICE_X49Y43 [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/rand_bit_reg}]
set_property BEL AFF          [get_cells -hierarchical -filter {NAME =~ *u_entropy_source/rand_bit_reg}]
```

这样可以让最终输出逻辑也保持在熵源区域附近。

## 9. 这个 XDC 实际构建的是一块熵源物理区域

可以把 `manual_ro_locbel_round1.xdc` 理解成在 ZYNQ-7020 上手工构建一块熵源物理区域：

```text
熵源物理区域
├── 8 个数据 RO
│   ├── 每个 RO 的 AND/NAND LUT
│   └── 每个 RO 的 NOT LUT
├── 采样环
│   ├── RO_SAMPLE_NAND
│   └── RO_SAMPLE_LOOP[0..7]
├── 64 个 sampled_data 采样寄存器
└── rand_bit 异或压缩逻辑和输出寄存器
```

这比普通的区域约束更细。普通 Pblock 只是告诉 Vivado“这些逻辑大致放在某块区域”，但 `LOC + BEL` 是告诉 Vivado“这个 cell 必须放到这个 Slice 的这个具体资源上”。

## 10. 这部分是怎么做出来的

实际工作流程可以概括为：

1. 先读懂 RTL 层次结构，确认熵源实例名是 `u_entropy_source`；
2. 根据 `RO_NUM_LOOP[i]` 找到每个 RO 的 LUT cell；
3. 在 ZYNQ-7020 器件上选择一片合适的 Slice 区域；
4. 用 `LOC` 把每个 RO 放到具体 Slice；
5. 用 `BEL` 把每个 RO 内部 LUT 放到具体 LUT 资源；
6. 继续约束采样寄存器、采样环和输出异或逻辑；
7. 运行综合与实现；
8. 打开 implemented design，在 Device 视图中检查 cell 的 `LOC` 和 `BEL` 是否符合预期；
9. 如果出现资源冲突或放置失败，再调整 XDC。

常见错误包括：

- 两个 cell 被约束到同一个 BEL；
- LUT cell 被放到不兼容的 BEL；
- Slice 内 FF 或 LUT 资源不够；
- 综合后 cell 名称与 XDC 中的 `get_cells` 匹配不上。

## 11. 对迁移的意义

原 `fpga` 工程面向 KU5P，原来的 Slice 坐标和 BEL 资源对应 KU 器件。迁移到 `fpga1` 后目标器件变为 ZYNQ-7020，原坐标不能直接照搬。

因此迁移的关键不是简单复制旧 XDC，而是：

1. 保留原工程“需要固定熵源关键逻辑”的设计思想；
2. 在新器件上重新选择物理区域；
3. 按新器件资源结构重新写 `LOC + BEL`；
4. 通过 Vivado 实现结果确认约束生效。

也就是说，迁移过程既包括 RTL 和 IP 适配，也包括熵源物理结构在新器件上的重建。

## 12. 对复现和实验的意义

这些手工约束让工程复现不只是“源码一致”，还包括“关键熵源物理布局尽可能一致”。

这对 RO-TRNG 很重要，因为不同物理布局会影响：

- RO 频率；
- RO 之间的耦合关系；
- 采样关系；
- 输出 bit 的 0/1 比例；
- 熵估计；
- 随机性测试表现。

工程中还存在用于生成不同布局方案的脚本，例如：

- `E:\Project\MLDSA\RO_TRNG\scripts\generate_ro_placement_xdc.py`
- `E:\Project\MLDSA\RO_TRNG\scripts\generate_fpga1_experiment_matrix.py`

这些脚本支持 `compact`、`row`、`same_column`、`checker`、`sparse`、`cross_region`、`far`、`random` 等布局模式，说明物理布局本身也是实验变量。

## 13. 需要说明的边界

当前工程中能确认的是：关键熵源逻辑做了手工布局约束。

也就是：

- 用 `LOC` 固定 Slice；
- 用 `BEL` 固定 Slice 内部 LUT 或 FF；
- 固定 RO、采样寄存器、采样环、输出逻辑的位置。

但目前没有看到针对每条 net 的固定路由约束，例如完整的 `FIXED_ROUTE` 或逐 PIP 约束。因此更准确的说法是：

```text
本工程对 RO-TRNG 熵源关键逻辑进行了手工物理布局；
布线由 Vivado 在这些布局约束下自动完成。
```

不要说成：

```text
所有线都是手工布线。
```

## 14. 视频讲解推荐话术

可以在录屏中这样讲：

> 这部分是迁移中最关键的物理约束。对普通同步逻辑来说，RTL 功能确定以后，布局通常可以交给 Vivado 自动完成。但这里的熵源是环形振荡器，它的振荡频率、采样关系和输出统计特性都会受到 LUT 延迟、反馈路径延迟以及物理位置影响。所以从原器件迁移到 ZYNQ-7020 后，我不能只把 RTL 复制过来，还要在新器件上重新固定熵源关键逻辑的物理位置。
>
> 这里我使用了两级物理约束。`LOC` 用来指定某个 cell 放到芯片上的哪个 Slice，例如 `SLICE_X44Y43`；`BEL` 用来指定它在这个 Slice 内部具体使用哪个基本资源，例如 `A6LUT`、`B6LUT`，或者寄存器位置 `AFF`、`BFF`。
>
> 以 RO0 为例，当前配置下一个数据 RO 由两级 LUT 构成：第一级是带使能反馈的 LUT，第二级是反相 LUT。我把 RO0 的第一级固定到 `SLICE_X44Y43/A6LUT`，把第二级固定到同一个 Slice 的 `B6LUT`。这样一个 RO 的主要振荡环就被压在同一个 Slice 的固定 LUT 资源上，而不是让 Vivado 每次实现时重新决定它的物理落点。
>
> 接着我把 8 个 RO 按 4 x 2 的紧凑模式放在 `SLICE_X44Y43` 到 `SLICE_X47Y44` 这一片区域。但是只固定 RO 本体还不够，因为最终随机位不是直接拿单个 RO 输出，而是由采样环对多个 RO 进行多相采样后，再对采样结果做异或压缩得到的。因此我还进一步固定了 64 个 `sampled_data` 采样寄存器的位置，固定了采样环中 NAND 和 NOT LUT 的位置，也固定了最终 `rand_bit` 异或逻辑及输出寄存器附近的物理落点。
>
> 所以这个 XDC 实际上固定的不是单独几个 RO，而是一整块熵源关键物理区域。这样做的意义是提高迁移后的物理结构可控性，让后续复现和不同布局方案对比更有依据。这里需要说明的是，本工程固定的是关键逻辑的物理放置，布线仍由 Vivado 在这些布局约束下自动完成。

## 15. 一句话总结

`manual_ro_locbel_round1.xdc` 的作用是：在 ZYNQ-7020 上用 `LOC` 指定 Slice、用 `BEL` 指定 Slice 内 LUT/FF，把 RO-TRNG 熵源中的 8 个 RO、采样寄存器、采样环和输出压缩逻辑固定到指定物理区域，从而减少 Vivado 自动布局带来的物理漂移，提高迁移后工程的可复现性和实验可比性。
