import pytest
from vending_machine import select_item, make_change, purchase

# Example test cases from starter code:
def test_invalid_item():
    assert select_item("water", {}, 100) == "invalid"


def test_no_change_needed():
    assert make_change(0) == []


# Additional test cases to achieve >90% code coverage:
def test_sold_out():
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_insufficient_credit():
    assert select_item("chips", {"chips": 3}, 50) == "insufficient"


def test_select_item_success():
    assert select_item("candy", {"candy": 5}, 100) == "ok"


def test_make_change_valid_combination():
    # 175 = 100 + 50 + 25
    assert make_change(175) == [100, 50, 25]


def test_make_change_negative_raises_error():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-10)


def test_purchase_success():
    stock = {"chips": 2}
    status, change = purchase("chips", stock, 150)
    assert status == "dispensed"
    assert change == [50]
    assert stock["chips"] == 1


def test_purchase_status_not_ok():
    stock = {"cola": 0}
    status, change = purchase("cola", stock, 200)
    assert status == "sold_out"
    assert change == []
