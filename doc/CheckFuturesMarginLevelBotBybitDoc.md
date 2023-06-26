# CheckFuturesMarginLevelBotBybit documentation
A trading bot that regularly checks the margin level on the futures exchange. If the margin falls below the specified limit, the bot automatically replenishes the futures account to the defined level after a certain time interval expires.

## Configuration
-- Intraday
* [Bot configuration](../config/CheckFuturesMarginLevelBotBybitIntradayConfig.yaml)
* [Logger configuration](../config/CheckFuturesMarginLevelBotBybitIntradayLogger.conf)

-- Swing
* [Bot configuration](../config/CheckFuturesMarginLevelBotBybitSwingConfig.yaml)
* [Logger configuration](../config/CheckFuturesMarginLevelBotBybitSwingLogger.conf)

-- Position
* [Bot configuration](../config/CheckFuturesMarginLevelBotBybitPositionConfig.yaml)
* [Logger configuration](../config/CheckFuturesMarginLevelBotBybitPositionLogger.conf)

## How to run
```bash
make CheckFuturesMarginLevelBotBybitIntraday # Intraday bot
make CheckFuturesMarginLevelBotBybitSwing # Swing bot
make CheckFuturesMarginLevelBotBybitPosition # Position bot
```