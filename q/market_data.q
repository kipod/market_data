.md.orders:([] date:`int$(); time:`timespan$(); symbolid:`int$(); ex:`char$(); mt:`int$(); orderid:`long$(); size:`int$(); price:`int$())
.md.bbo:([] date:`int$(); time:`timespan$(); symbolid:`int$(); ex:`char$(); bidvol:`int$(); bidprice:`int$(); askvol:`int$(); askprice:`int$(); src:`int$())
.md.trade:([] date:`int$(); time:`timespan$(); symbolid:`int$(); ex:`char$(); price:`int$(); size:`int$(); side:`char$(); src:`int$())
ta:([] a:`int$())


.md.upd:insert 
meta 
save `:/md/orders
count ta
count .md.orders
system "pwd"
count .ARCA.symbols
// q/kdb:
// value (`upd;`bbo;(2019.10.21; .z.n; 123; "Z"; 100; 1024; 200; 1025))

// C/C++:
// records = createTable(columns...);
// k(handle, "upd"; ks(ss("bbo")); records; K(0));

meta bbo
meta trade

select from .md.bbo where ex="N"
.z.n
.md.upd[`.md.bbo; (123; .z.n; 56; "Q"; 100; 1024; 200; 1025; 56)]
tables `.md
`:md/bbo set .md.bbo;
`:md/orders set .md.orders;
`:md/trade set .md.trade;

