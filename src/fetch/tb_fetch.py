import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
 
PROGRAM = [
    0x2800, 0x2920, 0x4200, 0x0d08,
    0x42d0, 0x2680, 0x1e94, 0x1794,
    0x0d0c, 0x4b50, 0x8800, 0x4f80,
    0x8800, 0x4690, 0x86f5, 0x9000,
]
 
 
@cocotb.test()
async def tb_fetch(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
 
    await reset(dut)
 
    for expected_pc in range(3):
        pc, warp, inst = await fetch_cycle(dut, 0)
        assert pc == expected_pc, f"expected warp0 pc {expected_pc}, got {pc}"
        assert warp == 0, f"expected warp_out 0, got {warp}"
        assert inst == PROGRAM[expected_pc], f"expected inst {hex(PROGRAM[expected_pc])} at pc {expected_pc}, got {hex(inst)}"
 
    pc, warp, inst = await fetch_cycle(dut, 1)
    assert pc == 0, f"expected warp1 pc 0, got {pc}"
    assert warp == 1, f"expected warp_out 1, got {warp}"
    assert inst == PROGRAM[0], \
        f"expected inst {hex(PROGRAM[0])} at pc 0, got {hex(inst)}"
 
    pc, warp, inst = await fetch_cycle(dut, 0)
    assert pc == 3, f"expected warp0 pc 3, got {pc}"
    assert warp == 0, f"expected warp_out 0, got {warp}"
    assert inst == PROGRAM[3], \
        f"expected inst {hex(PROGRAM[3])} at pc 3, got {hex(inst)}"
 
 
async def reset(dut):
    dut.rst.value = 1
    dut.fetch_warp_id.value = 0
    await RisingEdge(dut.clk)
    dut.rst.value = 0
 
 
async def fetch_cycle(dut, warp_id):
    dut.fetch_warp_id.value = warp_id
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    return int(dut.pc_out.value), int(dut.warp_out.value), int(dut.inst_out.value)