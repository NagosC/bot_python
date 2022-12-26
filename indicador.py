def ichimoku (ativo):
    high9  = ativo.high.rolling(9).max()
    low9   = ativo.high.rolling(9).min()
    high26 = ativo.high.rolling(44).max()
    low26  = ativo.high.rolling(44).min()
    high52 = ativo.high.rolling(52).max()
    low52  = ativo.high.rolling(52).min()


    tenkan= (high9 + low9) / 2
    kijun  = (high26 + low26) / 2
    senkou_A = ((tenkan + kijun) / 2 ).shift(26)
    senkou_B = ((high52 + low52)/ 2).shift(26)

    return tenkan, kijun, senkou_A, senkou_B
    
