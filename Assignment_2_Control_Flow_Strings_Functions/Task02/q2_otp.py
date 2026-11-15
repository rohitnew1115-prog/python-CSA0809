"""Q2: OTP verification; blank input never consumes an attempt."""
OTP = "246810"

def verify_while(entries, correct=OTP, extra_attempts=False):
    limit, attempts, pos = 3 + (2 if extra_attempts else 0), 0, 0
    while attempts < limit:
        if pos >= len(entries):
            print("Input ended before attempt limit")
            return attempts, "incomplete"
        entered = entries[pos]; pos += 1
        if not entered.strip(): print("Blank entry: not counted"); continue
        attempts += 1
        if entered == correct: print("OTP verified"); break
        print("Incorrect OTP")
    else:
        print("Account locked for 30 minutes")
        return attempts, "locked"
    return attempts, "verified"

def verify_for(entries, correct=OTP, extra_attempts=False):
    limit, attempts, pos = 3 + (2 if extra_attempts else 0), 0, 0
    for _ in range(limit):
        while pos < len(entries) and not entries[pos].strip():
            print("Blank entry: not counted"); pos += 1
        if pos >= len(entries):
            print("Input ended before attempt limit"); return attempts, "incomplete"
        entered = entries[pos]; pos += 1; attempts += 1
        if entered == correct: print("OTP verified"); break
        print("Incorrect OTP")
    else:
        print("Account locked for 30 minutes")
        return attempts, "locked"
    return attempts, "verified"

def verify_recursive(entries, pos=0, attempts=0, limit=3, correct=OTP):
    if attempts >= limit: return "locked"
    if pos >= len(entries): return "incomplete"
    value = entries[pos]
    if not value.strip(): return verify_recursive(entries,pos+1,attempts,limit,correct)
    if value == correct: return "verified"
    return verify_recursive(entries,pos+1,attempts+1,limit,correct)

def main():
    cases = [("blank then success",["","111111","246810"],False,"verified",2),
             ("three wrong",["1","2","3"],False,"locked",3),
             ("early success",["246810","1"],False,"verified",1),
             ("blank entries do not count",[""," ","1","2","","3"],False,"locked",3),
             ("security answer grants two",["1","2","3","4","246810"],True,"verified",5)]
    for name, entries, extra, expected, count in cases:
        print("\n",name)
        for fn in (verify_while, verify_for):
            result = fn(entries, extra_attempts=extra)
            assert result == (count,expected), (fn.__name__,result)
            print(fn.__name__,result)
        assert verify_recursive(entries,limit=3+(2 if extra else 0)) == expected
    # pass is a deliberate no-op placeholder for an optional policy hook.
    optional_audit_hook = False
    if optional_audit_hook: pass
    print("break stops on success; continue skips blanks; pass is a no-op; loop-else locks only on exhaustion.")
    print("while is natural for unknown blank-input counts. Iterative O(a) time/O(1) space; recursion O(a) stack.")

if __name__ == '__main__': main()
