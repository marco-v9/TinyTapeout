module counter_298A (
    input  wire        clk,
    input  wire        reset_n,   // async reset, active lo
    input  wire        en,        // count enable
    input  wire        load,      // sync load: 1 -> load d on next rising clk
    input  wire        up,        // 1 = count up, 0 = count down
    input  wire        oe,        // 1 = drive outputs, 0 = high-Z
    input  wire [7:0]  d,         // parallel load value
    output wire [7:0]  y          // tri-stated count bus
);

    reg [7:0] count_q;

    always @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            count_q <= 8'd0;
        end 

        else if (load) begin
            count_q <= d;
        end 
        
        else if (en) begin
            if (up)
                count_q <= count_q + 8'd1;
            else
                count_q <= count_q - 8'd1;
        end
    end

    // tri-state outputs 
    //assign y = oe ? count_q : 8'bz;
    assign y = count_q;

endmodule
