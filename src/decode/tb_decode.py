import cocotb
from cocotb.triggers import Timer

ADD, LD, CMP, BAR = 0b00001, 0b01000, 0b10000, 0b10001


@cocotb.test()
async def tb_decode(dut):

    
    dut.inst_in.value = (ADD << 11) | (0b101 << 8) | (0b011 << 5) | (0b110 << 2)
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == ADD
    assert int(dut.rd.value) == 0b101
    assert int(dut.rs1.value) == 0b011
    assert int(dut.rs2.value) == 0b110

    
    dut.inst_in.value = (LD << 11) | (1 << 10) | (0b010 << 7) | (0b111 << 4)
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == LD
    assert int(dut.memspace.value) == 1
    assert int(dut.rd.value) == 0b010
    assert int(dut.rs1.value) == 0b111

    
    dut.inst_in.value = (CMP << 11) | (0b10 << 9) | (0b001 << 6) | (0b010 << 3) | 0b011
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == CMP
    assert int(dut.conditioncode.value) == 0b10
    assert int(dut.rd.value) == 0b001
    assert int(dut.rs1.value) == 0b010
    assert int(dut.rs2.value) == 0b011

    
    dut.inst_in.value = BAR << 11
    await Timer(1, unit="ns")
    assert int(dut.opcode.value) == BAR
    assert int(dut.rd.value) == 0
    assert int(dut.rs1.value) == 0
    assert int(dut.rs2.value) == 0