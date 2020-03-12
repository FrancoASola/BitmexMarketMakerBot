# BitmexMarketMakerBot
It goes without say that this was a project for fun and profits are not expected much less guaranteed. <br>
Also, it should be noted Bitmex does not allow US traders (one of the reasons I no longer use them).
This was just a quick project that I put together in a few hours and while it did initially prove to be profitable, the indeterminacy of the cryptocurrency market proved too great for this to work properly. <br>
<br>
I did this in early 2018 during the cryptocurrency boom. Looking back on it I see that my code was rather…rudimentary. It still works fairly robustly, as long as it is running from the MarketMakerBot_XBT_always.py file (this file will keep restarting the MarketMakerBot_XBT.py file every time it crashes) as Bitmex tends to crash quite a lot. <br>

# How it works
Bitmex refunds a percentage of every buy and sell limit order. <br> 
<br>
Since you are “making market” by providing liquidity for market orders, Bitmex (and other brokers) provide a percent refund of your initial purchase as a reward for providing said liquidity. <br>
<br>
This refund can be “exploited” to earn small profits over many orders. Due to the nature of a limit order, you are buying against the trend of the market (I.E. you can only place buy orders below current price and vice versa for sell orders). 
<br>
<br>
This lends itself to automation as one can set a bot that checks the price periodically (5 seconds in this case) and sets the order one “tick” below the current price for buys and one above for sells.
