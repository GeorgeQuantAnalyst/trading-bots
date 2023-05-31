#!/bin/bash

BOT_NAMES=("early-reaction-bot-bybit-intraday" \
"early-reaction-bot-bybit-swing" \
"early-reaction-bot-bybit-position" \
"place-trailing-stops-bot-bybit-intraday" \
"place-trailing-stops-bot-bybit-swing" \
"place-trailing-stops-bot-bybit-position" \
"check-futures-margin-level-bot-bybit-intraday" \
"crypto-trend-screener-bot" \
"forex-trend-screener-bot")

ERRORS_LOG_PATHS=("${HOME}/log/early-reaction-bot-bybit-intraday/early_reaction_bot_bybit_intraday_error.log" \
"${HOME}/log/early-reaction-bot-bybit-swing/early_reaction_bot_bybit_swing_error.log" \
"${HOME}/log/early-reaction-bot-bybit-position/early_reaction_bot_bybit_position_error.log" \
"${HOME}/log/place-trailing-stops-bot-bybit-intraday/place_trailing_stops_bot_bybit_intraday_error.log" \
"${HOME}/log/place-trailing-stops-bot-bybit-swing/place_trailing_stops_bot_bybit_swing_error.log" \
"${HOME}/log/place-trailing-stops-bot-bybit-position/place_trailing_stops_bot_bybit_position_error.log" \
"${HOME}/log/check-futures-margin-level-bot-bybit-intraday/check_futures_margin_level_bot_bybit_intraday_error.log" \
"${HOME}/log/crypto-trend-screener-bot/crypto_trend_screener_bot_error.log" \
"${HOME}/log/forex-trend-screener-bot/forex_trend_screener_bot_error.log")


echo "---------------------------------------------------"
echo Trading bots errors monitor
echo "---------------------------------------------------"

echo
echo

for i in "${!BOT_NAMES[@]}"
do
	echo "********************************************"
	echo "# ${BOT_NAMES[$i]}"
	echo "********************************************"
	echo
	echo "## List of errors in app (last 5)"
	echo
	grep "ERROR"  -B 1 ${ERRORS_LOG_PATHS[$i]} | tail -10
	tail -1 ${ERRORS_LOG_PATHS[$i]}
	echo
done
