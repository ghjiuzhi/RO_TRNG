################################################################
# Placeholder XDC for RO_TDC_code_density_cal_sysclk_top
#
# The base fpga1 TDC sys_clk XDC already constrains sys_clk,
# UART_TX_o, por_n_i, RO combinational loops, and TDC false paths.
# This file exists so the shared Vivado in-memory flow receives an
# explicit first tclarg for "extra_xdc" and does not shift arguments.
################################################################

