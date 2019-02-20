
def time_ranges(st, et):
    '''
    Given a start and end time, finds the military time
    hour ranges that complete the day. Example:
    st = 5, et = 20
    sts = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    ets = [20, 21, 23, 0, 1, 2, 3, 4]
    '''
    if st == et:
        return None, None
    elif st < 0 or st > 23 or et < 0 or et > 23:
        return None, None

    tst = st
    tet = et
    times = []
    for i in range(24):
        times.append(i)
    sts = []
    ets = []
    if st in times:
        sts.append(tst)
        tst+=1
        if tst == 24:
            tst = 0
        while tst is not et and tst in times:
            sts.append(tst)
            tst+=1
            if tst == 24:
                tst = 0

    if tet in times:
        ets.append(tet)
        tet+=1
        if tet == 24:
            tet = 0
        while tet is not st and tet in times:
            ets.append(tet)
            tet+=1
            if tet == 24:
                tet = 0

    return sts, ets
