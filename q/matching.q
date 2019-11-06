meta .md.orders

select from .md.trade where date=7226, size > 100, symbolid=1580


`:symbolism.bo.ath:5001 "indxFAfile[2019.09.28;`AAPL]"
(hsym `$"symbolism-main.bo.ath:5001") ({[x;y] indxFAfile[x;y]};2019.09.28;`AAPL)
.md.getSymID:{[day; name]
        (hsym `$"symbolism-main.bo.ath:5001") ({[x;y] indxFAfile[x;y]};day;name)
        }

`date$7226
distinct `date$0 + .md.trade.date

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

.tmp.UTDF_NASDAQ:.md.tradeMatch[7226; "Q"; .md.UTDF] + .md.tradeMatch[7227; "Q"; .md.UTDF] + .md.tradeMatch[7228; "Q"; .md.UTDF] + .md.tradeMatch[7229; "Q"; .md.UTDF] + .md.tradeMatch[7230; "Q"; .md.UTDF]

.tmp.tm:.tmp.UTDF_NASDAQ

-100#select from .md.trade where ex="Q", date=7226

update r:100*nm%m from select nm:count i where null td, m:count i from .tmp.tm
update r:100*nm%m from select nm:count i where null td, m:count i by symbolid from .tmp.tm
select med td, avg td, sdev td from .tmp.tm where not null td
select `time$time, `long$td from .tmp.tm where not null td