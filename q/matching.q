
`:symbolism.bo.ath:5001 "indxFAfile[2019.09.28;`AAPL]"
(hsym `$"symbolism-main.bo.ath:5001") ({[x;y] indxFAfile[x;y]};2019.09.28;`AAPL)

.md.getSymID:{[day; name]
        (hsym `$"symbolism-main.bo.ath:5001") ({[x;y] indxFAfile[x;y]};day;name)
        }
                
.md.minDTime:00:00:00.000002p;
.md.maxDTime:00:00:00.002p;
.md.CTS:11;
.md.UTDF:10;
.md.CQS:72;
.md.UQDF:73;
.md.allEx:(select distinct exchange from .md.symbols)`exchange;

.md.tradeMatch:{[day;xchng;sid]
    symbols:$[xchng="Z"; .BATS.symbols; xchng="Q"; .NASDAQ.symbols; xchng="N"; .NYSE.symbols; xchng in "PT"; .ARCA.symbols];
    symids:.md.getSymID[`date$day] each symbols;
    trds:`time xasc update ttime:time from update "P"$string time from select from .md.trade where date=day, ex=xchng, size>100, src=sid, symbolid in symids;
    excs:`time xasc update "P"$string time from select date, size, time, symbolid, orderid, oprice:price from .md.orders where date=day, ex=xchng, mt in (9 10 11 12 19 20), size>100, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:excs[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from wj[w;`symbolid`size`time;excs;(trds;(::;`ttime))]}

.md.tradeMatchListed:{[day;xchng;sid;listedOn]
    symids:(,/){.md.getSymID[`date$x; y]}[day;] each (0!select from .EDGA.symbols where exchange in listedOn)`ticker;
    trds:`time xasc update ttime:time from update "P"$string time from select from .md.trade where date=day, ex=xchng, size>100, src=sid, symbolid in symids;
/     xchngExec:"Q";
/     xchngExec:xchng;
/     excs:`time xasc update "P"$string time from select date, size, time, symbolid, orderid, oprice:price from .md.orders where date=day, ex=xchngExec, mt in (9 10 11 12 19 20), size>100, symbolid in symids;
    excs:`time xasc update "P"$string time from select date, size, time, symbolid, orderid, oprice:price from .md.orders where date=day, mt in (9 10 11 12 19 20), size>100, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:excs[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from wj[w;`symbolid`size`time;excs;(trds;(::;`ttime))]}
 
.res.CTS_P:raze .md.tradeMatch[; "P"; .md.CTS] peach 7226 + til 5
.res.CTS_Z:raze .md.tradeMatchListed[; "Z"; .md.CTS; .md.allEx] peach 7226 + til 5
.res.UTDF_Q:raze .md.tradeMatch[ ; "Q"; .md.UTDF] peach 7226 + til 5
.res.CTS_P_P:raze .md.tradeMatchListed[; "P"; .md.CTS; `P] peach 7226 + til 5
.res.CTS_P_Z:raze .md.tradeMatchListed[; "P"; .md.CTS; `Z] peach 7226 + til 5
.res.CTS_P_N:raze .md.tradeMatchListed[; "P"; .md.CTS; `N] peach 7226 + til 5
.res.UTDF_P_Q:raze .md.tradeMatchListed[; "P"; .md.UTDF; `Q] peach 7226 + til 5

select from .md.trade where date=7226, ex="J", size>100, src=.md.CTS
symids:(,/){.md.getSymID[`date$x; y]}[day;] each (0!select from .EDGA.symbols where exchange in `P)`ticker;
select from .md.orders where date=7226, mt in (9 10 11 12 19 20),size>100
count .md.orders
f1:{[day;ex]
    (,/){.md.getSymID[`date$x; y]} [day;] each (0!select from .md.symbols where exchange in ex)`ticker
    }
count f1[7226; (`N)]

count .NYSE.symbols

select distinct exchange from .md.symbols
10#.md.symbols

