TOPLEVEL_LANG = verilog
SIM = verilator
VERILOG_SOURCES = \
    ../gpu_pkg.sv \
    ../fetch/fetch.sv \
    ../decode/decode.sv \
    ../alu/alu.sv \
    ../register/register.sv \
    ../memory/memory.sv \
    ../writeback/writeback.sv \
    ../controller/controller.sv \
    ../scheduler/scheduler.sv \
    ./core.sv
TOPLEVEL = core
MODULE = tb_core

EXTRA_ARGS += --Wno-WIDTHEXPAND --Wno-WIDTHTRUNC

include $(shell cocotb-config --makefiles)/Makefile.sim