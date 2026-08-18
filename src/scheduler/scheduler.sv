import gpu_pkg::*;

module scheduler(

	input clk,
	input rst ,

	input [NUM_WARPS-1:0] warp_done,
	input [NUM_WARPS-1:0] warp_waiting,

	output logic all_done,

	output logic  [$clog2(NUM_WARPS)-1:0]warp_id);




		always_ff @(posedge clk or posedge rst)begin
			if(rst )begin warp_id <= '0; end

		    else if (!all_done) begin 

		    	for(int i = 1 ; i < NUM_WARPS ; i = i + 1)begin 

		    		if(!warp_done[(warp_id + i )%NUM_WARPS] && !warp_waiting[(warp_id +i)%NUM_WARPS])begin    

		    			warp_id <= (warp_id + i )%NUM_WARPS;

		    			break;



		    		end


		    	end

		    end


		end


		assign all_done = &warp_done;


endmodule 
