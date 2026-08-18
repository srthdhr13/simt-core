import gpu_pkg::*;

module decode(

	input [15:0] inst_in,
	output [4:0] opcode ,
	output logic [2:0] rd,
	output logic [2:0] rs1,
	output logic  [2:0] rs2,
	output logic memspace,
	output logic [1:0] conditioncode);
	
  
  logic  [1:0] check_fam;
  assign opcode = inst_in[15:11];
  assign check_fam = opcode[4:3];
  always_comb begin 

  	
	 memspace      = 0;
	 conditioncode = 0;
	 rd            = 0;
	 rs1           = 0;
	 rs2           = 0;
	 
   	 case(check_fam)


    		2'b00: begin 

    	 		
         		rd     = inst_in[10:8];
         		rs1    = inst_in[7:5];
         		rs2    = inst_in[4:2];
         		
         	 

        	end 


        	2'b01: begin 

        		memspace = inst_in[10];
        		rd = inst_in[9:7];
        		rs1 = inst_in[6:4];

        	end 


        	2'b10: begin 

        		case(opcode) 

        			CMP:begin 
        			 conditioncode = inst_in[10:9];
        			 rd = inst_in[8:6];
        			 rs1 = inst_in[5:3];
        			 rs2 = inst_in[2:0];

        		   end 

        		    BAR:begin 
        		      conditioncode = 2'b0;
        		      rd = 3'b0;
        		      rs1 = 3'b0;
        		      rs2 = 3'b0;
        		    end 

        		    RET:begin 
        		      conditioncode = 2'b0;
        		      rd = 3'b0;
        		      rs1 = 3'b0;
        		      rs2 = 3'b0;
        		    end 
        		    default: begin 
        		    end 
        		endcase



        		

        	end 

        	default : begin 
        	end 

 
   	 endcase 

  end 




endmodule 
