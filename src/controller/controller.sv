import gpu_pkg::*;

module controller(

	input clk ,
	input rst,
	input [$clog2(NUM_WARPS)-1:0] warp_id,

	input [4:0] opcode,
	output logic reg_write_en,
	output logic [NUM_WARPS-1 : 0] warp_done,
	output logic [NUM_WARPS-1 : 0] warp_waiting);


	assign reg_write_en = (opcode != ST) && (opcode != BAR) && (opcode != RET);

	always_ff @(posedge clk or posedge rst)begin
		
		if(rst)begin
			warp_done <= '0;
			warp_waiting <= '0;
		end
		else begin
			if(opcode == RET)
				warp_done[warp_id] <= 1'b1;

			if(opcode == BAR)
				warp_waiting[warp_id] <= 1'b1;

			if(&(warp_waiting | warp_done))
				warp_waiting <= '0;
		end
	end















endmodule 