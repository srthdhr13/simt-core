import gpu_pkg::*;
module core(

	input clk,
	input rst
	
	);
	
	//fetch
 	 logic [15:0] inst_out;
 	 logic [$clog2(NUM_WARPS)-1:0] warp_out;
 	 logic [15:0] pc_out;
 	 
 	 //decode
 	 logic [4:0] opcode;
 	 logic [1:0] conditioncode;
 	 logic memspace;
 	 logic [2:0] rd;
 	 logic [2:0] rs1;
 	 logic [2:0] rs2;
 	 
 	 //alu 
 	 logic [DATA_WIDTH-1:0] result [NUM_THREADS-1:0];
 	 
 	 //controller
 	 logic reg_write_en;
 	 logic [NUM_WARPS-1:0] warp_done;
 	 logic [NUM_WARPS-1:0] warp_waiting;
 	 
 	 //writeback
 	 
 	 logic [DATA_WIDTH-1 :0] data [NUM_THREADS-1:0];
 	 
 	 //register
 	 
	logic [$clog2(NUM_WARPS)-1:0] read_warp_id;
	logic [$clog2(NUM_WARPS)-1:0] write_warp_id;

	logic [DATA_WIDTH-1:0] rs1_data[NUM_THREADS-1:0];
	logic [DATA_WIDTH-1:0]rs2_data[NUM_THREADS-1:0];
	logic [DATA_WIDTH-1:0] rd_data  [NUM_THREADS-1:0];
	
	//memory 
	logic [DATA_WIDTH-1:0] read_data [NUM_THREADS-1:0];
	
	//scheduler
	logic all_done;

	logic  [$clog2(NUM_WARPS)-1:0]warp_id;
	
 


	fetch fetch_inst(

		.clk(clk),
		.rst(rst),
		.fetch_warp_id(warp_id),
		.pc_out(pc_out),
		.warp_out(warp_out),
		.inst_out(inst_out)
		);
		
	decode decode_inst(
	
		.inst_in(inst_out),
		.opcode(opcode),
		.conditioncode(conditioncode),
		.memspace(memspace),
		.rd(rd),
		.rs1(rs1),
		.rs2(rs2)
	
	);
	
	alu alu_inst(
		.opcode(opcode),
		.conditioncode(conditioncode),
		.rd(rd_data),
		.rs1(rs1_data),
		.rs2(rs2_data),
		.result(result)
	);
	
	controller cont_inst(
		.clk(clk),
		.rst(rst),
		.warp_id(warp_out),
		.opcode(opcode),
		.reg_write_en(reg_write_en),
		.warp_done(warp_done),
		.warp_waiting(warp_waiting)
	
	
	);
	
	writeback writeback_inst(
		.opcode(opcode),
		.alu_result(result),
		.mem_result(read_data),
		.data(data)
	);
	
	register register_inst(
	
		.clk(clk),
		.rst(rst),
		.reg_write_en(reg_write_en),
		.rd(rd),
		.rs1(rs1),
		.rs2(rs2),
		.opcode(opcode),
		.read_warp_id(warp_out),
		.write_warp_id(warp_out),
		.write_data(data),
		.rs1_data(rs1_data),
		.rs2_data(rs2_data),
		.rd_data(rd_data)

	);
	
	memory memory_inst(
		.clk(clk),
		.rst(rst),
		.memspace(memspace),
		.opcode(opcode),
		.warp_id(warp_out),
		.address(rs1_data),
		.write_data(rd_data),
		.read_data(read_data)

	);
	
	scheduler scheduler_inst(
	
		.clk(clk),
		.rst(rst),
		.warp_done(warp_done),
		.warp_waiting(warp_waiting),
		.all_done(all_done),
		.warp_id(warp_id)
	
	);


endmodule 
