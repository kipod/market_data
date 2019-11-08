data:`:chernov.dev.ath:5000   "select from .md.orders where date=7230"; 
    //data:update size:"i"$size%100 from update sizeOrg:size  from data;
    //select count i by symbolid from data
symbolsZ:`:chernov.dev.ath:5000 ".BATS.symbols" ;
symbolsZdigits:(,/) {`:symbolism.bo.ath:5001 ({[sym] indxFAfile[2019.10.18;sym]};x) } each symbolsZ;
   //dictSymb:symbolsZdigits!symbolsZ
symbolsZdigits:(0!50#(`cnt xasc select cnt:count i by symbolid from data))   `symbolid;
data: select from data where symbolid in symbolsZdigits, ex="Z";
     
     //count data
     .Q.gc[]
mtdict: (1 2 4 5 6 7 8 13 14 16 17 18 9 10 11 12 19 20) !
    `BUY`SELL`CANCEL_LONG`CANCEL_FULL`DELETE`MODIFY_LONG`MODIFY_FULL`REPLACE_LONG`REPLACE_FULL`ADD_ATTR_BUY_LONG`ADD_ATTR_SELL_LONG`ADD_ATTR_FULL`EXEC_ORDER_NP_FV`EXEC_ORDER_NP_LV`EXEC_ORDER_LP_LV`EXEC_ORDER_FP_FV`EXEC_ORDER_WREMAINING_LONG`EXEC_ORDER_WREMAINING_FULL;

indxdict: (1 2 4 5 6 7 8 13 14 16 17 18 9 10 11 12 19 20) !(1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 );

data:select from data where symbolid=72, ex="P"
data:update actn:mtdict[mt],indx:indxdict[mt]  from data ;
10#data

dser:select from data where ex="P", actn like "EXEC_*", price=0;
dserial:(,/){0!delete ttime from update time:ttime from select ttime:x[0],size:x[2],ex:x[3], last price by time, orderid, symbolid from data where  time<=x[0], orderid=x[1], symbolid=x[4], price<>0}  each flip  (dser`time;dser`orderid;dser`size;dser`ex;dser`symbolid);
data:data lj 3!dserial;
   select from data where actn like "EXEC_*", price=0
getTopOfBook: {
     dataset: `time xasc select from data where date=x[0], symbolid=x[1], ex=x[2];        
     res: (,/)    {[dataset;order] update size5:{$[y;x;[x[z]:x[z-1]+x[z];x]]}/[size2;indx;i],indByOrderId:i from select from dataset where orderid=order} [dataset;] peach (exec distinct orderid from dataset where actn in `BUY`SELL);
     .Q.gc[];
    `time xasc res lj (select side:first actn by orderid from dataset where actn in `BUY`SELL)};
 
datalist:exec distinct flip (date;symbolid;ex) from data;
   
    
data:(update  size2:size^size2 from update size2:-1*size from data where actn like "EXEC*");  
data: update size2:0  from data where actn=`DELETE, size<>0


select from data where actn=`DELETE, price<>0
calcAlldata:{
          data3:getTopOfBook x;restdata: (,/)  {[data3;tt]dset:update ttime:tt,date,symbolid,ex from select from data3 where time<=tt,i=(last;i) fby ([]orderid);dset:delete from dset where size5=0;        
        (select  bid:max price, bsize:sum size5[where price=max price] by ttime,date,symbolid,ex from dset where side=`BUY, size5>0) lj
        (select ask:min price, asize:sum size5[where price=min price] by ttime,date,symbolid,ex from dset where side=`SELL, size5>0)} [data3;] peach (exec distinct time from `time xasc data3) ;        
        0N!x;reess:delete b from delete from (update b:(deltas bid)+(deltas  ask)+(deltas asize)+(deltas bsize)  from update ask:0^ask,bid:0^bid, asize:0^asize,bsize:0^bsize from restdata) where b=0}
        

5#data

select from data where time<14:32:53.789828689,price=61800
   
genBboZ18:(,/) calcAlldata peach 

calcAlldata

res:`ttime xasc calcAlldata first -1#datalist 
  rres: `time xasc getTopOfBook first -1#datalist  

   