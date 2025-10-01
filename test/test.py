# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# This is a testbench specifically for the ECE-298A Counter Project.
@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting counter test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # --- 1. Test Reset ---
    dut._log.info("Testing reset")
    dut.rst_n.value = 0 # Assert reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1 # De-assert reset
    await ClockCycles(dut.clk, 1)

    # After reset, the count should be 0.
    dut.ui_in.value = 0b00001000 # oe=1
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0, f"Reset failed: expected 0, got {dut.uio_out.value}"

    # --- 2. Test Parallel Load ---
    dut._log.info("Testing parallel load")
    load_value = 121
    dut.ui_in.value = 0b00000010 # oe=0, load=1
    dut.uio_in.value = load_value
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = 0b00001000 # oe=1, load=0
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == load_value, f"Load failed: expected {load_value}, got {dut.uio_out.value}"

    # --- 3. Test Count Up ---
    dut._log.info("Testing count up")
    dut.ui_in.value = 0b00001101 # oe=1, up=1, en=1
    await ClockCycles(dut.clk, 10)
    expected_value = (load_value + 10) & 0xFF # Use & 0xFF for 8-bit wrap-around
    assert dut.uio_out.value == expected_value, f"Count up failed: expected {expected_value}, got {dut.uio_out.value}"

    # --- 4. Test Count Down ---
    dut._log.info("Testing count down")
    dut.ui_in.value = 0b00001001 # oe=1, up=0, en=1
    await ClockCycles(dut.clk, 20)
    expected_value = (expected_value - 20) & 0xFF # Use & 0xFF for 8-bit wrap-around
    assert dut.uio_out.value == expected_value, f"Count down failed: expected {expected_value}, got {dut.uio_out.value}"

    # --- 5. Test Output Enable (Tri-state) ---
    dut._log.info("Testing tri-state output")
    dut.ui_in.value = 0b00000001 # oe=0, en=1
    await ClockCycles(dut.clk, 1)

    # In RTL sim, the bus will be 'z'. In gate-level, it will be 'x'.
    # We can detect a gate-level sim by checking for the presence of power pins.
    is_gl_sim = hasattr(dut, 'VPWR')

    if is_gl_sim:
        dut._log.info("Gate-level sim: checking for 'x' on tri-stated bus")
        assert 'x' in dut.uio_out.value.binstr.lower(), "Tri-state (oe=0) failed in GL sim."
    else:
        dut._log.info("RTL sim: checking for 'z' on tri-stated bus")
        assert 'z' in dut.uio_out.value.binstr.lower(), "Tri-state (oe=0) failed in RTL sim."

    dut._log.info("Tri-state test passed.")
    dut._log.info("All tests passed!")
