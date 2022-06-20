from get_ewma import get_ewma
import numpy
from random import randint

# для одномерного массива
# 1 -- open, -1 -- close
# open close in usd
def generate_signals(ask_prices : numpy.array, bid_prices : numpy.array,
                     open_threshold : float, close_threshold : float,
                     window_size_long : int,
                     window_size_short : int,
                     last_weight : float) -> numpy.array:
    window_size_long = int(window_size_long)
    window_size_short = int(window_size_short)
    
    ask_short = get_ewma(ask_prices, window_size_short, last_weight)
    ask_long = get_ewma(ask_prices, window_size_long, last_weight)
    bid_short = get_ewma(bid_prices, window_size_short, last_weight)
    bid_long = get_ewma(bid_prices, window_size_long, last_weight)

    ask_short = ask_short[-len(ask_long):]
    bid_short = bid_short[-len(bid_long):]

    diff_long = (ask_long - bid_long) / ((ask_prices[-len(ask_long):] + bid_prices[-len(bid_long):]) / 2.)
    diff_short = (ask_short - bid_short) / ((ask_prices[-len(ask_long):] + bid_prices[-len(bid_long):]) / 2.)

    comprator = lambda long, short : 1 if short - long > open_threshold else (-1 if long - short < close_threshold else 0)
    # в строчке выше я пробоввал все комбинации смены 1 и -1 местами, менял знаки меньше на больше
    # и пробовал отнимать шорт от лонга и наоборот
    # изменилось +- ничего

    signals = numpy.concatenate((numpy.zeros(len(ask_prices) - len(ask_long)), 
                                 numpy.array(list(map(comprator, diff_long, diff_short)))), 
                                axis=0)

    # две следующие строчки делают сигналы рандомными                                
    # for i in range(len(signals)):
    #    signals[i] = randint(-1, 1)
    return signals
