# CryptoTrendScreenerBotDoc documentation

## About bot

Trading bot looking for trends across the USDT perpetual futures market on the Bybit exchange. The application
recognizes intraday trends based on the D chart, swing trends based on the W and M charts. 
The output of the program is an report (list of coins divide to trends) for analyst platform TradingView.

## Configuration

* [Bot configuration](../config/CryptoTrendScreenerBotConfig.yaml)
* [Logger configuration](../config/CryptoTrendScreenerBotLogger.conf)

## How to run

```commandline
make CryptoTrendScreenerBot
```

