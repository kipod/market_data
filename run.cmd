@echo off
:: 2019_10_15
python parse.py --market=S:\temp\md\2019_10_15\market_ARCA-30.csv.bin --CQS=S:\temp\md\2019_10_15\CQS_ARCA_P-30.csv.bin --out=S:\temp\md\2019_10_15\CQS.csv
python parse.py --market=S:\temp\md\2019_10_15\market_ARCA-30.csv.bin --CQS=S:\temp\md\2019_10_15\CQS_ARCA_P-30.csv.bin --out=S:\temp\md\2019_10_15\CQS_1.csv --interval=1
python parse.py --market=S:\temp\md\2019_10_15\market_ARCA-30.csv.bin --CTS=S:\temp\md\2019_10_15\CTS_ARCA-30.csv.bin --out=S:\temp\md\2019_10_15\CTS.csv
python parse.py --market=S:\temp\md\2019_10_15\market_ARCA-30.csv.bin --CTS=S:\temp\md\2019_10_15\CTS_ARCA-30.csv.bin --out=S:\temp\md\2019_10_15\CTS_1.csv --interval=1
:: 2019_10_16
::python parse.py --market=S:\temp\md\2019_10_16\market_ARCA-30.csv.bin --CQS=S:\temp\md\2019_10_16\CQS_ARCA_P-30.csv.bin --out=S:\temp\md\2019_10_16\CQS.csv
python parse.py --market=S:\temp\md\2019_10_16\market_ARCA-30.csv.bin --CQS=S:\temp\md\2019_10_16\CQS_ARCA_P-30.csv.bin --out=S:\temp\md\2019_10_16\CQS_1.csv --interval=1
::python parse.py --market=S:\temp\md\2019_10_16\market_ARCA-30.csv.bin --CTS=S:\temp\md\2019_10_16\CTS_ARCA-30.csv.bin --out=S:\temp\md\2019_10_16\CTS.csv
::python parse.py --market=S:\temp\md\2019_10_16\market_ARCA-30.csv.bin --CTS=S:\temp\md\2019_10_16\CTS_ARCA-30.csv.bin --out=S:\temp\md\2019_10_16\CTS_1.csv --interval=1

