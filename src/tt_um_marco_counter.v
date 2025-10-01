// src/tt_um_marco_counter.v
module tt_um_marco_counter (
    input  wire [7:0] ui_in,    // 8 dedicated inputs
    output wire [7:0] uo_out,   // 8 dedicated outputs
    input  wire [7:0] uio_in,   // 8 bidirectional inputs (when oe=0)
    output wire [7:0] uio_out,  // 8 bidirectional outputs
    output wire [7:0] uio_oe,   // 1=drive uio_out, 0=input
    input  wire       ena,      // always 1 when user project is enabled
    input  wire       clk,      // system clock
    input  wire       rst_n     // reset (active low)
);
    // map inputs
    wire [7:0] d    = ui_in;     // parallel load value
    wire       en   = uio_in[0]; // controls on bidir pins (as inputs)
    wire       load = uio_in[1];
    wire       up   = uio_in[2];
    wire       oe   = uio_in[3];

    // DUT
    wire [7:0] y;

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

    assign uo_out = y;

    assign uio_out = 8'h00;
    assign uio_oe  = 8'h00; // keep UIO as inputs
endmodule
