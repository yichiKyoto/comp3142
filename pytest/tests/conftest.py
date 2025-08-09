import pytest
import csv
from airport.checkin import Suitcase, Gate



RESULT_FILE = "test_results.csv"
@pytest.fixture(scope="session")
def result_collector():
    # TODO:
    # Implement the logger fixture to collect results in a shared list and save to a CSV file (only one csv file).
    # The output CSV must have the following header and format:
    # length,width,height,result
    # 1,2,3,True (This is an example, including this comment, you don't need to write this in the file)
    # Each row should correspond to one test case.

    # --- setup ---
    records = []

    with open(RESULT_FILE, "w", newline="") as f:
        f.write("length,width,height,result\n")

    yield records

    # --- teardown ---
    with open(RESULT_FILE, "a", newline="") as f:
        for record in records:
            f.write(f"{record['length']},{record['width']},{record['height']},{record['result']}\n")