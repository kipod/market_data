h:`:chernov.dev.ath:5000;
day:"I"$.z.x[0];
xchng:"C"$.z.x[1];
datah: h   "select from .md.orders where date=",string[day],", ex=\"",xchng,"\"";
0N!xchng;
symbolsZ:$[xchng="Z";h ".BATS.symbols"; xchng="Q";h ".NASDAQ.symbols"; xchng="N"; h ".NYSE.symbols"; xchng in "PT"; h ".ARCA.symbols";::];
0N!symbolsZ;
dictday:(7230 7229 7228 7227 7226)!(2019.10.18;2019.10.17;2019.10.16;2019.10.15;2019.10.14);
symbolsZdigits:(,/) {`:symbolism.bo.ath:5001 ({[days;sym] indxFAfile[days;sym]};x;y) } [dictday[day];] each symbolsZ;

data: select from datah where symbolid in symbolsZdigits, ex in xchng;

.Q.gc[];
mtdict: (1 2 4 5 6 7 8 13 14 16 17 18 9 10 11 12 19 20) !
    `BUY`SELL`CANCEL_LONG`CANCEL_FULL`DELETE`MODIFY_LONG`MODIFY_FULL`REPLACE_LONG`REPLACE_FULL`ADD_ATTR_BUY_LONG`ADD_ATTR_SELL_LONG`ADD_ATTR_FULL`EXEC_ORDER_NP_FV`EXEC_ORDER_NP_LV`EXEC_ORDER_LP_LV`EXEC_ORDER_FP_FV`EXEC_ORDER_WREMAINING_LONG`EXEC_ORDER_WREMAINING_FULL;
indxdict: (1 2 4 5 6 7 8 13 14 16 17 18 9 10 11 12 19 20) !(1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 );

data:update actn:mtdict[mt],indx:indxdict[mt]  from data ;
data:(update  size2:size^size2 from update size2:-1*size from data where actn like "EXEC*");
data: update size2:0  from data where actn=`DELETE, size<>0;
if[count[data]=0;exit[0]];
dser:select from data where actn like "EXEC_*", price=0;
dserial:(,/){0!delete ttime from update time:ttime from select ttime:x[0],size:x[2],ex:x[3], last price by time, orderid, symbolid from data where  time<=x[0], orderid=x[1], symbolid=x[4], price<>0}  each flip  (dser`time;dser`orderid;dser`size;dser`ex;dser`symbolid);
if[count[dserial]>0;data:data lj 3!dserial];
getTopOfBook: {
     dataset: `time xasc select from data where date=x[0], symbolid=x[1], ex=x[2];
     res: (,/)    {[dataset;order] update size5:{$[y;x;[x[z]:x[z-1]+x[z];x]]}/[size2;indx;i],indByOrderId:i from select from dataset where orderid=order} [dataset;] peach (exec distinct orderid from dataset where actn in `BUY`SELL);
     .Q.gc[];
    `time xasc res lj (select side:first actn by orderid from dataset where actn in `BUY`SELL)};

datalist:exec distinct flip (date;symbolid;ex) from data;

calcAlldata:{
          data3:getTopOfBook x;restdata: (,/)  {[data3;tt]dset:update ttime:tt,date,symbolid,ex from select from data3 where time<=tt,i=(last;i) fby ([]orderid);dset:delete from dset where size5=0;
        (select  bid:max price, bsize:sum size5[where price=max price] by ttime,date,symbolid,ex from dset where side=`BUY, size5>0) lj
        (select ask:min price, asize:sum size5[where price=min price] by ttime,date,symbolid,ex from dset where side=`SELL, size5>0)} [data3;] peach (exec distinct time from `time xasc data3) ;
        0N!x;reess:delete b from delete from (update b:(deltas bid)+(deltas  ask)+(deltas asize)+(deltas bsize)  from update ask:0^ask,bid:0^bid, asize:0^asize,bsize:0^bsize from restdata) where b=0}
.Q.gc[];
genBboZ18:(,/) calcAlldata peach datalist;

(hsym `$"/home/athuser/taqila/",string[day],string[xchng]) set 0!genBboZ18;
exit[0];
