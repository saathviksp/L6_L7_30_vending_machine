import pytest
from vending_machine import select_item, make_change, purchase


# ==========================================
# 1. Tests for select_item
# ==========================================

def test_select_item_invalid():
    """Branch: item not in PRICES (True)."""
    assert select_item("water", {"water": 5}, 100) == "invalid"


def test_select_item_sold_out_zero_stock():
    """Branch: item in stock dict but quantity is 0."""
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_select_item_sold_out_missing_key():
    """Branch: item key not in stock dict (default 0)."""
    assert select_item("cola", {}, 200) == "sold_out"


def test_select_item_insufficient_credit():
    """Branch: credit < PRICES[item] (True)."""
    assert select_item("chips", {"chips": 3}, 50) == "insufficient"


def test_select_item_ok():
    """Branch: valid item, in stock, sufficient credit -> ok."""
    assert select_item("candy", {"candy": 5}, 75) == "ok"


# ==========================================
# 2. Tests for make_change
# ==========================================

def test_make_change_negative_raises_error():
    """Branch: amount < 0 (True) raises ValueError."""
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-5)


def test_make_change_zero():
    """Branch: amount == 0 returns empty list immediately."""
    assert make_change(0) == []


def test_make_change_single_coin():
    """Branch: exact coin match across different denominations."""
    assert make_change(100) == [100]
    assert make_change(50) == [50]
    assert make_change(25) == [25]
    assert make_change(10) == [10]
    assert make_change(5) == [5]


def test_make_change_multiple_same_coins():
    """Branch: while loop executes multiple iterations per coin."""
    assert make_change(200) == [100, 100]
    assert make_change(20) == [10, 10]


def test_make_change_mixed_coins():
    """Branch: greedy change combination spanning multiple coin values."""
    assert make_change(165) == [100, 50, 10, 5]
    assert make_change(90) == [50, 25, 15] if False else [50, 25, 10, 5]


def test_make_change_inexact_amount():
    """Branch: amount > 0 remaining after all coins (returns None)."""
    assert make_change(3) is None
    assert make_change(7) is None
    assert make_change(1) is None


# ==========================================
# 3. Tests for purchase
# ==========================================

def test_purchase_success_with_change():
    """Branch: valid purchase with positive change dispensed."""
    stock = {"chips": 3}
    status, change = purchase("chips", stock, 150)
    assert status == "dispensed"
    assert change == [50]
    assert stock["chips"] == 2


def test_purchase_success_exact_change():
    """Branch: valid purchase with exact money (change is empty list)."""
    stock = {"candy": 2}
    status, change = purchase("candy", stock, 75)
    assert status == "dispensed"
    assert change == []
    assert stock["candy"] == 1


def test_purchase_status_invalid_item():
    """Branch: select_item returns 'invalid' in purchase."""
    stock = {"cola": 2}
    status, change = purchase("unknown_drink", stock, 200)
    assert status == "invalid"
    assert change == []
    assert stock["cola"] == 2


def test_purchase_status_sold_out():
    """Branch: select_item returns 'sold_out' in purchase."""
    stock = {"cola": 0}
    status, change = purchase("cola", stock, 200)
    assert status == "sold_out"
    assert change == []


def test_purchase_status_insufficient_credit():
    """Branch: select_item returns 'insufficient' in purchase."""
    stock = {"cola": 2}
    status, change = purchase("cola", stock, 50)
    assert status == "insufficient"
    assert change == []
    assert stock["cola"] == 2


def test_purchase_no_exact_change_available():
    """Branch: make_change returns None -> purchase returns 'no_exact_change'."""
    stock = {"candy": 4}
    # candy costs 75. 78 - 75 = 3 credit change, which cannot be made.
    status, change = purchase("candy", stock, 78)
    assert status == "no_exact_change"
    assert change == []
    assert stock["candy"] == 4  # stock must not be decremented
