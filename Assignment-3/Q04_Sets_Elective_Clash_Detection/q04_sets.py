"""Elective registration set analysis."""
a1_elective=['192311001','192311004','192311007','192311009']; b1_elective=['192311002','192311004','192311009','192311010']
all_students=['192311001','192311002','192311004','192311007','192311009','192311010','192311003','192311005','192311006','192311008']
def main():
    a,b,all_s=map(set,(a1_elective,b1_elective,all_students))
    op=(a&b,a^b,all_s-(a|b)); meth=(a.intersection(b),a.symmetric_difference(b),all_s.difference(a.union(b)))
    print('clash:',sorted(op[0])); print('exactly_one:',sorted(op[1])); print('neither:',sorted(op[2])); print('operators equal methods:',op==meth)
    print('Venn: intersection is center; symmetric difference is both outer-only regions; neither lies outside both circles but inside all_students.')
    print('duplicates collapse by hashing; average set membership O(1), list membership O(n); tuples can be set members when elements hashable, lists cannot.')
    print('small manual:',{1,2}&{2,3},{1,2}^{2,3},{1,2,3}-{1,2})
    print('empty:',set()&set(),'identical symmetric difference:',{1,2}^{1,2})
    duplicate_regs=['192311001','192311001','192311004']; print('duplicates removed:',sorted(set(duplicate_regs)))
    print('complexity: nested pairwise O(n*m), O(1) extra; sort-and-walk O(n log n+m log m), O(n+m) depending copies; set operations average O(n+m), O(n+m) space.')
    print('conversion to set removes duplicates and ordering/multiplicity information.')
if __name__=='__main__': main()
