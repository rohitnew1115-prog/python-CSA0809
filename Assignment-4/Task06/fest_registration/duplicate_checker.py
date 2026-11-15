"""Track accepted register numbers with an average O(1) set lookup."""


def accept_once(register_number, seen):
    if register_number in seen:
        return False
    seen.add(register_number)
    return True
