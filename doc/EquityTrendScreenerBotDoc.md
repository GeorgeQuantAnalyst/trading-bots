# EquityTrendScreenerBotDoc documentation

## About bot

Trading bot looking for trends across most US traded stocks (with week options), small-cap U.S. stocks in index Russell 2000 and large-cap U.S. stocks in index S&P 500.
The application recognizes position trends based on the 3M and Y charts. 
The output of the program is an report (list of coins divide to trends) for analyst platform TradingView.

## Configuration

* [Bot configuration](../config/EquityTrendScreenerBotConfig.yaml)
* [Logger configuration](../config/EquityTrendScreenerBotLogger.conf)

## How to run

```commandline
make EquityTrendScreenerBot
```

