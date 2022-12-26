import MetaTrader5 as mt5
import pandas as pd
import indicador as ind
from tempo import main
from pandas_ta import ma

#inicializa o meta trader
if not mt5.initialize():
    print('falha na inicialização')
    mt5.shutdown()

#pega o ativo 
def get_ohlc(simbolo, timeframe, n=250):
    ativo = mt5.copy_rates_from_pos(simbolo,timeframe,0,n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit="s")
    #ativo.set_index('time', inplace=True)
    return ativo


#verifica se o sibolo usado é válido 
symbol = "XAUUSD"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"Simbolo {symbol} não achado... tentando adiciona-lo")
    mt5.shutdown()
else:
    print( f'{symbol} Achado com sucesso' )

# se o símbolo não estiver disponível no MarketWatch, adicionamo-lo
    if not mt5.symbol_select(symbol,True):
        print(f"symbol_select({symbol}) failed, exit")
        mt5.shutdown()

def robo():
    ativo = (get_ohlc('XAUUSD',mt5.TIMEFRAME_M5))
    fechamento = list(ativo['close'])
    posicao = mt5.positions_get(symbol= "XAUUSD")
    order   = mt5.orders_get(symbol= "XAUUSD")
    tenkan = list(ind.ichimoku(ativo)[0])
    kijun  = list(ind.ichimoku(ativo)[1])
    mediaL = list(ma('sma',ativo['close'], length = 200))

    lot = 0.01
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 1
    requestcompra = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 350 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
    }


    lot = 0.01
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 1
    requestvenda = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + 350 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "order": 115340,
    }   
    

    if tenkan[-1] > kijun[-1] and tenkan[-2] <= kijun[-2] and tenkan[-1] > mediaL[-1] and  kijun[-1] > mediaL [-1] and fechamento[-1] > kijun[-1] and fechamento[-1] > mediaL[-1]:
        if posicao == () and  order == ():
            resultado = mt5.order_send(requestcompra)
            print(resultado)
            print(f'Compra realizada no {symbol}')
            


    if tenkan[-1] < kijun[-1] and tenkan[-2] >= kijun[-2] and tenkan[-1] < mediaL[-1] and kijun[-1] < mediaL[-1] and fechamento[-1] < kijun[-1] and fechamento[-1] < mediaL[-1]:
        if posicao == () and  order == () :
            resultado = mt5.order_send(requestvenda)
            print(resultado)
            print(f'Venda realizada no {symbol}')


    if posicao != ():
        pos = pd.DataFrame(list(posicao),columns=posicao[0]._asdict().keys())
        sl = pos['sl'][0]
        tipo = pos['type'][0]
        if tipo == mt5.ORDER_TYPE_BUY:
            Psl = sl + 450 * point
            if price > Psl:
                puxador(pos,mt5)
        else:
            Psl = sl - 450 * point    
            if price < Psl:
                puxador(pos,mt5)


    
if __name__ == "__main__":    
    main(robo , interval= 30)


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
        new_sl = sl + 150 * point
    else:
        tipo = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
        new_sl = sl - 150 * point


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
    mt5.order_send(request_puxador)

    