export const getHourRanges = (st, et) => {

    if(st === et) {
        return [null, null]
    }

    let times = []
    for(let i = 0; i < 24; i++) {
      times.push(i);
    }

    let tst = st
    let tet = et
    let sts = []
    let ets = []
    if(times.indexOf(st) !== -1) {
        sts.push(tst)
        tst+=1
        if(tst === 24){
            tst = 0
        }
        while(tst !== et && times.indexOf(tst) !== -1) {
          sts.push(tst)
          tst+=1
          if(tst === 24) {
            tst = 0
          }
        }
    }

    if(times.indexOf(tet) !== -1) {
      ets.push(tet);
      tet+=1
      if(tet === 24) {
        tet = 0
      }
      while(tet !== st && times.indexOf(tet) !== -1) {
        ets.push(tet)
        tet+=1
        if(tet === 24) {
          tet = 0
        }
      }
    }

    return [sts, ets]
}

export default {
  getHourRanges
}
