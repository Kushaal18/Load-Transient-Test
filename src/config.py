"""
config.py

Configuration file for the Load Transient Testing Automation Framework.

This file contains:
- Instrument VISA addresses
- PDN rail specifications
- Test parameters
- Acceptance criteria
"""

# Instrument VISA Addresses

POWER_SUPPLY_ADDRESS = None
ELECTRONIC_LOAD_ADDRESS = None
OSCILLOSCOPE_ADDRESS = None
DMM_ADDRESS = None

# Input Supply

INPUT_VOLTAGE = 5.0           #V

# PDN Output Rail Specifications

RAILS = [
    {
        "name": "3V6",
        "voltage": 3.6,
        "max_current": 1.5
    },

    {
        "name": "1V8",
        "voltage": 1.8,
        "max_current": 1.0
    },

    {
        "name": "3V3",
        "voltage": 3.3,
        "max_current": 3.0
    },

    {
        "name": "2V5",
        "voltage": 2.5,
        "max_current": 1.5
    }
]

# Load Transient Test Parameters

LOAD_LOW_PERCENT = 10
LOAD_HIGH_PERCENT = 90
TRANSIENT_FREQUENCY = 1000      # Hz
PULSE_WIDTH_MS = 5              # ms
NUMBER_OF_CAPTURES = 10

# Acceptance Criteria

VOLTAGE_TOLERANCE = 0.05        
MAX_RIPPLE = 50              #mV
MAX_OVERSHOOT = 100          #mV
MAX_UNDERSHOOT = 100         #mV
MAX_SETTLING_TIME = 100      #us

# Output File Locations

CSV_FOLDER = "data/csv"
WAVEFORM_FOLDER = "data/waveforms"
REPORT_FOLDER = "data/report"