import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

MOVS_OPCODE = 0b00101   
NORMAL_OPCODE = 0        

@cocotb.test()
async def tb_register(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    await reset(dut)

    await write_reg(dut, 0, 1, [0x1111, 0x2222, 0x3333, 0x4444])
    await check_reg(dut, 0, 1, 1,
                     [0x1111, 0x2222, 0x3333, 0x4444],
                     [0x1111, 0x2222, 0x3333, 0x4444])
    await check_reg(dut, 1, 1, 1,
                     [0, 0, 0, 0],
                     [0, 0, 0, 0])
    await write_reg(dut, 1, 1, [0xAAAA, 0xBBBB, 0xCCCC, 0xDDDD])
    await check_reg(dut, 1, 1, 1,
                     [0xAAAA, 0xBBBB, 0xCCCC, 0xDDDD],
                     [0xAAAA, 0xBBBB, 0xCCCC, 0xDDDD])
    await check_reg(dut, 0, 1, 1,
                     [0x1111, 0x2222, 0x3333, 0x4444],
                     [0x1111, 0x2222, 0x3333, 0x4444])
    await write_and_read_same_cycle(
        dut,
        write_warp=1, wr_reg=2, wr_values=[0x5555, 0x6666, 0x7777, 0x8888],
        read_warp=0, rs1=1, rs2=1,
        expected_rs1=[0x1111, 0x2222, 0x3333, 0x4444],
        expected_rs2=[0x1111, 0x2222, 0x3333, 0x4444],
        expected_rd=[0, 0, 0, 0],
    )

    await check_movs_tid(dut, read_warp=0)
    await check_movs_tid(dut, read_warp=1)

    await check_movs_wid(dut, read_warp=0, expected_wid=0)
    await check_movs_wid(dut, read_warp=1, expected_wid=1)


async def reset(dut):
    dut.rst.value = 1
    dut.reg_write_en.value = 0
    dut.opcode.value = NORMAL_OPCODE
    dut.read_warp_id.value = 0
    dut.write_warp_id.value = 0
    dut.rs1.value = 0
    dut.rs2.value = 0
    dut.rd.value = 0
    for i in range(4):
        dut.write_data[i].value = 0
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)


async def write_reg(dut, warp, reg, values):
    dut.opcode.value = NORMAL_OPCODE
    dut.write_warp_id.value = warp
    dut.rd.value = reg
    for i in range(4):
        dut.write_data[i].value = values[i]
    dut.reg_write_en.value = 1
    await RisingEdge(dut.clk)
    dut.reg_write_en.value = 0
    await Timer(1, unit="ns")


async def check_reg(dut, warp, rs1, rs2,
                     expected_rs1, expected_rs2):
    dut.opcode.value = NORMAL_OPCODE
    dut.read_warp_id.value = warp
    dut.rs1.value = rs1
    dut.rs2.value = rs2
    await Timer(1, unit="ns")
    for i in range(4):
        assert int(dut.rs1_data[i].value) == expected_rs1[i], \
            f"RS1 mismatch at thread {i}"
        assert int(dut.rs2_data[i].value) == expected_rs2[i], \
            f"RS2 mismatch at thread {i}"


async def write_and_read_same_cycle(dut, write_warp, wr_reg, wr_values,
                                     read_warp, rs1, rs2,
                                     expected_rs1, expected_rs2, expected_rd):
    dut.opcode.value = NORMAL_OPCODE
    dut.write_warp_id.value = write_warp
    dut.rd.value = wr_reg
    for i in range(4):
        dut.write_data[i].value = wr_values[i]
    dut.reg_write_en.value = 1
    dut.read_warp_id.value = read_warp
    dut.rs1.value = rs1
    dut.rs2.value = rs2
    await RisingEdge(dut.clk)
    dut.reg_write_en.value = 0
    await Timer(1, unit="ns")
    for i in range(4):
        assert int(dut.rs1_data[i].value) == expected_rs1[i], \
            f"RS1 mismatch at thread {i} during concurrent write"
        assert int(dut.rs2_data[i].value) == expected_rs2[i], \
            f"RS2 mismatch at thread {i} during concurrent write"
        assert int(dut.rd_data[i].value) == expected_rd[i], \
            f"RD mismatch at thread {i} during concurrent write"


async def check_movs_tid(dut, read_warp):

    dut.opcode.value = MOVS_OPCODE
    dut.read_warp_id.value = read_warp
    dut.rs1.value = 0b000
    await Timer(1, unit="ns")
    for i in range(4):
        assert int(dut.rs1_data[i].value) == i, \
            f"MOVS %tid mismatch at thread {i}, warp {read_warp}: got {int(dut.rs1_data[i].value)}"


async def check_movs_wid(dut, read_warp, expected_wid):
  
    dut.opcode.value = MOVS_OPCODE
    dut.read_warp_id.value = read_warp
    dut.rs1.value = 0b001
    await Timer(1, unit="ns")
    for i in range(4):
        assert int(dut.rs1_data[i].value) == expected_wid, \
            f"MOVS %wid mismatch at thread {i}, warp {read_warp}: got {int(dut.rs1_data[i].value)}"