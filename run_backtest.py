import numpy


class Event:
    index = 100500 # index in ask_price\bid_price
    timestamp = -1
    ask_price = 300
    bid_price = 300
    signal = 300

    def __init__(self, i, ts, ask, bid, s) -> None:
        self.index = i + 0
        self.timestamp = ts + 0
        self.ask_price = ask + 0.
        self.bid_price = bid + 0.
        self.signal = s + 0

id_count = 0
class Adding:
    id = -1
    value = 0.
    timestamp = -1
    index = 100500

    def __init__(self, v, ts, i) -> None:
        global id_count
        assert v >= 0.
        self.id = id_count
        id_count += 1
        self.value = v + 0.
        self.timestamp = ts + 0
        self.index = i + 0

used_id = {}

# я сюда всякие разные сигналы скармливал никогда не давало потратить больше чем денег есть
# звучит неплохо
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
                CUR_USL[adding.index] += adding.value
                assert adding.id not in used_id.keys()
                used_id[adding.id] = "bebra"
            else:
                new_addings.append(adding)
        addings = new_addings
        if event.signal == -1 and CUR_USL[event.index] > 0.:
            addings.append(Adding((CUR_USL[event.index] * event.bid_price * (1. - commission)),
                                   event.timestamp + delay, -1))
            CUR_USL[event.index] = 0
        if event.signal == 1:
            buy_sum = min(CUR_USL[-1], max_position_usd)
            addings.append(Adding((buy_sum / event.ask_price * (1. - commission)), 
                                   event.timestamp + delay, event.index))
            CUR_USL[-1] -= buy_sum
            assert CUR_USL[-1] >= 0.
        USL_LOG.append(CUR_USL)
        # print(f"CUR_USL = {CUR_USL}")
    for adding in addings:
        CUR_USL[adding.index] += adding.value
    USL_LOG.append(CUR_USL)
    return USL_LOG
