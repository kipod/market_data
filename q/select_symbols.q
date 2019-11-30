dr:(2019.10.14;2019.10.18);
acsymq: `:crm.ath:5016 "select c:count i by date, sym from quote where date within dr, ex = \"Q\"";
acsymz: `:crm.ath:5016 "select c:count i by date, sym from quote where date within dr, ex = \"Z\"";
acsymn: `:crm.ath:5016 "select c:count i by date, sym from quote where date within dr, ex = \"N\"";
acsymp: `:crm.ath:5016 "select c:count i by date, sym from quote where date within dr, ex = \"P\"";
atsymq: `:crm.ath:5016 "select c:count i by date, sym from trade where date within dr, size>100, ex=\"Q\"";
atsymz: `:crm.ath:5016 "select c:count i by date, sym from trade where date within dr, size>100, ex=\"Z\"";
atsymn: `:crm.ath:5016 "select c:count i by date, sym from trade where date within dr, size>100, ex=\"N\"";
atsymp: `:crm.ath:5016 "select c:count i by date, sym from trade where date within dr, size>100, ex=\"P\"";


syms:(,/){`:symbolism.bo.ath:5001 ({[sym]select first distinct exchange by ticker from .symbolism.FullActiveFile where date=2019.10.14, ticker=sym};x)} each niceSymbols[(100;1000);acsymq]
syms:(,/){`:symbolism.bo.ath:5001 ({[sym]select first distinct exchange by ticker from .symbolism.FullActiveFile where date=2019.10.14, ticker=sym};x)} each (exec sym from acsymq)
.NASDAQ.symbols:(,/){100#select from syms where exchange=x} each `P`Z`N`Q

.md.getSymID:{[day; name]
        (hsym `$"symbolism-main.bo.ath:5001") ({[x;y] indxFAfile[x;y]};day;name)
        }
        
([] symbolid:(.md.getSymID[2019.10.18;] each (0!.NASDAQ.symbols)`ticker))

`:symbolism.bo.ath:5001 "select from .symbolism.FullActiveFile where date=2019.10.14"
exec sym from acsymq
`:crm.ath:5016 "10#select from quote where date=2019.10.15"

niceSymbols:{[cr;allSyms]exec sym from select avg c by sym from allSyms where c within cr};
niceSymbols[(100;1000);acsymq]
csymq:niceSymbols[(1000;2000);acsymq]; / select NASDAQ symbols by frequency quota messages
csymz:niceSymbols[(1000;20000);acsymz];
csymn:niceSymbols[(1000;20000);acsymn];
csymp:niceSymbols[(700;20000);acsymp];
tsymq:niceSymbols[(580;4000);atsymq]; / select NASDAQ symbols by trading frequency
tsymz:niceSymbols[(550;4000);atsymz];
tsymn:niceSymbols[(500;4500);atsymn];
tsymp:niceSymbols[(440;6000);atsymp];

.NASDAQ.symbols:tsymq inter csymq;
.BATS.symbols:tsymz inter csymz;
.NYSE.symbols:tsymn inter csymn;
.ARCA.symbols:tsymp inter csymp;

delete acsymq from `.;
delete acsymz from `.;
delete acsymn from `.;
delete acsymp from `.;
delete atsymq from `.;
delete atsymz from `.;
delete atsymn from `.;
delete atsymp from `.;
delete csymq from `.;
delete csymz from `.;
delete csymn from `.;
delete csymp from `.;
delete tsymq from `.;
delete tsymz from `.;
delete tsymn from `.;
delete tsymp from `.;

trades: `:crm.ath:5016 "select from trade where date within dr, ex = \"Q\", size>100";
.NASDAQ.trade: select from trades where sym in .NASDAQ.symbols;
trades: `:crm.ath:5016 "select from trade where date within dr, ex = \"Z\", size>100";
.BATS.trade: select from trades where sym in .BATS.symbols;
trades: `:crm.ath:5016 "select from trade where date within dr, ex = \"N\", size>100";
.NYSE.trade: select from trades where sym in .NYSE.symbols;
trades: `:crm.ath:5016 "select from trade where date within dr, ex = \"P\", size>100";
.ARCA.trade: select from trades where sym in .ARCA.symbols;
// count .NASDAQ.trade
.Q.gc[]
`:crm.ath:5015 "select from TaqMasterFiles where date=2019.10.14, listed_exchange<>`Q, traded_on_nasdaq"

count select from .md.genBBO2

acsymq: `:crm.ath:5016 "select from (select c:count i by date, sym from quote where date within dr, ex in \"QT\") where c within (100;1000)";
exec distinct sym from (select c:count i by sym from acsymq) where c=5
syms:`:symbolism.bo.ath:5001 ({[dr;s]select ticker, exchange from .symbolism.FullActiveFile where date within dr, ticker in s, exchange in `P`Z`N`Q};dr;exec distinct sym from (select c:count i by sym from acsymq) where c=5)

count syms
.NASDAQ.symbols:raze {select [100] from syms where exchange=x} each `P`Z`N`Q
select count i by exchange from .NASDAQ.symbols


acsymj: `:crm.ath:5016 "select from (select c:count i by date, sym from quote where date within dr, ex in \"J\") where c within (100;1000)";
syms:`:symbolism.bo.ath:5001 ({[dr;s]select ticker, exchange from .symbolism.FullActiveFile where date within dr, ticker in s, exchange in `P`Z`N`Q};dr;exec distinct sym from (select c:count i by sym from acsymj) where c=5)

count syms
.EDGA.symbols:raze {select [100] from syms where exchange=x} each `P`Z`N`Q
select count i by exchange from .EDGA.symbols
