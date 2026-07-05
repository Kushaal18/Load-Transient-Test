# Power Distribution Network (PDN) Load Transient Test Automation

## Overview

This project implements a Python-based automated test framework for load transient testing of a Power Distribution Network (PDN) using SCPI commands and the PyVISA library. The framework automates instrument configuration, executes the load transient test sequence, logs measurement data to a CSV file, and generates a PDF qualification report.

---

## Source Files

### `config.py`

Contains all configurable parameters used throughout the project, including:

- Instrument VISA addresses
- Test parameters
- Voltage tolerance limits
- Load transient settings
- File paths
- PDN rail specifications

---

### `instruments.py`

Implements Python classes for communicating with the test instruments using SCPI commands through PyVISA.

Supported instruments:

- Keithley 2230-30-1 Programmable DC Power Supply
- Keithley 2380 Electronic Load
- Keysight DSOX6004A Oscilloscope
- Keithley DMM6500 Digital Multimeter

Each class provides functions for connecting to the instrument, configuring it, performing measurements, and disconnecting after testing.

---

### `transient_test.py`

Implements the automated load transient testing procedure.

Responsibilities include:

- Configure the power supply
- Configure the electronic load
- Configure the oscilloscope
- Execute the transient test
- Measure output voltage and load current
- Capture and save waveforms
- Return measurement results

---

### `csvlog.py`

Logs all measurements obtained during testing into a CSV file.

Responsibilities include:

- Create CSV log file
- Store measurement results
- Evaluate voltage acceptance criteria
- Record Pass/Fail status for every measurement

---

### `report.py`

Generates a PDF qualification report from the recorded CSV data.

The report summarizes:

- Average, minimum, and maximum output voltage
- Average, minimum, and maximum load current
- Pass/Fail count for each output rail
- Overall qualification result

---

### `main.py`

Acts as the entry point of the automation framework.

Responsibilities include:

- Connect all instruments
- Request board information from the operator
- Execute load transient testing for each PDN output rail
- Save test results
- Generate the final qualification report
- Disconnect all instruments

---

## Assumptions

- Manual probe switching is performed between output rails.
- Load transient parameters (frequency, pulse width, etc.) were assumed(values are written in the final submission document).
- SCPI commands were verified against the respective instrument datasheet where applicable.
- Instrument connections are verified before testing begins, and the program exits if any required instrument is unavailable.

---

## How to Run

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python src/main.py
```

---

## Author

**Kushaal Kundala**
