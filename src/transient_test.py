"""
transient_test.py

Executes the automated load transient test for a PDN output rail.
"""

import time
from datetime import datetime

from config import (
    INPUT_VOLTAGE,
    LOAD_LOW_PERCENT,
    LOAD_HIGH_PERCENT,
    TRANSIENT_FREQUENCY,
    PULSE_WIDTH_MS,
    NUMBER_OF_CAPTURES
)


def run_transient_test(
        psu,
        eload,
        scope,
        dmm,
        rail_name,
        rail_voltage,
        max_current):
    """
    Perform automated load transient test on one output rail.

    Parameters:
        psu        : PowerSupply object
        eload      : ElectronicLoad object
        scope      : Oscilloscope object
        dmm        : DigitalMultimeter object
        rail_name  : Name of the output rail (e.g. 3V3)
        rail_voltage : Expected output voltage
        max_current : Maximum rated current of the rail

    Returns:
        List containing measurement dictionaries.
    """

    results = []

    print(f"\nStarting Load Transient Test : {rail_name}")

    # Configure Power Supply

    psu.set_voltage(INPUT_VOLTAGE)
    psu.output_on()

    time.sleep(2)

    # Configure Oscilloscope

    scope.configure()

    # Calculate transient load values

    low_current = max_current * (LOAD_LOW_PERCENT / 100)

    high_current = max_current * (LOAD_HIGH_PERCENT / 100)

    # Configure Electronic Load

    eload.configure_dynamic_mode(
        low_current,
        high_current,
        TRANSIENT_FREQUENCY,
        PULSE_WIDTH_MS
    )

    # Capture Waveforms

    for capture in range(NUMBER_OF_CAPTURES):

        print(f"Capture {capture+1}/{NUMBER_OF_CAPTURES}")

        scope.single_capture()

        eload.enable()

        # Allow transient event
        time.sleep(1)

        measured_voltage = dmm.measure_voltage()
        measured_current = eload.measure_load_current()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        waveform_name = f"{rail_name}_{timestamp}_{capture+1}.png"

        scope.save_waveform(waveform_name)

        eload.disable()

        results.append({

            "Timestamp": timestamp,

            "Rail": rail_name,

            "Expected Voltage": rail_voltage,

            "Measured Voltage": measured_voltage,

            "Measured Current": measured_current,

            "Waveform": waveform_name

        })
    # Shut Down Instruments

    psu.output_off()

    print(f"{rail_name} Test Completed\n")

    return results