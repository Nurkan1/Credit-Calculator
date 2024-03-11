
# Requirements for the Credit Calculation Program

This document outlines the setup required to run the Credit Calculation Program successfully. This Python script facilitates the calculation of loan details, including monthly payments and amortization schedules, enhancing personal finance management.

## Python Version

- Python 3.8 or above is recommended to ensure full compatibility with the script's features.

## Dependencies

The script utilizes the following Python Standard Library modules:
- `math` for mathematical operations,
- `locale` for localizing numbers,
- `os` for interacting with the operating system,
- `subprocess` for invoking an external subprocess,
- `datetime` for managing dates and times.

These modules are included with Python; no additional installations are required.

## Setup Instructions

Ensure Python 3.8 or later is installed on your system. You can verify this by running:
```bash
python --version
```
If Python is not installed or an older version is detected, please install or update Python from the [official Python website](https://www.python.org/downloads/).

## Running the Script

To run the Credit Calculation Program, navigate to the script's directory and execute:
```bash
python credit_calculation_program.py
```
Replace `credit_calculation_program.py` with the actual script name if different.

## Additional Notes

- The program uses `locale.setlocale(locale.LC_ALL, '')` to format numbers according to your system's locale. Ensure your system locale is correctly set for accurate number formatting.
- Ensure write permissions to the directory where the script is run, as it generates output files.

## Troubleshooting

If you encounter any issues with the standard library modules, verify your Python installation and consult the [Python documentation](https://docs.python.org/3/library/) for assistance.
