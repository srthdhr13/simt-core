import gpu_pkg::*;


module memory(
    input clk,
    input rst,
    input memspace,
    input [4:0] opcode,
    input [$clog2(NUM_WARPS)-1:0] warp_id,
    input [DATA_WIDTH-1:0] address [NUM_THREADS-1:0],
    input [DATA_WIDTH-1:0] write_data [NUM_THREADS-1:0],
    output logic [DATA_WIDTH-1:0] read_data [NUM_THREADS-1:0]
);
    logic [DATA_WIDTH-1:0] globalmem [GLOBAL_MEM_SIZE-1:0];
    logic [DATA_WIDTH-1:0] sharedmem [NUM_WARPS-1:0][SHARED_MEM_SIZE-1:0];
    integer i , a;

  
    always_comb begin
        case(opcode)
            LD: begin
                case(memspace)
                    GLOBAL: for(i=0;i<NUM_THREADS;i=i+1)
                              read_data[i] = globalmem[address[i][$clog2(GLOBAL_MEM_SIZE)-1:0]];
                    SHARED: for(i=0;i<NUM_THREADS;i=i+1)
                              read_data[i] = sharedmem[warp_id][address[i][$clog2(SHARED_MEM_SIZE)-1:0]];
                endcase
            end
            default: for(i=0;i<NUM_THREADS;i=i+1)
                         read_data[i] = '0;
        endcase
    end

  
    always_ff @(posedge clk or posedge  rst) begin
        if (rst) begin

               for ( a = 0; a < GLOBAL_MEM_SIZE; a = a + 1)
                     globalmem[a] <= '0;
                for (int w = 0; w < NUM_WARPS; w = w + 1)
                    for (int a = 0; a < SHARED_MEM_SIZE; a = a + 1)
                        sharedmem[w][a] <= '0;
           
        end else begin
            case(opcode)
                ST: begin
                    case(memspace)
                        GLOBAL: for(a=0;a<NUM_THREADS;a=a+1)
                                  globalmem[address[a][$clog2(GLOBAL_MEM_SIZE)-1:0]] <= write_data[a];
                        SHARED: for(a=0;a<NUM_THREADS;a=a+1)
                                  sharedmem[warp_id][address[a][$clog2(SHARED_MEM_SIZE)-1:0]] <= write_data[a];

                        default : ;
                    endcase
                end
                default : ;
            endcase
        end
    end

endmodule
