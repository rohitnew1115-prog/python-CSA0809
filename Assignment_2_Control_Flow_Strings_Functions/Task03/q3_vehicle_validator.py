"""Q3: String-only vehicle registration normalisation and validation."""
def normalise(text): return text.strip().replace(" ", "").replace("-", "").upper()

def validate(reg):
    if len(reg) not in (9,10): return False, "length must be 9 or 10"
    if not reg[0:2].isalpha(): return False, "state must be two letters"
    if not reg[2:4].isdigit(): return False, "district must be two digits"
    series = reg[4:-4]
    if len(series) not in (1,2) or not series.isalpha(): return False, "series must be one or two letters"
    if not reg[-4:].isdigit(): return False, "final section must be four digits"
    return True, "valid"

def format_receipt(reg):
    ok, _ = validate(reg)
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}" if ok else "INVALID"

def main():
    samples = ["tn 09 ab 1234","KA-01-M-0007","TN9AB1234","TN 22 1234 AB","mh 12 q 9876","DL-05-ZZ-4321","T1-09-AB-1234","TN-09-A1-1234","TN-09-AB-12X4"]
    for raw in samples:
        clean=normalise(raw); ok, reason=validate(clean)
        print(f"{raw:20} -> {clean:10} -> {format_receipt(clean) if ok else reason}")
        if raw.startswith("tn 09"): assert clean == "TN09AB1234" and format_receipt(clean)=="TN 09 AB 1234"
    text="tn 09 ab 1234"; changed=text.upper(); assert text != changed
    s="TN09AB1234"; print("text.upper() returns a new string:",text,"=>",changed)
    print("For 10 chars: s[-4:] =",s[-4:],"; s[4:-1] =",s[4:-1])
    print("For 6 chars: s[-4:] selects last four; s[4:-1] selects index 4 only.")
    print("Regex alternative: ^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$; both scan O(n), O(n) temporary slicing bound.")

if __name__ == '__main__': main()
