# EarlyReactionBot_Bybit documentation

## About bot

Bot checks whether there was a reaction to the trading level earlier, if so, it cancels the given trade.

## Configuration

* [Bot configuration intraday](../config/EarlyReactionBotBybitIntradayConfig.yaml)
* [Logger configuration intraday](../config/EarlyReactionBotBybitIntradayLogger.conf)
* [Bot configuration swing](../config/EarlyReactionBotBybitSwingConfig.yaml)
* [Logger configuration swing](../config/EarlyReactionBotBybitSwingLogger.conf)
* [Bot configuration position](../config/EarlyReactionBotBybitPositionConfig.yaml)
* [Logger configuration position](../config/EarlyReactionBotBybitPositionLogger.conf)

## How to run
```commandline
make EarlyReactionBotBybitIntraday
make EarlyReactionBotBybitSwing
make EarlyReactionBotBybitPosition
```
