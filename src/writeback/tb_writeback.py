import cocotb
from cocotb.triggers import Timer

LD = 0b01000
ADD = 0b00001
ST = 0b01001
BAR = 0b10001

@cocotb.test()
async def tb_writeback(dut):
    alu_vals = [0x1111, 0x2222, 0x3333, 0x4444]
    mem_vals = [0xAAAA, 0xBBBB, 0xCCCC, 0xDDDD]
    for i in range(4):
        dut.alu_result[i].value = alu_vals[i]
        dut.mem_result[i].value = mem_vals[i]

    for op in [ADD, ST, BAR, 0]:
        dut.opcode.value = op
        await Timer(1, unit="ns")
        for i in range(4):
            assert int(dut.data[i].value) == alu_vals[i], \
                f"opcode {bin(op)} thread {i}: expected ALU {hex(alu_vals[i])}, got {hex(int(dut.data[i].value))}"

  
    dut.opcode.value = LD
    await Timer(1, unit="ns")
    for i in range(4):
        assert int(dut.data[i].value) == mem_vals[i], \
            f"LD thread {i}: expected MEM {hex(mem_vals[i])}, got {hex(int(dut.data[i].value))}"