TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
  ../gpu_pkg.sv\
    fetch.sv

TOPLEVEL = fetch
MODULE = tb_fetch

include $(shell cocotb-config --makefiles)/Makefile.sim
