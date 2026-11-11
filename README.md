# Software Engineering Laboratory Portfolio (UE24CS351A)

**Department of Computer Science and Engineering | PES University (RR Campus)**  
**Student Name:** Saathvik Shenoy Padubidri  
**SRN:** PES1UG24CS394 (per1ug24cs394) | **Section:** 5th Sem, Section G  
**Faculty:** Dr. Sapna V M  
**Repository:** [https://github.com/saathviksp/L6_L7_30_vending_machine](https://github.com/saathviksp/L6_L7_30_vending_machine)  

---

## Laboratory Modules

| Lab Module | Topic | Primary Deliverables | Status |
|---|---|---|---|
| **[Lab 6](./lab6/)** | Code & Branch Coverage Analysis | `BranchCoverageTest_vending_machine.py`, `CodeCoverageTest_vending_machine.py`, `PES1UG24CS394_SE_Lab6_Code_and_Branch_Coverage.pdf` | **100% Branch Coverage Achieved** |
| **[Lab 7](./lab7/)** | Fuzz Testing for Input Validation (Hypothesis) | `vending_machine.py`, `processor.py`, `test_vending_machine.py`, `test_processor.py`, `PES1UG24CS394_SE_Lab7_Fuzz_Testing.pdf` | **100% Fuzz Tests Passing (Resilient to Edge Cases)** |

---

## Lab 7 Summary: Fuzzing for Input Validation Bugs

### Objective
Apply dynamic fuzz testing using the **Hypothesis** library to uncover latent input validation defects in a vending machine processing application, followed by hardening using defensive programming.

### Deliverables
1. **Academic PDF Report:** [`PES1UG24CS394_SE_Lab7_Fuzz_Testing.pdf`](./PES1UG24CS394_SE_Lab7_Fuzz_Testing.pdf) (Contains screenshots of Steps 2, 4, 5, 6, failure analysis, and rubric compliance).
2. **Hardened Application Code:** [`lab7/vending_machine.py`](./lab7/vending_machine.py) and [`lab7/processor.py`](./lab7/processor.py)
3. **Updated Test Suite:** [`lab7/test_vending_machine.py`](./lab7/test_vending_machine.py) and [`lab7/test_processor.py`](./lab7/test_processor.py)
4. **Terminal Screenshots:** [`lab7/screenshots/`](./lab7/screenshots/)

### Key Bugs Uncovered by Hypothesis
- `parse_coins(s)`: Crashed on `s=''` (`ValueError`) and `s=None` (`AttributeError`).
- `slot_position(s)`: Crashed on `s=''` (`IndexError`), `s='0'` (`ValueError`), `s=None` (`TypeError`), and German `'ß0'` (`TypeError: ord() expected char, len 2 found`).
- `change_due(s)`: Crashed on `s=''` (`ValueError: not enough values to unpack`), `s='/'` (`ValueError`), and `s=None` (`AttributeError`).

All bugs have been hardened and verified with 100% passing property-based tests.
