# BinanceBot

This bot is created for sending notifications via telegram. Bot is based on Binance Future API. Work on bot is still in progress, keep that in mind (not everything works correctly) :)

**Problems:**

* fixed
  - 3 same color candles in a row, then different color candle should reset the multiple
  - create 'greens' and 'reds' at the same time before conditions   
* to fix:
  - 'while abs(difference) > 30' loop prevent dividing by zero 
  - improve 'greens' and 'reds' (add checker_value: if current_price is higher/lower than checker_value)
  - ConnectionResetError: [WinError 10054]
