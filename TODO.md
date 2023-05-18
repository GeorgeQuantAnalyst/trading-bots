# TODOs

-- high priority
* [x] Migrate CryptoTrendScreenerJob to CryptoTrendScreenerBot
* [] Migrate ForexTrendScreenerJob to ForexTrendScreenerBot @Lucka
* [] Migrate bybit-place-trailing-stops-job to BybitPlaceTrailingStopBot @Lucka
* [] Create BybitEarlyReactionBot
* [] Release version 1.0.0

-- medium priority
* [] Create BybitCloseTradesAtTimeBot: Bot closing pending orders and position at defined time. You can set close for all or specific currency pairs.

-- low priority
* [] Create BybitMaxOpenPositionsBot: Bot controlling the maximum number of open positions, if more than allowed limit, the newer positions will be closed.
* [] Create BybitStopOutBot: Bot checking for sufficient equity for trading, if the equity falls below the set limit, all positions and pending orders will be terminated.
