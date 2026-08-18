TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
      ../gpu_pkg.sv\
        scheduler.sv

TOPLEVEL = scheduler
MODULE = tb_scheduler

EXTRA_ARGS += --Wno-WIDTHEXPAND --Wno-WIDTHTRUNC 

include $(shell cocotb-config --makefiles)/Makefile.sim
