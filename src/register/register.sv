import gpu_pkg::*;


module register (


	input clk,
	input rst,


	input reg_write_en,
	input [2:0] rd,
	input [2:0] rs1,
	input [2:0] rs2,
	input [4:0] opcode,

	
	input [$clog2(NUM_WARPS)-1:0] read_warp_id,
	input [$clog2(NUM_WARPS)-1:0] write_warp_id,


	input [DATA_WIDTH-1:0]write_data[NUM_THREADS-1:0],
	
	output logic [DATA_WIDTH-1:0] rs1_data[NUM_THREADS-1:0],
	output logic [DATA_WIDTH-1:0]rs2_data[NUM_THREADS-1:0],
	output logic [DATA_WIDTH-1:0] rd_data  [NUM_THREADS-1:0]

 );  
 

    
    logic [DATA_WIDTH-1:0] regfile [NUM_WARPS-1:0][NUM_THREADS-1:0][NUM_REGS-1:0];



    always_ff @(posedge clk or posedge rst) begin 
  
      


    	if (rst) begin 
    	
             for (int w = 0 ; w < NUM_WARPS ; w = w +1 )begin
    		for(int i = 0 ; i < NUM_THREADS ; i = i+1)begin 

    			for(int j = 0 ; j < NUM_REGS ; j = j + 1)begin 

    				regfile[w][i][j] <= '0;

    			end

    		end

    	end 
     end

    	else if (reg_write_en) begin 

    		for (int i = 0 ; i < NUM_THREADS ; i = i+1)begin 
    	

    		 regfile[write_warp_id][i][rd] <= write_data[i];

    		end 

    	end 
   

    end 

	always_comb begin
    		for (int k = 0 ; k < NUM_THREADS ; k = k+1) begin
        		if (opcode == MOVS) begin
            			case (rs1)
                		3'b000: rs1_data[k] = k[DATA_WIDTH-1:0];
                		3'b001: rs1_data[k] = {{(DATA_WIDTH-$clog2(NUM_WARPS)){1'b0}}, read_warp_id};
                		default: rs1_data[k] = '0;
          		  endcase
        	end else begin
            	rs1_data[k] = regfile[read_warp_id][k][rs1];
        	end
        	rs2_data[k] = regfile[read_warp_id][k][rs2];
        	rd_data[k]  = regfile[read_warp_id][k][rd];
    		end
	end


endmodule 



