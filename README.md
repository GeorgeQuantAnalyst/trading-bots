# Trading bots

This repository contains trading bots for Automate trading (Trading bots can execute trades automatically based on predefined rules and strategies) 
and Risk management (Trading bots can incorporate risk management techniques, such as setting stop-loss orders or position sizing, to manage potential losses).
All trading bots are written in Python programming language.

## Developed bots
* **CryptoTrendScreenerBot**:  trading bot for searching the intraday, swing trends on the USDT perpetual futures markets of the Bybit exchange.
* **ForexTrendScreenerBot**:  trading bot for searching the intraday, swing trends on the most traded forex pairs (majors, minors and cross).
* **PlaceTrailingStopsBotBybit**: trading bot for entering a trailing stop loss based on open futures positions on the Bybit exchange.
* **EarlyReactionBotBybit**: trading bot for close early reaction trades (A trade where the price reaches 33% before entry and then the market turns to profit).
* **CloseTradesAtTimeBotBybit**: trading bot closing pending orders and position at defined time.
* **CheckFuturesMarginLevelBotBybit**: trading bot checking sufficient margin on the futures exchange, if the margin is below the specified limit, then after the expiration of a defined time interval (2 hours intraday, 12 hours swing for example) the bot fund futures account on defined level.

## Development
Application is actively maintenance and develop.

## Prerequisites
* Python 3.11 and higher

## Exchange api documentation
* [Bybit rest api v5 documentation](https://bybit-exchange.github.io/docs/v5/intro)

## Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
     <td align="center"><a href="https://github.com/GeorgeQuantAnalyst"><img src="https://avatars.githubusercontent.com/u/112611533?v=4" width="100px;" alt=""/><br /><sub><b>GeorgeQuantAnalyst</b></sub></a><br /><a href="https://github.com/GeorgeQuantAnalyst" title="Ideas">🤔</a></td>
    <td align="center"><a href="https://github.com/LucyQuantAnalyst"><img src="https://avatars.githubusercontent.com/u/115091833?v=4" width="100px;" alt=""/><br /><sub><b>LucyQuantAnalyst</b></sub></a><br /><a href="https://github.com/LucyQuantAnalyst" title="Code">💻</a></td>
  </tr>
</table>
