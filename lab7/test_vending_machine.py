"""
test_vending_machine.py - Property-Based Fuzz Testing using Hypothesis
Lab 7: Fuzzing for Input Validation Bugs
Student Name: Saathvik Shenoy Padubidri
SRN: PES1UG24CS394
"""

import pytest
from hypothesis import given, strategies as st
from vending_machine import parse_coins, slot_position, change_due


# =====================================================================
# 1. Negative / Robustness Fuzz Tests (Arbitrary Text or None - No Crash)
# =====================================================================

@given(st.text() | st.none())
def test_parse_coins_no_crash(s):
    """
    Hypothesis fuzz test: parse_coins must never raise an unhandled exception
    on arbitrary strings, malformed delimiters, empty text, or None.
    """
    try:
        parse_coins(s)
    except Exception as e:
        assert False, f"parse_coins crashed with: {e}"


@given(st.text() | st.none())
def test_slot_position_no_crash(s):
    """
    Hypothesis fuzz test: slot_position must never raise an unhandled exception
    on arbitrary strings, out-of-range indices, multi-byte casing, or None.
    """
    try:
        slot_position(s)
    except Exception as e:
        assert False, f"slot_position crashed with: {e}"


@given(st.text() | st.none())
def test_change_due_no_crash(s):
    """
    Hypothesis fuzz test: change_due must never raise an unhandled exception
    on missing slashes, non-integer tokens, negative balances, or None.
    """
    try:
        change_due(s)
    except Exception as e:
        assert False, f"change_due crashed with: {e}"


# =====================================================================
# 2. Positive / Property Invariant Fuzz Tests (Valid Generated Domains)
# =====================================================================

@given(st.lists(st.integers(min_value=1, max_value=500), min_size=1, max_size=20))
def test_parse_coins_valid_inputs(coins):
    """
    Property invariant: Valid comma-separated positive integers must parse
    back into the exact list of integers.
    """
    csv_str = ",".join(str(c) for c in coins)
    result = parse_coins(csv_str)
    assert result == coins


@given(st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
       st.integers(min_value=1, max_value=99))
def test_slot_position_valid_inputs(char, col):
    """
    Property invariant: Valid slot codes (<letter><positive_int>) must correctly
    map to 0-indexed (row, column) coordinates.
    """
    code = f"{char}{col}"
    result = slot_position(code)
    expected_row = ord(char.upper()) - ord('A')
    expected_col = col - 1
    assert result == (expected_row, expected_col)


@given(st.integers(min_value=100, max_value=1000), st.integers(min_value=1, max_value=100))
def test_change_due_valid_inputs(paid, price):
    """
    Property invariant: Valid 'paid/price' inputs where paid >= price must
    correctly compute the number of five-coins.
    """
    payment = f"{paid}/{price}"
    result = change_due(payment)
    expected_coins = (paid - price) // 5
    assert result == f"{expected_coins} five-coins"
