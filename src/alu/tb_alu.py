import cocotb
from cocotb.triggers import Timer

ADD, MUL, MAD, MOV, MOVS, CMP = 0b00001, 0b00010, 0b00011, 0b00100, 0b00101, 0b10000
EQ, NE, LT, GT = 0b00, 0b01, 0b10, 0b11


@cocotb.test()
async def tb_alu(dut):
    rs1 = [1, 2, 3, 4]
    rs2 = [10, 20, 30, 40]
    rd  = [100, 200, 300, 400]

    for i in range(4):
        dut.rd[i].value = rd[i]
        dut.rs1[i].value = rs1[i]
        dut.rs2[i].value = rs2[i]

    
    dut.opcode.value = ADD
    await Timer(1, unit="ns")
    assert int(dut.result[1].value) == rs1[1] + rs2[1]

    
    dut.opcode.value = MUL
    await Timer(1, unit="ns")
    assert int(dut.result[1].value) == rs1[1] * rs2[1]

    
    dut.opcode.value = MAD
    await Timer(1, unit="ns")
    assert int(dut.result[1].value) == rd[1] + rs1[1] * rs2[1]

    
    dut.opcode.value = MOV
    await Timer(1, unit="ns")
    assert int(dut.result[1].value) == rs1[1]

    
    dut.opcode.value = MOVS
    await Timer(1, unit="ns")
    assert int(dut.result[1].value) == rs1[1]

    
    dut.opcode.value = CMP
    dut.rs1[0].value = 5
    dut.rs2[0].value = 5
    dut.conditioncode.value = EQ
    await Timer(1, unit="ns")
    assert int(dut.result[0].value) == 1

    dut.rs1[0].value = 3
    dut.rs2[0].value = 5
    dut.conditioncode.value = LT
    await Timer(1, unit="ns")
    assert int(dut.result[0].value) == 1