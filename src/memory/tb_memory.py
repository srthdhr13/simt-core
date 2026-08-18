import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

LD, ST = 0b01000, 0b01001
GLOBAL, SHARED = 0, 1


@cocotb.test()
async def tb_memory(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    dut.opcode.value = ST
    dut.memspace.value = GLOBAL
    dut.address[0].value = 5
    dut.write_data[0].value = 0x1234
    await RisingEdge(dut.clk)

    dut.opcode.value = LD
    await Timer(1, unit="ns")
    assert int(dut.read_data[0].value) == 0x1234

    dut.opcode.value = ST
    dut.memspace.value = SHARED
    dut.warp_id.value = 0
    dut.address[0].value = 3
    dut.write_data[0].value = 0xAAAA
    await RisingEdge(dut.clk)

    dut.warp_id.value = 1
    dut.write_data[0].value = 0xBBBB
    await RisingEdge(dut.clk)

    dut.opcode.value = LD
    dut.warp_id.value = 0
    await Timer(1, unit="ns")
    assert int(dut.read_data[0].value) == 0xAAAA