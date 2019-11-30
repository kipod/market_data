.md.minDTime:00:00:00.00002p;
.md.maxDTime:00:00:00.02p;
.md.CTS:11;
.md.UTDF:10;
.md.CQS:72;
.md.UQDF:73;

//.md.genBboZ18:`:crm.ath:5018 "genBboZ18"
//.md.genBboZ18:`:crm.ath:5018 "res"

.md.getSymID:{[day; name]
        (hsym `$"symbolism-main.bo.ath:5001") ({[x;y] indxFAfile[x;y]};day;name)
        }

.md.genBboQ7230

count update bsize:`int$bsize%100, asize:`int$asize%100 from .md.genBboQ7230
count select from .md.bbo where date=7230, symbolid=661
.md.genBbo: delete ttime from update time:ttime, "i"$ask, "i"$bid, "i"$asize%100, "i"$bsize%100 from `ttime xasc .md.genBbo;

.md.bboMatch:{[day;xchng;sid]
    symbols:$[xchng="Z"; .BATS.symbols; xchng="Q"; .NASDAQ.symbols; xchng="N"; .NYSE.symbols; xchng in "PT"; .ARCA.symbols];
    symids:.md.getSymID[`date$day] each symbols;
    symids:exec distinct symbolid from .md.genBbo where date=day, ex=xchng;
    bbo:`time xasc update ttime:time from update "P"$string time from select from .md.bbo where date=day, ex=xchng, src=sid, symbolid in symids;
    genbbo:`time xasc update "P"$string time from select date,time, symbolid, bidvol:`int$bsize%100, bidprice:bid, askvol:`int$asize%100, askprice:ask from .md.genBbo where date=day, ex=xchng, symbolid in symids;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:genbbo[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from
        wj[w;`symbolid`bidvol`bidprice`askvol`askprice`time;genbbo;(bbo;(::;`ttime))]}

.md.bboMatchListed:{[day;xchng;sid;listedOn]
    symids:(,/){.md.getSymID[`date$x; y]}[day;] each (0!select from .EDGA.symbols where exchange in listedOn)`ticker;
/     symids:exec distinct symbolid from .md.genBBOQ;
    bboEx:xchng;
    bbo:`time xasc update ttime:time from update "P"$string time from select from .md.bbo where date=day, ex in bboEx, src=sid, symbolid in symids;   
    genbbo:`time xasc update "P"$string time from select date,time:ttime, symbolid, bidvol:`int$bsize%100, bidprice:bid, askvol:`int$asize%100, askprice:ask from .md.genBBOJ where date=day, ex=xchng, symbolid in bbo`symbolid;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:genbbo[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from
        wj[w;`symbolid`bidvol`bidprice`askvol`askprice`time;genbbo;(bbo;(::;`ttime))]}
        
(,/){.md.getSymID[`date$x; y]}[day;] each (0!select from .md.symbols where exchange in `P)`ticker
symids:(,/){.md.getSymID[`date$x; y]}[7226;] each (0!select from .md.symbols)`ticker
bbos:select distinct symbolid from .md.bbo where date=7226, ex="T", src=.md.CQS, symbolid in symids
count exec distinct symbolid from .md.genBBOQ7230

count .NASDAQ.symbols

genBbos:select distinct symbolid from select date,time, symbolid, bidvol:bsize, bidprice:bid, askvol:asize, askprice:ask from .md.genBbo where date=7226, ex="Q", symbolid in symids

exec count distinct symbolid from .md.orders where date=7226, ex="Q", symbolid in symids

select distinct ex from .md.genBbo where symbolid in symids
.Q.gc[]
count symids
 select count distinct symbolid by date from .md.genBBOQ

 select count i by symbolid from .md.bbo where date=7230, ex in "QT", symbolid in exec distinct symbolid from .md.genBBOQ7230
select distinct date from .md.genBBOQ7230
.res.genBboZ18:.md.bboMatch [7226;"Z";.md.UQDF]
.res.UQDF_Z_Q:.md.bboMatchListed[7226i; "Z"; .md.UQDF; `Q]
.md.bboMatchListed[7226i; "Q"; .md.CQS; `P`N`Q`Z`A]

select distinct exchange from .md.symbols

.md.matchBBOSave:{[name; ex; src; listedEx]
    tableName:`$".res.",name; 
    tableName set raze .md.bboMatchListed[; ex; src; listedEx] peach 7226 + til 5;
    fileName:`$":res/",name;
    fileName set get tableName; // save to file
    ![`.res;();0b;tables `.res]; // delete all tables from .res
    show `$name," - done";
}

