# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Unreleased
### Added
- EquityTrendScreenerBot

### Deleted
- ForexTrendScreenerBot

### Changed
- CryptoTrendScreenerBotBybit: add support for find positions trends (3M, Y)

### Fixed
- Precise compute context of market (up-trend, down-trend, start-rotation after up-trend, start rotation after downn-trend)
- Better logging in CryptoTrendScreenerBotBybit and EquityTrendScreenerBot

## [1.0.1] - 2023-06-12
### Fixed
- Missing exception handling for pybit client

## [1.0.0] - 2023-06-09
### Added
- BybitExampleBot
- CheckFuturesMarginLevelBotBybit
- CloseTradesAtTimeBotBybit
- CryptoTrendScreenerBotBybit
- EarlyReactionBotBybit
- ForexTrendScreenerBot
- PlaceTrailingStopsBotBybit
