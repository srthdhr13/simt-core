import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def tb_scheduler(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.rst.value = 1
    dut.warp_done.value = 0b0000
    dut.warp_waiting.value = 0b0000
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    assert int(dut.warp_id.value) == 0
    for expected in [1, 2, 3, 0]:
        await RisingEdge(dut.clk)
        assert int(dut.warp_id.value) == expected

    dut.warp_done.value = 0b0110
    await RisingEdge(dut.clk)
    assert int(dut.warp_id.value) == 1
    await RisingEdge(dut.clk)
    assert int(dut.warp_id.value) == 3

    dut.warp_done.value = 0b0000
    dut.warp_waiting.value = 0b0110
    await RisingEdge(dut.clk)
    assert int(dut.warp_id.value) == 0
    await RisingEdge(dut.clk)
    assert int(dut.warp_id.value) == 3

    dut.warp_waiting.value = 0b0000
    dut.warp_done.value = 0b1111
    await RisingEdge(dut.clk)
    assert dut.all_done.value == 1
    held = int(dut.warp_id.value)
    await RisingEdge(dut.clk)
    assert int(dut.warp_id.value) == held