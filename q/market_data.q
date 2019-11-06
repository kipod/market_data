.md.orders:([] date:`int$(); time:`timespan$(); symbolid:`int$(); ex:`char$(); mt:`int$(); orderid:`long$(); size:`int$(); price:`int$())
.md.bbo:([] date:`int$(); time:`timespan$(); symbolid:`int$(); ex:`char$(); bidvol:`int$(); bidprice:`int$(); askvol:`int$(); askprice:`int$(); src:`int$())
.md.trade:([] date:`int$(); time:`timespan$(); symbolid:`int$(); ex:`char$(); price:`int$(); size:`int$(); side:`char$(); src:`int$())
.md.nyseUpdBook:([] date:`int$(); time:`timespan$(); symbolid:`int$(); mt:`int$(); quoteCond:`int$(); price:`long$(); volume:`long$(); numOrders:`int$(); chgSize:`int$(); reason:`int$(); tradeStat:`int$(); side:`char$())
ta:([] a:`int$())


.md.upd:insert 
count .md.orders
system "pwd"
count .ARCA.symbols
count select from .md.nyseUpdBook 
distinct select date from .md.nyseUpdBook
select distinct tradeStat from .md.nyseUpdBook
select num:count i by code:`char$tradeStat from .md.nyseUpdBook

select from .md.nyseUpdBook where date = 7226, symbolid = 688, tradeStat = `int$"O", side = "A"

select date, time, symbolid, price, tradeSize from (
 update tradeSize:abs deltas volume from distinct `time xasc (-1_-2#5#dataset),
 {-1#select from .md.nyseUpdBook where date = 7226, symbolid = 688, tradeStat = `int$"O", price=x[1], time<=x[0], volume<>x[2], numOrders>x[3]}   first -1_-2#flip (5#dataset`time;5#dataset`price;5#dataset`volume;5#dataset`numOrders) 
) where reason=`int$"E" 



.md.nyseGenTrade:{
    dataset:select from .md.nyseUpdBook where date = x[0], symbolid = x[1], side=x[2];
    datasetE:select from dataset where tradeStat = `int$"O", reason = `int$"E";
    res:update tradeSize:abs deltas volume by price from distinct `time xasc (datasetE,(,/){-1#select from y where date = 7226, symbolid = 688, tradeStat = `int$"O", price=x[1], time<=x[0], volume<>x[2], numOrders>x[3]} [;dataset] each flip(datasetE`time;datasetE`price;datasetE`volume;datasetE`numOrders));
    select date, time, symbolid, price, tradeSize,side:x[2] from res where reason=`int$"E", tradeSize>0    
    } 
    
    
    .tmp.nyseGenTrade:(,/).md.nyseGenTrade each .tmp.datalist 
   
       
    .tmp.datalist: (cross/) (exec distinct flip (date;symbolid) from  .md.nyseUpdBook;"BA")
              
                   
    


// q/kdb:
// value (`upd;`bbo;(2019.10.21; .z.n; 123; "Z"; 100; 1024; 200; 1025))

// C/C++:
// records = createTable(columns...);
// k(handle, "upd"; ks(ss("bbo")); records; K(0));
`char$79
`int$"O"
select from .md.bbo where ex="N"
.z.n
tables `.md
`:md/bbo set .md.bbo;
`:md/orders set .md.orders;
`:md/trade set .md.trade;

count .md.trade



