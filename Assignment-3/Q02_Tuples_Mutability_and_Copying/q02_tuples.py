"""Tuple identity, grid aliasing, copying and measurement."""
import copy, sys, timeit
def main():
    rows,cols=3,4; bad=[[0]*cols]*rows; bad[0][1]=7
    good=[[0 for _ in range(cols)] for _ in range(rows)]; good[0][1]=7
    print('bad:',bad); print('good:',good)
    a=(13.04818,80.82341); print('tuple comparison:',a==(13.04818,80.82341),a==(13.0,80.82341))
    stops={(13.04818,80.82341):'T. Nagar'}; print(stops[(13.04818,80.82341)])
    print('bad row identities:',[id(r) for r in bad]); print('good row identities:',[id(r) for r in good])
    shallow=copy.copy(good); deep=copy.deepcopy(good); shallow[1][1]=4; print('shallow affects source:',good[1][1]==4,'deep independent:',deep[1][1]==0)
    print('unpacking:',[(lat,lon) for lat,lon in [a]])
    values=list(range(1_000_000)); tup=tuple(values); print('container bytes:',sys.getsizeof(values),sys.getsizeof(tup),'(elements shared; shallow sizes)')
    print('creation seconds:',timeit.timeit('list(range(100000))',number=5),timeit.timeit('tuple(range(100000))',number=5))
    try: (['mutable'],)[0].append('inside')
    finally: print('mutable element in tuple:',(['mutable','inside'],))
    print('tuple keys need immutable/hashable elements; list keys are mutable/unhashable. list argument mutation affects caller because both names reference same object.')
    print('grid choices: list-of-lists O(1) access, O(r*c) space including empty cells; dict[(r,c)] average O(1), O(k) space for k occupied cells, but coordinate validation needed.')
if __name__=='__main__': main()
