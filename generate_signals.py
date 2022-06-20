from get_ewma import get_ewma
import numpy


# для одномерного массива
# 1 -- open, -1 -- close
def generate_signals(ask_prices : numpy.array, bid_prices : numpy.array,
                     open_threshold : int, close_threshold : int,
                     window_size_long : int,
                     window_size_short : int,
                     last_weight : int) -> numpy.array:
    
    ask_short = get_ewma(ask_prices, window_size_short, last_weight)
    ask_long = get_ewma(ask_prices, window_size_long, last_weight)
    bid_short = get_ewma(bid_prices, window_size_short, last_weight)
    bid_long = get_ewma(bid_prices, window_size_long, last_weight)

    ask_short = ask_short[-len(ask_long):]
    bid_short = bid_short[-len(bid_long):]

    diff_long = ask_long - bid_long
    diff_short = ask_short - bid_short

    comprator = lambda long, short : 1 if short - long > open_threshold else (-1 if short - long < close_threshold else 0)

    signals = numpy.concatenate((numpy.zeros(len(ask_prices) - len(ask_long)), 
                                 numpy.array(list(map(comprator, diff_long, diff_short)))), 
                                axis=0)
    return signals
