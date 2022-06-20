def count_earnings(LOG_USL, bid_prices, comission):
    bid = []
    for i in range(len(bid_prices)):
        bid.append(bid_prices[i][-1])
    res = (1. - comission) * LOG_USL[-1][-1]
    for i in range(len(bid)):
        res += bid[i] * LOG_USL[-1][i] * (1. - comission)
    return res
