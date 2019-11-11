.md.minDTime:00:00:00.0002p;
.md.maxDTime:00:00:00.02p;
.md.CTS:11;
.md.UTDF:10;

.md.tradeMatch:{[day;xchng;sid]
    symbols:$[xchng="Z"; .BATS.symbols; xchng="Q"; .NASDAQ.symbols; xchng="N"; .NYSE.symbols; xchng in "PT"; .ARCA.symbols];
    symids:.md.getSymID[`date$day] each symbols;
    trds:`time xasc update ttime:time from update "P"$string time from select from .md.trade where date=day, ex=xchng, size>100, src=sid, symbolid in symids;
    excs:`time xasc update "P"$string time from select date, size, time, symbolid, orderid, oprice:price from .md.orders where date=day, ex=xchng, mt within (9;12), size>100, symbolid in symids;
    w:"P"$strin g (.md.minDTime;.md.maxDTime)+\:excs[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from
        wj[w;`symbolid`size`time;excs;(trds;(::;`ttime))]}
        

//.md.genBboZ18:`:crm.ath:5018 "genBboZ18"
//.md.genBboZ18:`:crm.ath:5018 "res"

.md.genBbo: delete ttime from update time:ttime, "i"$ask, "i"$bid, "i"$asize%100, "i"$bsize%100 from `ttime xasc .md.genBbo;

.md.bboMatch:{[day;xchng;sid]
    symbols:$[xchng="Z"; .BATS.symbols; xchng="Q"; .NASDAQ.symbols; xchng="N"; .NYSE.symbols; xchng in "PT"; .ARCA.symbols];
    symids:.md.getSymID[`date$day] each symbols;
    symids:exec distinct symbolid from .md.genBbo where date=day, ex=xchng;
    bbo:`time xasc update ttime:time from update "P"$string time from select from .md.bbo where date=day, ex=xchng, src=sid, symbolid in symids;
    genbbo:`time xasc update "P"$string time from select date,time, symbolid, bidvol:bsize, bidprice:bid, askvol:asize, askprice:ask from .md.genBbo where date=day, ex=xchng, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:genbbo[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from
        wj[w;`symbolid`bidvol`bidprice`askvol`askprice`time;genbbo;(bbo;(::;`ttime))]}

//.md.genBbo:.md.genBboP,.md.genBboQ,.md.genBboZ

.res.genBboZ18:.md.bboMatch [7226;"Z";73]

{update r:100*nm%m from select nm:count i[where null td], m:count i by symbolid from x} .res.genBboZ18

{update r:100*nm%m from select nm:count i[where null td], m:count i by symbolid from x} .res.genBboZ18
select med td, avg td, sdev td from .tmp.tm where not null td
select `time$time, `long$td from .tmp.tm where not null td

