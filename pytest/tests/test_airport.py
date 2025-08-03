import pytest
import csv
from ..airport.checkin import Suitcase, Gate

GATE1 = Gate(53, 12000)
GATE2 = Gate(1827, 1738)

def fake_check_price(suitcase : Suitcase):
    if suitcase.width > 500 or suitcase.height > 500 or suitcase.length > 500:
        return 543.21
    else:
        return 124.45

def test_gate_output(mocker):
    # TODO:
    # Use mocker.patch.object to override the check_price method of the Gate class.
    # If any dimension of the suitcase is greater than 500, it should return "543.21".
    # Otherwise, it should return "124.45".
    # Write two assert statements to check the output of the check_price method for two different Suitcase objects.
    mocker.patch.object(Gate, "check_price", new=fake_check_price)




# TODO:
# 1. Create a Suitcase object that can pass through the global GATE1 (can_pass_gate returns True).
# 2. Write another test case where a Suitcase cannot pass through GATE1 (can_pass_gate returns False).
# 3. Use the result_collector fixture to record both results and ensure they are saved to the output CSV file.
def test_gate1():
    fitSuitcase = Suitcase(10, 43, 100)
    fitResult = GATE1.can_pass_gate(fitSuitcase.width, fitSuitcase.height)
    # records will look like {"length": "", width: "", height: "", result: ""}
    result_collector.add(
        {"length": str(fitSuitcase.length), "width": str(fitSuitcase.width), "height": str(fitSuitcase.height),
         "result": str(fitResult)})
    unfitSuitcase = Suitcase(10, 100, 100)
    unfitResult = GATE1.can_pass_gate(unfitSuitcase.width, unfitSuitcase.height)
    result_collector.add(
        {"length": str(unfitSuitcase.length), "width": str(unfitSuitcase.width), "height": str(unfitSuitcase.height),
         "result": str(unfitResult)})


# TODO:
# 1. Create a Suitcase object that can pass through the global GATE2 (can_pass_gate returns True).
# 2. Write another test case where a Suitcase cannot pass through GATE2 (can_pass_gate returns False).
# 3. Use the result_collector fixture to record both results and ensure they are saved to the output CSV file.
def test_gate2():
    fitSuitcase = Suitcase(10, 1000, 1000)
    fitResult = GATE2.can_pass_gate(fitSuitcase.width, fitSuitcase.height)
    result_collector.add(
        {"length": str(fitSuitcase.length), "width": str(fitSuitcase.width), "height": str(fitSuitcase.height),
         "result": str(fitResult)})

    unfitSuitcase = Suitcase(10, 1828, 1739)
    unfitResult = GATE2.can_pass_gate(unfitSuitcase.width, unfitSuitcase.height)
    result_collector.add(
        {"length": str(unfitSuitcase.length), "width": str(unfitSuitcase.width), "height": str(unfitSuitcase.height),
         "result": str(unfitResult)})

