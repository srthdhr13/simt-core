import gpu_pkg::*; 
module alu(
	input [4:0] opcode,
	input [1:0] conditioncode,
	input [DATA_WIDTH-1:0] rd [NUM_THREADS-1:0],
	input [DATA_WIDTH-1:0] rs1 [NUM_THREADS-1:0],
	input [DATA_WIDTH-1:0] rs2 [NUM_THREADS-1:0],
	output logic [DATA_WIDTH-1:0] result [NUM_THREADS-1:0]
	); 
	integer i;
	always_comb begin 
	    for (i = 0 ; i < NUM_THREADS ; i = i+1) begin 	
	    	result[i] = {DATA_WIDTH{1'b0}};
			case(opcode)
				ADD :begin 
					result[i] = rs1[i]+rs2[i];
				end
				MUL:begin 
					result[i] = rs1[i]*rs2[i];
				end
				MAD:begin 
					result[i] = rd[i] + (rs1[i]*rs2[i]);
				end
				MOV:begin 
					result[i] = rs1[i];
				end 
				MOVS:begin
					result[i] = rs1[i];
				end 
				CMP:begin 
					case(conditioncode)
						EQ:begin 
							result[i] = (rs1[i] == rs2[i]) ? {{(DATA_WIDTH-1){1'b0}},1'b1} : {DATA_WIDTH{1'b0}};
						end 
						NE:begin 
							result[i] = (rs1[i] != rs2[i]) ? {{(DATA_WIDTH-1){1'b0}},1'b1} : {DATA_WIDTH{1'b0}};
						end
						LT:begin 
							result[i] = (rs1[i] < rs2[i]) ? {{(DATA_WIDTH-1){1'b0}},1'b1} : {DATA_WIDTH{1'b0}};
						end
						GT:begin 
							result[i] = (rs1[i] > rs2[i]) ? {{(DATA_WIDTH-1){1'b0}},1'b1} : {DATA_WIDTH{1'b0}};
						end
						default : ;
					endcase 
				end 
				default : ;
			endcase 
		end 
	end
endmodule
