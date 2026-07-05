"""
report.py

Generates a PDF report from the load transient test CSV file.
"""

import csv
import os
import statistics
from collections import defaultdict
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from config import CSV_FOLDER, REPORT_FOLDER


def generate_report(board_serial="SN-001",
                    operator="Test Engineer"):

    csv_file = os.path.join(
        CSV_FOLDER,
        "Load_Transient_Test_Results.csv"
    )

    report_file = os.path.join(
        REPORT_FOLDER,
        f"{board_serial}_Qualification_Report.pdf"
    )

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(report_file)

    elements = []

    # Title

    elements.append(
        Paragraph(
            "<b>Power Distribution Network Qualification Report</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph(f"Board Serial Number : {board_serial}",
                  styles["Normal"])
    )

    elements.append(
        Paragraph(
            f"Test Date : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Operator : {operator}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,20))

    # Instrument Details

    elements.append(
        Paragraph("<b>Test Equipment</b>",
                  styles["Heading2"])
    )

    equipment = [
        ["Power Supply",
         "Keithley 2230-30-1"],

        ["Electronic Load",
         "Keithley 2380"],

        ["Oscilloscope",
         "Keysight DSOX6004A"],

        ["Digital Multimeter",
         "Keithley DMM6500"]
    ]

    equipment_table = Table(equipment)

    equipment_table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),

        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    elements.append(equipment_table)

    elements.append(Spacer(1,20))

    # Read CSV

    rail_data = defaultdict(list)

    with open(csv_file, newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            rail_data[row["Rail"]].append(row)

    overall_pass = True

    # Rail Statistics

    for rail, measurements in rail_data.items():

        voltages = [
            float(m["Measured Voltage (V)"])
            for m in measurements
        ]

        currents = [
            float(m["Measured Current (A)"])
            for m in measurements
        ]

        pass_count = sum(
            1 for m in measurements
            if m["Status"] == "PASS"
        )

        fail_count = sum(
            1 for m in measurements
            if m["Status"] == "FAIL"
        )

        if fail_count > 0:
            overall_pass = False

        elements.append(
            Paragraph(
                f"<b>{rail}</b>",
                styles["Heading2"]
            )
        )

        table_data = [

            ["Average Voltage (V)",
             f"{statistics.mean(voltages):.3f}"],

            ["Minimum Voltage (V)",
             f"{min(voltages):.3f}"],

            ["Maximum Voltage (V)",
             f"{max(voltages):.3f}"],

            ["Average Current (A)",
             f"{statistics.mean(currents):.3f}"],

            ["Minimum Current (A)",
             f"{min(currents):.3f}"],

            ["Maximum Current (A)",
             f"{max(currents):.3f}"],

            ["PASS Count",
             str(pass_count)],

            ["FAIL Count",
             str(fail_count)]

        ]

        table = Table(table_data)

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ]))

        elements.append(table)

        elements.append(Spacer(1,20))

    # Overall Result

    result = "PASS" if overall_pass else "FAIL"

    elements.append(
        Paragraph(
            f"<b>Overall Result : {result}</b>",
            styles["Heading1"]
        )
    )

    document.build(elements)
    print(f"Report saved to {report_file}")