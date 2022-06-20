import numpy


class Event:
    index = 100500 # index in ask_price\bid_price
    timestamp = -1
    ask_price = 300
    bid_price = 300
    signal = 300

    def __init__(self, i, ts, ask, bid, s) -> None:
        self.index = i
        self.timestamp = ts
        self.ask_price = ask
        self.bid_price = bid
        self.signal = s

class Adding:
    usd = 0.
    timestamp = -1
    index = 100500

    def __init__(self, u, ts, i) -> None:
        self.usd = u
        self.timestamp = ts
        self.index = i


# тут тоже  все одномерное торгуем одной монеткой
# а вот хуй, тут уже обязательно видимо не одномерное...
def run_backtest(ask_prices : numpy.array,
                 bid_prices : numpy.array,
                 timestamps : numpy.array,
                 signals_array : numpy.array,
                 max_position_usd : float,
                 commission : float,
                 delay : float,
                 start_usd : float):

    events = [] # да лист это колхоз а что вы мне сделаете, я в другом городе (я реально в другом городе у вышки общаги за мкадом лол)
    for i in range(ask_prices.shape[0]):
        for j in range(bid_prices.shape[1]):
            events.append(Event(i, timestamps[i][j], ask_prices[i][j],
            bid_prices[i][j], signals_array[i][j]))
    events.sort(key=lambda event : event.timestamp)
    USL_LOG = []
    CUR_USL = [] # первые len(ask_prices) значений -- количество соответствущих монеток, ask_price -- текущая сумма usd
    CUR_USL = [0.] * len(ask_prices) + [start_usd]
    USL_LOG.append(CUR_USL)
    addings = []
    for event in events:
        new_addings = []
        for adding in addings:
            if adding.timestamp <= event.timestamp:
                CUR_USL[adding.index] += adding.usd
            else:
                new_addings.append(adding)
        addings = new_addings

        if event.signal == -1:
            addings.append(Adding((event.bid_price * CUR_USL[event.index] * (1. - commission)),
                              event.timestamp + delay, -1))
            CUR_USL[event.index] = 0
        if event.signal == 1:
            buy_sum = min(CUR_USL[-1], max_position_usd)
            addings.append(Adding(event.timestamp, (event.ask_price / buy_sum * (1. - commission)), event.index))
            CUR_USL[-1] -= buy_sum
        USL_LOG.append(CUR_USL)
    for adding in addings:
        CUR_USL[adding.index] += adding.usd
    USL_LOG.append(CUR_USL)
    return USL_LOG
