import gpu_pkg::* ;

module writeback(

	input [4:0] opcode,

	input [DATA_WIDTH-1:0] alu_result [NUM_THREADS-1:0],
	input [DATA_WIDTH-1:0] mem_result [NUM_THREADS-1:0],

	output logic [DATA_WIDTH-1:0] data [NUM_THREADS-1:0]


	);


   integer i;
   always_comb begin 

   	for (i = 0 ; i < NUM_THREADS ; i = i +1)begin 


   		case(opcode)

   			LD: begin 

   				data[i] = mem_result[i];



   			end

   			default : data[i] = alu_result[i];


   		endcase 


   	end 


   end 


endmodule 
