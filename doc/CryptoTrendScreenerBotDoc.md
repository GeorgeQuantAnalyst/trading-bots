# CryptoTrendScreenerBotDoc documentation

## About bot

Trading bot looking for trends across the USDT perpetual futures market on the Bybit exchange. The application recognizes
intraday trends based on the D chart, swing trends based on the W and M charts. The output of the program is an excel
file.

**Find trade opportunities (example intraday)**
* Long
  * Open report the sheet "Intraday D trends"
  * Sort by the market that grew the most by colum "Change 7 days, %"
  * Filter markets by context (Up-trend, Start rotation after up-trend) 

* Short
  * Open report the sheet "Intraday D trends"
  * Sort by the market that decline the most by colum "Change 7 days, %"
  * Filter markets by context (Up-trend, Start rotation after up-trend) 

## Configuration

* [Bot configuration](../config/CryptoTrendScreenerBotConfig.yaml)
* [Logger configuration](../config/CryptoTrendScreenerBotLogger.conf)

## How to run
```commandline
make CryptoTrendScreenerBot
```

## How to open report
```
libreoffice reports/cryptoTrendScreener/CryptoTrendScreener_YYYYMMDD.xlsx
```

