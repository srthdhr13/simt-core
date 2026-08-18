package gpu_pkg;
  parameter NUM_WARPS = 4;
  parameter NUM_THREADS = 4;
  parameter NUM_REGS = 8;
  parameter DATA_WIDTH = 16;
  parameter ADD  = 5'b00001;
  parameter MUL =  5'b00010;
  parameter MAD =  5'b00011;
  parameter MOV =  5'b00100;  
  parameter MOVS =  5'b00101;
  parameter LD  =  5'b01000;
  parameter ST = 5'b01001;
  parameter CMP  = 5'b10000;
  parameter BAR =  5'b10001;
  parameter RET=5'b10010;
  parameter EQ = 2'b00;
  parameter NE = 2'b01;
  parameter LT = 2'b10;
  parameter GT =  2'b11;
  parameter GLOBAL = 1'b0;
  parameter SHARED = 1'b1;
  parameter GLOBAL_MEM_SIZE = 64;
  parameter SHARED_MEM_SIZE = 32;

endpackage
