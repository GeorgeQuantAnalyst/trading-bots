# TODOs

-- high priority
* [x] Migrate CryptoTrendScreenerJob to CryptoTrendScreenerBot
* [x] Migrate ForexTrendScreenerJob to ForexTrendScreenerBot
* [x] Migrate bybit-place-trailing-stops-job to BybitPlaceTrailingStopBot
* [x] Create BybitEarlyReactionBot
* [x] Release version 1.0.0

-- medium priority
* [x] Create BybitCloseTradesAtTimeBot: Bot closing pending orders and position at defined time. You can set close for all or specific currency pairs.
* [x] Logging rest response as DEBUG level

-- low priority
* [] Create BybitMaxOpenPositionsBot: Bot controlling the maximum number of open positions, if more than allowed limit, the newer positions will be closed.
* [] Create BybitStopOutBot: Bot checking for sufficient equity for trading, if the equity falls below the set limit, all positions and pending orders will be terminated.
