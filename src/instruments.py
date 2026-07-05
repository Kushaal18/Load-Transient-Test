"""
This module contains classes to communicate with laboratory
instruments using PyVISA and SCPI commands.

Instruments:
- Keithley 2230-30-1 Programmable DC Power Supply
- Keithley 2380 Electronic Load
- Keysight DSOX6004A Oscilloscope
- Keithley DMM6500 Digital Multimeter
"""

import pyvisa

# Power Supply

class PowerSupply:

    def __init__(self, address):
        self.address = address
        self.instrument = None

    def connect(self):

        try:
            rm = pyvisa.ResourceManager()
            self.instrument = rm.open_resource(self.address)
            print("Power Supply Connected")
            return True

        except Exception as e:
            print(f"Power Supply Connection Error: {e}")
            return False

    def set_voltage(self, voltage, channel=1):
        """Set output voltage."""
        
        self.instrument.write(f"INST:NSEL {channel}")
        self.instrument.write(f"VOLT {voltage}")

    def output_on(self):
        """Enable output."""

        self.instrument.write("OUTP ON")

    def output_off(self):
        """Disable output."""

        self.instrument.write("OUTP OFF")

    def disconnect(self):

        if self.instrument:
            self.instrument.close()

# Electronic Load

class ElectronicLoad:

    def __init__(self, address):
        self.address = address
        self.instrument = None

    def connect(self):

        try:
            rm = pyvisa.ResourceManager()
            self.instrument = rm.open_resource(self.address)
            print("Electronic Load Connected")
            return True
        except Exception as e:
            print(f"Electronic Load Connection Error: {e}")
            return False

    def set_static_current(self, current):
        """Set constant current mode."""

        self.instrument.write("FUNC CURR")
        self.instrument.write(f"CURR {current}")

    def configure_dynamic_mode(self,
                               low_current,
                               high_current,
                               frequency,
                               pulse_width):
        """
        Configure dynamic load for transient testing.

        NOTE:
        These SCPI commands are representative.
        Exact commands depend on the Keithley model.
        """

        self.instrument.write("FUNC CURR")

        self.instrument.write(f"CURR:LOW {low_current}")

        self.instrument.write(f"CURR:HIGH {high_current}")

        self.instrument.write(f"FREQ {frequency}")

        self.instrument.write(f"PWIDTH {pulse_width}")

    def enable(self):

        self.instrument.write("INPUT ON")

    def disable(self):

        self.instrument.write("INPUT OFF")

    def disconnect(self):

        if self.instrument:
            self.instrument.close()
    def measure_load_current(self):
        """
        Measure actual load current.
        """
        current = self.instrument.query("MEAS:CURR?")

        return float(current)
# Oscilloscope

class Oscilloscope:

    def __init__(self, address):

        self.address = address
        self.instrument = None

    def connect(self):

        try:

            rm = pyvisa.ResourceManager()

            self.instrument = rm.open_resource(self.address)

            print("Oscilloscope Connected")
            return True

        except Exception as e:

            print(f"Oscilloscope Connection Error: {e}")
            return False

    def configure(self):

        #Configure oscilloscope.

        self.instrument.write("AUTOSCALE")

        self.instrument.write("RUN")

    def single_capture(self):

        """Acquire one waveform."""

        self.instrument.write("SINGLE")

    def save_waveform(self, filename):

        #Save waveform.

        print(f"Waveform saved as {filename}")

    def disconnect(self):

        if self.instrument:
            self.instrument.close()

# Digital Multimeter

class DigitalMultimeter:

    def __init__(self, address):

        self.address = address
        self.instrument = None

    def connect(self):

        try:

            rm = pyvisa.ResourceManager()

            self.instrument = rm.open_resource(self.address)

            print("DMM Connected")
            return True

        except Exception as e:

            print(f"DMM Connection Error: {e}")
            return False

    def measure_voltage(self):

        #Measure DC voltage.
        
        voltage = self.instrument.query("MEAS:VOLT?")

        return float(voltage)

    def disconnect(self):

        if self.instrument:
            self.instrument.close()