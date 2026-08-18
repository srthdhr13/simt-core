import gpu_pkg::*;

module fetch(

	input clk,
	input rst,
	input [$clog2(NUM_WARPS)-1:0] fetch_warp_id,
	output logic  [15:0] inst_out,
	output logic [15:0] pc_out,
	output logic [$clog2(NUM_WARPS)-1:0] warp_out

	);

	
	logic  [5:0] pc [NUM_WARPS-1:0];
	logic [15:0] inst_mem [0:63];
	

	initial begin 

		$readmemh("/home/sruthidhar/projects/gpu2/updated_proj/program.hex" , inst_mem);

	end 

	

	always_ff @(posedge clk or posedge rst) begin 
	
	       

		if (rst) begin 

			for(int  w = 0 ; w < NUM_WARPS ;  w = w+1)begin

			pc[w] <= 6'd0;end
			inst_out <= 16'd0;
			pc_out <= 16'd0;
			warp_out <= '0;
		

		end else begin 
		    inst_out <= inst_mem[pc[fetch_warp_id]];
		    pc_out <= {10'd0 ,pc[fetch_warp_id]};
		    warp_out <= fetch_warp_id;
			pc[fetch_warp_id] <= pc[fetch_warp_id]+ 6'd1;
			
		 

		end 

	end 
	
	


endmodule 	
