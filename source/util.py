
def time_ranges(st, et):
    if st == et:
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
