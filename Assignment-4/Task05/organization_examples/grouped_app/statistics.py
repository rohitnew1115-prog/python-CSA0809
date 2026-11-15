"""Grouped-module form: basic attendance statistics."""
def present_percent(rows):
    total=len(rows); present=sum(row[2]=="P" for row in rows)
    return present/total*100 if total else 0.0