.md.matchBBOSave["UQDF_Z_Q"; "Z"; .md.UQDF; `Q]
.md.matchBBOSave["CQS_P_Z"; "P"; .md.CQS; `Z]
.md.matchBBOSave["CQS_Z_Z"; "Z"; .md.CQS; `Z]
.md.matchBBOSave["CQS_Q_P"; "Q"; .md.CQS; `P]
.md.matchBBOSave["CQS_Q_PNTZ"; "Q"; .md.CQS; `P`N`T`Z]

homework:{
.md.matchBBOSave["UQDF_Q_Q"; "Q"; .md.UQDF; `Q];
.md.matchBBOSave["CQS_Q"; "Q"; .md.CQS; .md.allEx];
}

100#select from .md.bbo where ex="N"
count .res.genBboZ18
count select distinct symbolid from .res.UQDF_Z_Q

{update r:100*nm%m from select nm:count i[where null td], m:count i by symbolid from x} get `:res/CQS_Q
{update r:100*nm%m from select nm:count i[where null td], m:count i by symbolid from x} get `:res/UQDF_Q_Q

{update r:100*nm%m from select nm:count i[where null td], m:count i by symbolid from x} .res.UQDF_Z_Q
select med td, avg td, sdev td from .tmp.tm where not null td
select `time$time, `long$td from .tmp.tm where not null td


getStat[getDelta[get `:res/CQS_Q]]
getStat[getDelta[get `:res/UQDF_Q_Q]]

select distinct symbolid from get `:res/CQS_P_Z
count distinct (select from .md.bbo where ex="N", src=72)`symbolid
get `.md.genBboUpdBook

.md.nyseBboMatchListed:{[day;sid;listedOn]
    symids:(,/){.md.getSymID[`date$x; y]}[day;] each 10#(0!select from .md.symbols where exchange in listedOn)`ticker;
    bbo:`time xasc 0!update ttime:time from update "P"$string time from select from .md.bbo where date=day, ex="N", src=sid, symbolid in symids;   
    genbbo:`time xasc 0!update "P"$string time from select date,time:ttime, symbolid, bidvol:`int$bsize%100, bidprice:bid, askvol:`int$asize%100, askprice:ask from .md.genBboUpdBook where date=day, symbolid in distinct bbo`symbolid;
    w:"P"$string (.md.minDTime;.md.maxDTime)+\:genbbo[`time];
    update td:{d:x-y;r:min d where d>0;$[0Wj=`long$r;0Nn;r]}'[ttime;time] from
        wj[w;`symbolid`bidvol`bidprice`askvol`askprice`time;genbbo;(bbo;(::;`ttime))]}

.md.nyseBboMatchListed[;.md.CQS;`P]

.md.matchNyseBBOSave:{[name; src; listedEx]
    tableName:`$".res.",name; 
    tableName set raze .md.nyseBboMatchListed[; src; listedEx] peach 7226 + til 5;
    fileName:`$":res/",name;
    fileName set get tableName; // save to file
    ![`.res;();0b;tables `.res]; // delete all tables from .res
    show `$name," - done";
}
.z.d
.md.matchNyseBBOSave["CQS_N"; .md.CQS; .md.allEx]
getStat[getDelta[get `:res/CQS_N]]
.md.matchNyseBBOSave["UQDF_N_Q"; .md.UQDF; `Q]
getStat[getDelta[get `:res/UQDF_Q_Q]]

select from .md.symbols where
symids:(,/){.md.getSymID[`date$x; y]}[7226;] each (0!select from .md.symbols where exchange in `Z)`ticker
symids:(,/){.md.getSymID[`date$x; y]}[7226;] each `:crm.ath:5018 "symlist`ticker"
select distinct symbolid from .md.genBboUpdBook where date=7226, symbolid in symids
select distinct symbolid from .md.bbo where date=7226, symbolid in symids, ex="N"
symids
count select distinct symbolid from .md.genBBO where date=7226, ex in "QT", symbolid in symids
in symids

5 in til 7


