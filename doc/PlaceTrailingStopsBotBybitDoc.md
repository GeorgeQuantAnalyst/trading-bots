# PlaceTrailingStopsBot documentation
Trading bot for entering a trailing stop loss based on open futures positions on the Bybit exchange. 
Bot run in regular intervals defined in CRON table.

**Equation of trailing stop**
```
trailing_stop_loss_move = abs(entry_price-stop_loss_price)
```

## Configuration
-- Intraday
* [Bot configuration](../config/PlaceTrailingStopsBotBybitIntradayConfig.yaml)
* [Logger configuration](../config/PlaceTrailingStopsBotBybitIntradayLogger.conf)

-- Swing
* [Bot configuration](../config/PlaceTrailingStopsBotBybitSwingConfig.yaml)
* [Logger configuration](../config/PlaceTrailingStopsBotBybitSwingLogger.conf)

-- Position
* [Bot configuration](../config/PlaceTrailingStopsBotBybitPositionConfig.yaml)
* [Logger configuration](../config/PlaceTrailingStopsBotBybitPositionLogger.conf)

## How to run
```bash
make placeTrailingStopsBotBybitIntraday # Intraday bot
make placeTrailingStopsBotBybitSwing # Swing bot
make placeTrailingStopsBotBybitPosition # Position bot
```