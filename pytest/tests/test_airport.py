import pytest
import csv
from airport.checkin import Suitcase, Gate

GATE1 = Gate(53, 12000)
GATE2 = Gate(1827, 1738)

def fake_check_price(gate: Gate, suitcase : Suitcase):
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
    suitcase1 = Suitcase(600, 50, 50)
    suitcase2 = Suitcase(100, 100, 100)
    assert GATE1.check_price(suitcase1) == 543.21
    assert GATE2.check_price(suitcase2) == 124.45



# TODO:
# 1. Create a Suitcase object that can pass through the global GATE1 (can_pass_gate returns True).
# 2. Write another test case where a Suitcase cannot pass through GATE1 (can_pass_gate returns False).
# 3. Use the result_collector fixture to record both results and ensure they are saved to the output CSV file.
def test_gate1(result_collector):
    fit_suitcase = Suitcase(10, 43, 100)
    fit_result = GATE1.can_pass_gate(fit_suitcase.width, fit_suitcase.height)
    # records will look like {"length": "", width: "", height: "", result: ""}
    result_collector.append(
        {"length": str(fit_suitcase.length), "width": str(fit_suitcase.width), "height": str(fit_suitcase.height),
         "result": str(fit_result)})
    unfit_suitcase = Suitcase(10, 100, 100)
    unfit_result = GATE1.can_pass_gate(unfit_suitcase.width, unfit_suitcase.height)
    result_collector.append(
        {"length": str(unfit_suitcase.length), "width": str(unfit_suitcase.width), "height": str(unfit_suitcase.height),
         "result": str(unfit_result)})


# TODO:
# 1. Create a Suitcase object that can pass through the global GATE2 (can_pass_gate returns True).
# 2. Write another test case where a Suitcase cannot pass through GATE2 (can_pass_gate returns False).
# 3. Use the result_collector fixture to record both results and ensure they are saved to the output CSV file.
def test_gate2(result_collector):
    fit_suitcase = Suitcase(10, 1000, 1000)
    fit_result = GATE2.can_pass_gate(fit_suitcase.width, fit_suitcase.height)
    result_collector.append(
        {"length": str(fit_suitcase.length), "width": str(fit_suitcase.width), "height": str(fit_suitcase.height),
         "result": str(fit_result)})

    unfit_suitcase = Suitcase(10, 1828, 1739)
    unfit_result = GATE2.can_pass_gate(unfit_suitcase.width, unfit_suitcase.height)
    result_collector.append(
        {"length": str(unfit_suitcase.length), "width": str(unfit_suitcase.width), "height": str(unfit_suitcase.height),
         "result": str(unfit_result)})

