"""
Hardened vending_machine.py for Lab 7 (Fuzz Testing)
Handles arbitrary unexpected, malformed, and edge-case inputs without crashing.
"""

def parse_coins(coins_csv):
    """
    Parses a comma-separated string of coin values into a list of integers.
    Hardened against: None, non-string, empty strings, spaces, non-numeric entries, and negatives.
    """
    if not isinstance(coins_csv, str):
        return []
    coins = []
    for part in coins_csv.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            val = int(part)
            if val > 0:
                coins.append(val)
        except ValueError:
            continue
    return coins

def slot_position(code):
    """
    Parses a vending machine slot code (e.g. 'B7') into a 0-indexed (row, column) tuple.
    Hardened against: None, non-string, empty strings, multi-byte casing (e.g. 'ß'),
    missing digits, non-alphabetic row letters, invalid columns.
    """
    if not isinstance(code, str):
        return None
    code = code.strip()
    if len(code) < 2:
        return None
    first_char = code[0]
    if not (('A' <= first_char <= 'Z') or ('a' <= first_char <= 'z')):
        return None
    row = ord(first_char.upper()) - ord('A')
    col_str = code[1:]
    try:
        col_num = int(col_str)
        if col_num < 1:
            return None
        column = col_num - 1
    except ValueError:
        return None
    return row, column

def change_due(payment):
    """
    Calculates the change due formatted as five-coins from a 'paid/price' string (e.g. '200/150').
    Hardened against: None, non-string, missing slash, non-integer values, negative amounts, underpayment.
    """
    if not isinstance(payment, str):
        return "0 five-coins"
    parts = payment.strip().split('/')
    if len(parts) != 2:
        return "0 five-coins"
    try:
        paid = int(parts[0].strip())
        price = int(parts[1].strip())
    except ValueError:
        return "0 five-coins"
    if paid < 0 or price < 0:
        return "0 five-coins"
    change = paid - price
    if change < 0:
        return "0 five-coins"
    return str(change // 5) + ' five-coins'

def main():
    print("==== Running parse_coins ====")
    user_input = input("Enter coin values as CSV (e.g. 5,10,25): ")
    result = parse_coins(user_input)
    print("Coins:", result)

    print("\n==== Running slot_position ====")
    user_input = input("Enter a slot code (e.g. B7): ")
    result = slot_position(user_input)
    print("Row and Column:", result)

    print("\n==== Running change_due ====")
    user_input = input("Enter paid/price (e.g. 200/150): ")
    result = change_due(user_input)
    print("Change Due:", result)

if __name__ == "__main__":
    main()
