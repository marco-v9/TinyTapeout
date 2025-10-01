// src/tt_um_marco_counter.v
module tt_um_marco_counter (
    input  wire [7:0] ui_in,    // 8 dedicated inputs
    output wire [7:0] uo_out,   // 8 dedicated outputs
    input  wire [7:0] uio_in,   // 8 bidirectional inputs 
    output wire [7:0] uio_out,  // 8 bidirectional outputs
    output wire [7:0] uio_oe,   // 1=drive uio_out, 0=input
    input  wire       ena,      // always 1 when user project is enabled
    input  wire       clk,      // system clock
    input  wire       rst_n     // reset (active low)
);
    // map inputs
    wire en     = ui_in[0]; // Count enable
    wire load   = ui_in[1]; // Sync load enable
    wire up     = ui_in[2]; // Count direction
    wire oe     = ui_in[3]; // Output enable for the tri-state bus

    wire [7:0] d = uio_in;   // Parallel load value comes from the bidi bus
    wire [7:0] y;            // The counter's output wire


    counter_298A dut (
        .clk     (clk),
        .reset_n (rst_n),
        .en      (en),
        .load    (load),
        .up      (up),
        .oe      (oe),
        .d       (d),
        .y       (y)
    );

    assign uo_out = 8'b0;
    
    assign uio_out = y;

    assign uio_oe = {8{oe}};

    wire _unused = &{ena, 1'b0};

endmodule