.md.getSymID[`date$day; x]
count select from .md.symbols where exchange=`A

dateDay:"d"$7226i
dateDay
count select from listed

.md.tradeMatch[7226; "P"; .md.CTS]
exec ticker from 
exec ticker from .md.tradeMatchListed[ 7226; "P"; .md.CTS; `P]  where exchange=`P
 where exchange=`P
exec ticker from listed where exchange=`P


select distinct ex from .md.trade where date=7226, src=.md.CTS
count select from .md.orders where date=7226, ex="P", mt in (9 10 11 12 19 20)
count .res.CTS_P

select from .md.bbo where ex="Z"

-100#select from .md.trade where ex="Q", date=7226

100#select from .res.UTDF_Z where not null td
         
{update r:100*nm%m from select nm:count i where null td, m:count i from x} .res.CTS_Q
{update r:100*nm%m from select nm:count i where null td, m:count i by symbolid from x} .res.CTS_P
{select m:med td, a:avg td, s_dev:sdev td from x where not null td} .res.CTS_P
delta:{select `time$time, `long$td from x where not null td} .res.CTS_P

getDelta:{select `time$time, `long$td from x where not null td}

statDelayFor:{
    [percent; dtSet] ds:("i"$((count dtSet)*percent%100))#asc dtSet[`td]; 
    `max_val`avg_val`med_val`sdev_val!(max[ds]; avg[ds]; med[ds]; sdev[ds]) % 1000
    }
    
getStat:{[delta]
    (,/){update proc:y from enlist statDelayFor[y; x] } 
    [delta;] each (50 87.5 90 95 98 99)
}

statDelayFor[99; .res.UTDF_P_Q]

getStat[getDelta[.res.CTS_P_P]]
getStat[getDelta[.res.CTS_P_Z]]
getStat[getDelta[.res.CTS_N_N]]
getStat[getDelta[.res.UTDF_P_Q]]
.res.CTS_Z:raze .md.tradeMatchListed[; "Z"; .md.CTS; .md.allEx] peach 7226 + til 5
getStat[getDelta[.res.CTS_Z]]

sym_cqs:exec distinct symbolid from .md.bbo where date=7226, src=.md.CQS
sym_uqdf:exec distinct symbolid from .md.bbo where date=7226, src=.md.UQDF

sym_cts:exec distinct symbolid from .md.trade where date=7226, src=.md.CTS
exec distinct symbolid from .md.trade where date=7226, src=.md.UTDF, symbolid in sym_cts

exec distinct exchange from llll where id in sym_uqdf 
(,/){.md.getSymID[2019.10.14; x]} each  (0!lll)`ticker 

count select from .NASDAQ.listed where exchange=`Q

.res.UTDF_Q_Q:raze .md.tradeMatchListed[; "Q"; .md.UTDF; `Q] peach 7226 + til 5
getStat[getDelta[.res.UTDF_Q_Q]]
.Q.gc[]
count .res.CTS_Q

.md.nyseTradeMatchListed:{[day;sid;listedOn]
    symids:(,/){.md.getSymID[`date$x; y]}[day;] each (0!select from .md.symbols where exchange in listedOn)`ticker;
    trds:`time xasc update ttime:time from update "P"$string time from select from .md.trade where date=day, ex="N", size>100, src=sid, symbolid in symids;
    excs:`time xasc update "P"$string time from select date, size:tradeSize, time, symbolid, price from `time xasc .md.nyseGenTrade where date=day, tradeSize>100, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:excs[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from wj[w;`symbolid`price`time;excs;(trds;(::;`ttime))]}

.res.CTS_N:raze .md.nyseTradeMatchListed[; .md.CTS; .md.allEx] peach 7226 + til 5
.res.CTS_N_P:raze .md.nyseTradeMatchListed[; .md.CTS; `P] peach 7226 + til 5
.res.CTS_N_N:raze .md.nyseTradeMatchListed[; .md.CTS; `N] peach 7226 + til 5
.res.CTS_N_Z:raze .md.nyseTradeMatchListed[; .md.CTS; `Z] peach 7226 + til 5
.res.UTDF_N_Q:raze .md.nyseTradeMatchListed[; .md.UTDF; `Q] peach 7226 + til 5
{update r:100*nm%m from select nm:count i where null td, m:count i from x} .res.CTS_J

getStat[getDelta[.res.CTS_N]]
getStat[getDelta[.res.CTS_N_P]]
getStat[getDelta[.res.CTS_N_N]]
getStat[getDelta[.res.CTS_N_Z]]
getStat[getDelta[.res.UTDF_N_Q]]


select distinct date from .md.genBboQ

.res.CTS_J:raze .md.tradeMatchListed[; "J"; .md.CTS; .md.allEx] peach 7226 + til 5
getStat[getDelta[.res.CTS_J]]
.res.UTDF_J:raze .md.tradeMatchListed[; "J"; .md.UTDF; `Q] peach 7226 + til 5;
getStat[getDelta[.res.UTDF_J]]
