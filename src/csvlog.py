"""
csvlog.py

Logs load transient test results to a CSV file.
"""

import csv
import os

from config import (
    CSV_FOLDER,
    VOLTAGE_TOLERANCE
)

def save_results(results):
    #Save measurement results to CSV.

    # Create folder if it doesn't exist
    os.makedirs(CSV_FOLDER, exist_ok=True)

    csv_file = os.path.join(CSV_FOLDER, "Load_Transient_Test_Results.csv")

    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as file:

        writer = csv.writer(file)

        # Write header only once
        if not file_exists:

            writer.writerow([
    "Timestamp",
    "Rail",
    "Expected Voltage (V)",
    "Measured Voltage (V)",
    "Measured Current (A)",
    "Low Current (A)",
    "High Current (A)",
    "Waveform",
    "Status"
])

        # Write each measurement
        for result in results:

            expected = result["Expected Voltage"]
            measured = result["Measured Voltage"]

            lower_limit = expected * (1 - VOLTAGE_TOLERANCE)
            upper_limit = expected * (1 + VOLTAGE_TOLERANCE)

            if lower_limit <= measured <= upper_limit:
                status = "PASS"
            else:
                status = "FAIL"

            writer.writerow([
    result["Timestamp"],
    result["Rail"],
    expected,
    measured,
    result["Measured Current"],
    result["Low Current"],
    result["High Current"],
    result["Waveform"],
    status
])

    print(f"Results saved to {csv_file}")