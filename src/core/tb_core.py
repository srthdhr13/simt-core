import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly

@cocotb.test()
async def tb_core(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    print(f"{'cycle':>5} {'warp':>4} {'pc':>4} {'opcode':>8} {'reg_we':>6} {'rd':>3}")
    for cycle in range(30):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if int(dut.all_done.value) == 1:
            print(f"\nall_done asserted at cycle {cycle}")
            break
        we = int(dut.reg_write_en.value)
        print(f"{cycle:5} {int(dut.warp_out.value):4} {int(dut.pc_out.value):4} "
              f"{str(dut.opcode.value):>8} {we:6} {int(dut.rd.value) if we else -1:3}")