import pytest
from vending_machine import select_item, make_change, purchase


# ==========================================
# 1. Tests for select_item
# ==========================================

def test_invalid_item():
    """Branch: item not in PRICES (True)."""
    assert select_item("water", {}, 100) == "invalid"


def test_select_item_invalid_with_stock():
    """Branch: item not in PRICES even if provided in stock dict."""
    assert select_item("unknown", {"unknown": 10}, 100) == "invalid"


def test_sold_out():
    """Branch: item in stock dict but quantity is 0."""
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_select_item_sold_out_missing_key():
    """Branch: item key absent from stock dict (evaluates stock.get to 0)."""
    assert select_item("chips", {}, 100) == "sold_out"


def test_insufficient_credit():
    """Branch: credit < PRICES[item] (True)."""
    assert select_item("chips", {"chips": 3}, 50) == "insufficient"


def test_select_item_success():
    """Branch: item in PRICES, stock > 0, credit >= price."""
    assert select_item("candy", {"candy": 5}, 75) == "ok"


# ==========================================
# 2. Tests for make_change
# ==========================================

def test_no_change_needed():
    """Branch: amount == 0 returns empty list immediately."""
    assert make_change(0) == []


def test_make_change_negative_raises_error():
    """Branch: amount < 0 (True) raises ValueError."""
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-10)


def test_make_change_valid_combination():
    """Branch: greedy coin breakdown spanning multiple denominations."""
    # 175 = 100 + 50 + 25
    assert make_change(175) == [100, 50, 25]


def test_make_change_single_coin_denominations():
    """Branch: each individual coin denomination matched."""
    assert make_change(100) == [100]
    assert make_change(50) == [50]
    assert make_change(25) == [25]
    assert make_change(10) == [10]
    assert make_change(5) == [5]


def test_make_change_multiple_same_coins():
    """Branch: while loop executes multiple iterations per coin value."""
    assert make_change(200) == [100, 100]
    assert make_change(20) == [10, 10]


def test_make_change_impossible_amount():
    """Branch: amount > 0 remaining after all coins (returns None)."""
    assert make_change(3) is None
    assert make_change(7) is None
    assert make_change(1) is None


# ==========================================
# 3. Tests for purchase
# ==========================================

def test_purchase_success():
    """Branch: successful purchase with change dispensed."""
    stock = {"chips": 2}
    status, change = purchase("chips", stock, 150)
    assert status == "dispensed"
    assert change == [50]
    assert stock["chips"] == 1


def test_purchase_success_exact_change():
    """Branch: successful purchase with exact payment (change is empty)."""
    stock = {"candy": 2}
    status, change = purchase("candy", stock, 75)
    assert status == "dispensed"
    assert change == []
    assert stock["candy"] == 1


def test_purchase_status_not_ok():
    """Branch: select_item fails during purchase (e.g. sold out)."""
    stock = {"cola": 0}
    status, change = purchase("cola", stock, 200)
    assert status == "sold_out"
    assert change == []


def test_purchase_status_insufficient_credit():
    """Branch: select_item fails during purchase due to insufficient credit."""
    stock = {"chips": 2}
    status, change = purchase("chips", stock, 25)
    assert status == "insufficient"
    assert change == []
    assert stock["chips"] == 2


def test_purchase_no_exact_change_available():
    """Branch: make_change returns None -> returns 'no_exact_change' without decrementing stock."""
    stock = {"candy": 4}
    # Candy costs 75. 78 - 75 = 3 credit change, which cannot be formed from coins [100, 50, 25, 10, 5].
    status, change = purchase("candy", stock, 78)
    assert status == "no_exact_change"
    assert change == []
    assert stock["candy"] == 4
