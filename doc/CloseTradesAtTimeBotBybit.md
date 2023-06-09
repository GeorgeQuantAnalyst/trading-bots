# CloseTradesAtTimeBotBybit documentation
A trading bot that closes pending orders and positions at a specific predefined time.

## Configuration
-- Intraday
* [Bot configuration](../config/CloseTradesAtTimeBotBybitIntradayConfig.yaml)
* [Logger configuration](../config/CloseTradesAtTimeBotBybitIntradayLogger.conf)

-- Swing
* [Bot configuration](../config/CloseTradesAtTimeBotBybitSwingConfig.yaml)
* [Logger configuration](../config/CloseTradesAtTimeBotBybitSwingLogger.conf)

-- Position
* [Bot configuration](../config/CloseTradesAtTimeBotBybitPositionConfig.yaml)
* [Logger configuration](../config/CloseTradesAtTimeBotBybitPositionLogger.conf)

## How to run
```bash
make CloseTradesAtTimeBotBybitIntraday # Intraday bot
make CloseTradesAtTimeBotBybitSwing # Swing bot
make CloseTradesAtTimeBotBybitPosition # Position bot
```
