"""
main.py

Main program for automated PDN load transient testing.
"""

from config import (
    POWER_SUPPLY_ADDRESS,
    ELECTRONIC_LOAD_ADDRESS,
    OSCILLOSCOPE_ADDRESS,
    DMM_ADDRESS,
    RAILS
)

from instruments import (
    PowerSupply,
    ElectronicLoad,
    Oscilloscope,
    DigitalMultimeter
)

from transient_test import run_transient_test
from csvlog import save_results
from report import generate_report


def main():

    print("\nPDN Load Transient Test\n")

    # Create Instrument Objects

    psu = PowerSupply(POWER_SUPPLY_ADDRESS)

    eload = ElectronicLoad(ELECTRONIC_LOAD_ADDRESS)

    scope = Oscilloscope(OSCILLOSCOPE_ADDRESS)

    dmm = DigitalMultimeter(DMM_ADDRESS)

    # Connect Instruments

    if not all([
        psu.connect(),
        eload.connect(),
        scope.connect(),
        dmm.connect()
    ]):
        print("\nInstrument connection failed. Exiting program.")
        return

    # Board Details

    board_serial = input("Enter Board Serial Number : ")

    operator = input("Enter Operator Name : ")

    # Test Every Rail

    for rail in RAILS:

        input(
            f"\nConnect probes to {rail['name']} rail and press Enter..."
        )

        results = run_transient_test(

            psu,

            eload,

            scope,

            dmm,

            rail["name"],

            rail["voltage"],

            rail["max_current"]

        )

        save_results(results)

    # Generate Report

    generate_report(

        board_serial=board_serial,

        operator=operator

    )

    # Disconnect Instruments

    psu.disconnect()

    eload.disconnect()

    scope.disconnect()

    dmm.disconnect()

    print("\nTesting Completed Successfully.")

if __name__ == "__main__":

    main()