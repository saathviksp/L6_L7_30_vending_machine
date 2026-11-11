# Lab 7: Fuzzing for Input Validation Bugs

**Department of Computer Science and Engineering | PES University (RR Campus)**  
**Course:** Software Engineering (UE24CS351A)  
**Student Name:** Saathvik Shenoy Padubidri  
**SRN:** PES1UG24CS394 (per1ug24cs394) | **Section:** 5th Sem, Section G  
**Faculty:** Dr. Sapna V M  
**Assigned Module:** `vending_machine.py` / `processor.py`  
**Repository:** [https://github.com/saathviksp/L6_L7_30_vending_machine](https://github.com/saathviksp/L6_L7_30_vending_machine)  

---

## 1. Overview & Objectives

The primary objective of this laboratory is to explore **fuzz testing (property-based testing)** as a dynamic security and quality assurance technique using Python's **Hypothesis** library. Unlike standard unit testing which only evaluates expected happy-path scenarios, property-based fuzzers generate high volumes of randomized, malformed, and degenerate inputs to discover unhandled exceptions, algorithmic crashes, and boundary condition bugs.

### Fuzz Testing Methodology
1. **Property Formulation:** Define invariants and non-crashing behaviors using `@given` decorators with Hypothesis strategies (`st.text() | st.none()`, `st.lists()`, `st.integers()`).
2. **Automated Fuzzing & Shrinking:** Hypothesis feeds random data and, upon discovering an unhandled exception, executes shrinking algorithms to locate the minimal reproducible failing counterexample.
3. **Defensive Hardening:** Apply input validation guards, type checks, and structured exception handling to harden the functions against adversarial and malformed inputs.
4. **Re-Verification:** Re-execute the complete property-based test suite to ensure 100% test passing and fault tolerance.

---

## 2. Repository Deliverables

| Deliverable File | Description | Verification Status |
|---|---|---|
| `vending_machine.py` / `processor.py` | Hardened application code implementing input validation guards | Completed & Tested |
| `test_vending_machine.py` / `test_processor.py` | Property-based fuzz test suite using Hypothesis (6 tests) | 100% Passed (12/12) |
| `PES1UG24CS394_SE_Lab7_Fuzz_Testing.pdf` | Academic submission report with screenshots & analysis | Generated & Verified |
| `screenshots/` | Terminal output captures across all lab steps (Steps 2, 4, 5, 6) | High Resolution PNGs |

---

## 3. Vulnerability Diagnosis & Minimal Falsifying Inputs

| Function | Minimal Counterexample | Exception Triggered | Underlying Defect & Remediation |
|---|---|---|---|
| `parse_coins(s)` | `s = ''`<br/>`s = None` | `ValueError: invalid literal for int`<br/>`AttributeError: 'NoneType' object has no attribute 'split'` | Empty string produces `['']` breaking `int('')`; `None` cannot be split. **Fix:** Added `isinstance(s, str)` check and per-token `try-except ValueError`. |
| `slot_position(s)` | `s = ''`<br/>`s = '0'`<br/>`s = None`<br/>`s = 'ß0'` | `IndexError: string index out of range`<br/>`ValueError: invalid literal for int`<br/>`TypeError: 'NoneType' not subscriptable`<br/>`TypeError: ord() expected char, len 2 found` | Indexing empty/None strings crashes; single-digit leaves empty column string; German `'ß'.upper()` expands to `'SS'` breaking `ord()`. **Fix:** ASCII range check `'A' <= char <= 'Z'` and length guard `>= 2`. |
| `change_due(s)` | `s = ''`<br/>`s = '/'`<br/>`s = None` | `ValueError: not enough values to unpack`<br/>`ValueError: invalid literal for int`<br/>`AttributeError: 'NoneType' object has no attribute 'split'` | Missing delimiter fails unpacking; naked slash produces empty string tokens; `None` has no split. **Fix:** Validate `len(parts) == 2`, convert safely, and guard negative balances. |

---

## 4. Execution Commands

### Step 1: Install Dependencies
```powershell
pip install hypothesis pytest
```

### Step 2: Run Buggy Application
```powershell
python processor.py
# (or: python vending_machine.py)
```

### Step 3 & 4: Run Fuzz Tests (Discovering Failures)
```powershell
pytest test_processor.py
# (or: pytest test_vending_machine.py)
```

### Step 5: Run Hardened Application
```powershell
python processor.py
```

### Step 6: Re-Verify Hardened Code with Hypothesis
```powershell
pytest -v test_processor.py
pytest -v test_vending_machine.py
```
