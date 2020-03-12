import bitmex
import random

#Params
symbol_bx="XBTUSD"
contracts= 200
tk_profit=4
max_contracts=3*contracts
min_price=25
liq_price=450


##Initiation 
client = bitmex.bitmex(test=False, config=None, api_key="", api_secret="")

cur_candle_time=0
cur_time=datetime.datetime.utcnow()
orders_completed=0
order_price=5196.5
Mark='N'
cur_price=client.Trade.Trade_get(symbol=symbol_bx, reverse=True, count=1).result()[0][0]['price']
cur_contracts=0
order_price=1000
cntr=0
action="None"
cntr_bought=0

def myround(x, prec=2, base=0.05):
    return round(base * round(x/base),prec)
while True:
    print(datetime.datetime.utcnow().timestamp())
    past_price=cur_price
    past_contracts=cur_contracts
    past_order_price=order_price
    past_action=action
    cntr+=1
    print(cntr)
    
    ##Pull Price

    

    ##CHECK POSITIONS
    
    cur_pos=client.Position.Position_get().result()
    cur_contracts=(cur_pos[0][0]['currentQty'])
    cur_pos_main=client_main.Position.Position_get().result()
    cur_contracts_main=(cur_pos_main[0][0]['currentQty'])
    order_price=myround(cur_pos[0][0]['avgEntryPrice'],prec=1,base=0.5)

    print(f"order price: {order_price}")
    print(f"past order price: {past_order_price}")
    print(f"Current Price: {cur_price}")
    print(f"Past Price: {past_price}")
    print(f"cur_contracts: {cur_contracts}")
    print(f"past contracts: {past_contracts}")
    print(f"Mark: {Mark}")
    if past_order_price!=order_price:
        Mark="N"
    if past_contracts!=cur_contracts:
        cntr=0

    order_bk=client.OrderBook.OrderBook_getL2(symbol="XBTUSD", depth=4).result()[0]
    Sells=0
    Buys=0
    for order in order_bk:
        if order['side']=='Sell':
            Sells+=int(order['size'])
        if order['side']=='Buy':
            Buys+=int(order['size'])  
    print(Buys)
    print(Sells)  
    print(Buys/Sells)

    #Determine a trend depending on orders in the order book (Against Trend)
    if Buys<Sells:
        action="Buy"
    elif Sells<Buys:
        action="Sell"
    else:
        action="Both"

    print(action)
    cur_price=client.Trade.Trade_get(symbol=symbol_bx, reverse=True, count=1).result()[0][0]['price']
    ##PLACE ORDERS
        #Place orders depending on recommendation. Will also close out past orders if the momentum switched
    ##Entry

    if cur_price<past_price-0.5 or cur_price>past_price+0.5 or action!=past_action:
        
        ##If Sold
        if 0>cur_contracts+(cntr_bought*contracts)>-max_contracts and cur_price>=order_price+(min_price+2*abs((cur_contracts+(cntr_bought*contracts))/contracts)):
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price-300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())
            client.Order.Order_cancelAll().result()
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+0.5,   orderQty=-contracts,execInst='ParticipateDoNotInitiate').result())
            order=(client.Order.Order_new(symbol=symbol_bx, price=order_price-tk_profit, orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())
            order=(client.Order.Order_new(symbol=symbol_bx, price=order_price+liq_price, orderQty=2*cur_contracts,execInst='ParticipateDoNotInitiate').result())
            if cur_contracts==-max_contracts:
                Mark='N'
            print(1)
        
        ##If Bought
        if 0<cur_contracts-(cntr_bought*contracts)<max_contracts and cur_price<=order_price-(min_price+2*abs((cur_contracts-(cntr_bought*contracts))/contracts)):
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())
            client.Order.Order_cancelAll().result()
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price-0.5,   orderQty= contracts,execInst='ParticipateDoNotInitiate').result())
            order=(client.Order.Order_new(symbol=symbol_bx, price=order_price+tk_profit,  orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result()) 
            order=(client.Order.Order_new(symbol=symbol_bx, price=order_price-liq_price, orderQty=2*cur_contracts,execInst='ParticipateDoNotInitiate').result())
            if cur_contracts==max_contracts:
                Mark='N'
        
            print(2)
        ##If Sold or Bought, ensure the proper number of contracts are being closed
        if cur_price<order_price+min_price or cur_price>order_price-min_price:
            
            if cur_contracts<0 and Mark=='N':
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price-300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())
                client.Order.Order_cancelAll().result()
                print(order_price)
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price-tk_profit, orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price+liq_price, orderQty=2*cur_contracts,execInst='ParticipateDoNotInitiate').result())  
                Mark="Y"  
                print(3)
            if cur_contracts>0 and Mark=='N':
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())   
                client.Order.Order_cancelAll().result()
                print(order_price)
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price+tk_profit,  orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())  
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price-liq_price, orderQty=2*cur_contracts,execInst='ParticipateDoNotInitiate').result())
                Mark="Y"  
                print(4)   
        ##Places a new order            
        if cur_contracts==0:
            cntr=0
            cntr_bought=0
            
            if action=="Buy":  
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())       
                client.Order.Order_cancelAll().result()
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price-0.5, orderQty= contracts,execInst='ParticipateDoNotInitiate').result())

            elif action=="Sell":
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())  
                client.Order.Order_cancelAll().result()
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+0.5, orderQty=-contracts,execInst='ParticipateDoNotInitiate').result())
            elif action=="Both":
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())  
                client.Order.Order_cancelAll().result()
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price-0.5, orderQty= contracts,execInst='ParticipateDoNotInitiate').result())
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+0.5, orderQty=-contracts,execInst='ParticipateDoNotInitiate').result())
            print("action taken")  
            Mark="N"
            print(5)  
                            
        ## If Maximum amount of contracts are bought or sold ensure there is an order
        if abs(cur_contracts)>=max_contracts and past_contracts!=cur_contracts:
            
            if cur_contracts<0:
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())  
                client.Order.Order_cancelAll().result()
                print(order_price)
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price-tk_profit, orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price+liq_price, orderQty=2*cur_contracts,execInst='ParticipateDoNotInitiate').result())   
                Mark="Y"
                print(6)  
            if cur_contracts>0: 
                order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())    
                client.Order.Order_cancelAll().result()
                print(order_price)
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price+tk_profit,  orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())  
                order=(client.Order.Order_new(symbol=symbol_bx, price=order_price-liq_price, orderQty=2*cur_contracts,execInst='ParticipateDoNotInitiate').result())
                Mark="Y" 
                print(7)  

        ##If position is in positive but it hasnt closed for some reason... This closes it     
        if cur_contracts>0 and cur_price>order_price+4:
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())
            client.Order.Order_cancelAll().result()
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+0.5, orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())
        if cur_contracts<0 and cur_price<order_price-4:
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price+300,   orderQty=-1,execInst='ParticipateDoNotInitiate').result())
            client.Order.Order_cancelAll().result()
            order=(client.Order.Order_new(symbol=symbol_bx, price=cur_price-0.5, orderQty=-cur_contracts,execInst='ParticipateDoNotInitiate').result())    

    time.sleep(5)