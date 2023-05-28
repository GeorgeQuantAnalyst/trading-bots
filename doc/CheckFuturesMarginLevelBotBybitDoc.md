# CheckFuturesMarginLevelBotBybit documentation
Trading bot checking sufficient margin on the futures exchange, if the margin is below the specified limit,
then after the expiration of a defined time interval (2 hours intraday, 12 hours swing for example) the bot fund
futures account on defined level.

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