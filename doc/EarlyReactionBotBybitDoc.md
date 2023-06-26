# EarlyReactionBot_Bybit documentation

## About bot

A trading bot that executes close early reaction trades, where the price reaches 33% before entry and then the market turns in favor of profit.

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
