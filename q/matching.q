meta .md.orders

select from .md.trade where date=7226, size > 100, symbolid=1580


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

.md.tradeMatch:{[day;xchng;sid]
    symbols:$[xchng="Z"; .BATS.symbols; xchng="Q"; .NASDAQ.symbols; xchng="N"; .NYSE.symbols; xchng in "PT"; .ARCA.symbols];
    symids:.md.getSymID[`date$day] each symbols;
    trds:`time xasc update ttime:time from update "P"$string time from select from .md.trade where date=day, ex=xchng, size>100, src=sid, symbolid in symids;
    excs:`time xasc update "P"$string time from select date, size, time, symbolid, orderid, oprice:price from .md.orders where date=day, ex=xchng, mt in (9 10 11 12 19 20), size>100, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:excs[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from wj[w;`symbolid`size`time;excs;(trds;(::;`ttime))]}

.md.tradeMatchListed:{[day;xchng;sid;listedOn]
    //symbols:$[xchng="Z"; .BATS.symbols; xchng="Q"; .NASDAQ.symbols; xchng="N"; .NYSE.symbols; xchng in "PT"; .ARCA.symbols];
    listed:$[xchng="Z"; .BATS.listed; xchng="Q"; .NASDAQ.listed; xchng="N"; .NYSE.listed; xchng in "PT"; .ARCA.listed];
    symids:listed;
    :symids;
    trds:`time xasc update ttime:time from update "P"$string time from select from .md.trade where date=day, ex=xchng, size>100, src=sid, symbolid in symids;
    excs:`time xasc update "P"$string time from select date, size, time, symbolid, orderid, oprice:price from .md.orders where date=day, ex=xchng, mt in (9 10 11 12 19 20), size>100, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:excs[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from wj[w;`symbolid`size`time;excs;(trds;(::;`ttime))]}

count exec ticker from .ARCA.listed where exchange=`P

.res.UTDF_Q:raze .md.tradeMatch[ ; "Q"; .md.UTDF] peach 7226 + til 5
.res.UTDF_Z:raze .md.tradeMatch[ ; "Z"; .md.UTDF] peach 7226 + til 5
.res.UTDF_T:raze .md.tradeMatch[ ; "T"; .md.UTDF] peach 7226 + til 5

.res.CTS_Z:raze .md.tradeMatch[ ; "Z"; .md.CTS] peach 7226 + til 5
.res.CTS_P:raze .md.tradeMatch[ ; "P"; .md.CTS] peach 7226 + til 1
.res.CTS_P_lP:raze .md.tradeMatchListed[ ; "P"; .md.CTS; `P] peach 7226 + til 5

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

{update r:100*nm%m from select nm:count i where null td, m:count i from x} .res.UTDF_Q
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

getStat[getDelta[.res.CTS_P]]

sym_cqs:exec distinct symbolid from .md.bbo where date=7226, src=.md.CQS
exec distinct symbolid from .md.bbo where date=7226, src=.md.UQDF, symbolid in sym_cqs

sym_cts:exec distinct symbolid from .md.trade where date=7226, src=.md.CTS
exec distinct symbolid from .md.trade where date=7226, src=.md.UTDF, symbolid in sym_cts

lll: (,/)(.NYSE.listed;.ARCA.listed;.BATS.listed;.NASDAQ.listed)
exec distinct exchange from lll where .md.getSymID[2019.10.14; ticker] in sym_cts
.md.getSymID[2019.10.14; ] each sym_cqs
lll
