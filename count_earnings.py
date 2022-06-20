

def count_earnings(LOG_USL, ask_prices, comission):
    ask = ask_prices[-1]
    return sum(list(map(lambda coin, price : coin * price * (comission - 1), LOG_USL[-1], ask))) + (1. - comission) * LOG_USL[-1][-1]
