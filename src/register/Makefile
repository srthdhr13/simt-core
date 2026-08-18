TOPLEVEL_LANG = verilog
SIM = verilator 

VERILOG_SOURCES = \
  ../gpu_pkg.sv\
   register.sv

TOPLEVEL = register
MODULE = tb_register

include $(shell cocotb-config --makefiles)/Makefile.sim
