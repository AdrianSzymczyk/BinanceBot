# BinanceBot

This bot is created for sending notifications via telegram. For now there are two periods of time (~~1min~~, 5min, 15min). Bot is based on Binance Future API. Work on bot is still in progress, keep that in mind (not everything works correctly) :)

**Task list**
- [ ] Run the project on google cloud server 
- [ ] Create and configure notification sending on telegram

**Problems:**

* fixed
  - 3 same color candles in a row, then different color candle should reset the multiple
  - create 'greens' and 'reds' at the same time before conditions   
  - improve 'greens' and 'reds'
* to fix:
  - 'while abs(difference) > 20' loop prevent dividing by zero (somewhat repaired)
  - ConnectionResetError: [WinError 10054] (unable to fix, it occurs when 'get_price' method is called by two processes in the same time)

