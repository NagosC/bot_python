def puxador (pos,mt5):
    tipo = pos['type'][0]
    symbol = pos['symbol'][0]
    point = mt5.symbol_info(symbol).point
    sl = (pos['sl'][0])
    ticket = int (pos["ticket"][0])
    volume = pos['volume'][0]
    if tipo == mt5.ORDER_TYPE_BUY:
        tipo = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
        new_sl = sl + 100 * point
    else:
        tipo == mt5.ORDER_TYPE_BUY
        price == mt5.symbol_info_tick(symbol).ask
        new_sl = sl - 100 * point


    request_puxador = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": symbol,
        "volume": float(volume),
        "type": tipo,
        "position": ticket,
        "sl": new_sl,
        "price": price,
        "magic": 234000,
        "comment": "change stop loss",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
    return mt5.order_send(request_puxador)
    