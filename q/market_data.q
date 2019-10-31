bbo:([] date:`date$(); time:`timespan$(); symbolid:`int$(); marketid:`char$(); bidvol:`int$(); bidprice:`int$(); askvol:`int$(); askprice:`int$())
trade:([] date:`date$(); time:`timespan$(); symbolid:`int$(); marketid:`char$(); price:`int$(); size:`int$(); side:`char$())
orders:([] date:`date$(); time:`timespan$(); symbolid:`int$(); marketid:`char$(); orderid:`long$(); size:`int$(); price:`int$())

upd:insert

// q/kdb:
// value (`upd;`bbo;(2019.10.21; .z.n; 123; "Z"; 100; 1024; 200; 1025))

// C/C++:
// records = createTable(columns...);
// k(handle, "upd"; ks(ss("bbo")); records; K(0));