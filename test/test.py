# test.py (Corrected)

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# This is a testbench specifically for the ECE-298A Counter Project.
# It tests the main functions: reset, load, count up, count down, and output enable.
@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting counter test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # --- 1. Test Reset ---
    dut._log.info("Testing reset")
    dut.rst_n.value = 0 # Assert reset
    # Set initial control values
    dut.ena.value = 1       # Project is enabled
    dut.ui_in.value = 0b00001000 # oe=1, up=0, load=0, en=0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1 # De-assert reset
    await ClockCycles(dut.clk, 1)

    # After reset, the count should be 0.
    # We set oe=1 (ui_in[3]) to see the output.
    dut.ui_in.value = 0b00001000 # oe=1
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0, f"Reset failed: expected 0, got {dut.uio_out.value}"

    # --- 2. Test Parallel Load ---
    dut._log.info("Testing parallel load")
    # To load, we set oe=0 (uio becomes input) and load=1.
    load_value = 121
    dut.ui_in.value = 0b00000010 # oe=0, up=0, load=1, en=0
    dut.uio_in.value = load_value
    await ClockCycles(dut.clk, 1) # Wait for load to happen on posedge clk

    # Now, disable load and enable output to check the value.
    dut.ui_in.value = 0b00001000 # oe=1, load=0
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == load_value, f"Load failed: expected {load_value}, got {dut.uio_out.value}"

    # --- 3. Test Count Up ---
    dut._log.info("Testing count up")
    # Enable counting, direction up. oe is already high.
    dut.ui_in.value = 0b00001101 # oe=1, up=1, load=0, en=1
    await ClockCycles(dut.clk, 10) # Count for 10 cycles
    expected_value = load_value + 10
    assert dut.uio_out.value == expected_value, f"Count up failed: expected {expected_value}, got {dut.uio_out.value}"

    # --- 4. Test Count Down ---
    dut._log.info("Testing count down")
    # Enable counting, direction down.
    dut.ui_in.value = 0b00001001 # oe=1, up=0, load=0, en=1
    await ClockCycles(dut.clk, 20) # Count for 20 cycles
    expected_value = expected_value - 20
    assert dut.uio_out.value == expected_value, f"Count down failed: expected {expected_value}, got {dut.uio_out.value}"

    # --- 5. Test Output Enable (Tri-state) ---
    dut._log.info("Testing tri-state output")
    # Disable the output driver.
    dut.ui_in.value = 0b00000001 # oe=0, en=1
    await ClockCycles(dut.clk, 1)
    # When tri-stated, the value is high-impedance ('z').
    # We check if 'z' is present in the binary string representation of the output.
    assert 'z' in dut.uio_out.value.binstr.lower(), "Tri-state (oe=0) failed."
    dut._log.info("Tri-state test passed.")
