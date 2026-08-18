
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ReadOnly
 
ADD, ST, BAR, RET = 0b00001, 0b01001, 0b10001, 0b10010
 
async def step(dut, op, warp=0):
    dut.opcode.value = op
    dut.warp_id.value = warp
    await RisingEdge(dut.clk)
    await ReadOnly()
    await Timer(1, unit="ns")
 
@cocotb.test()
async def tb_controller(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
 
    dut.rst.value = 1
    dut.opcode.value = ADD
    dut.warp_id.value = 0
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await step(dut, ADD)
 
    dut.opcode.value = ST
    await Timer(1, unit="ns")
    assert int(dut.reg_write_en.value) == 0    
 
    dut.opcode.value = ADD
    await Timer(1, unit="ns")
    assert int(dut.reg_write_en.value) == 1     
 
    await step(dut, RET, warp=1)
    await step(dut, RET, warp=3)
    assert int(dut.warp_done.value) == 0b1010   
 
    await step(dut, BAR, warp=0)
    await step(dut, BAR, warp=2)
    assert int(dut.warp_waiting.value) == 0b0101   
 
    await step(dut, ADD)
    assert int(dut.warp_waiting.value) == 0     
    assert int(dut.warp_done.value) == 0b1010   