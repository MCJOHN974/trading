import pandas
import numpy
from generate_signals import generate_signals
from run_backtest import run_backtest
from count_earnings import count_earnings
from scipy import optimize


# Пробуем посмотреть на данные
bchusdt = pandas.read_pickle("pkls/bchusdt_fut_ob.pkl")
btcusdt = pandas.read_pickle("pkls/btcusdt_fut_ob.pkl")
ethusdt = pandas.read_pickle("pkls/ethusdt_fut_ob.pkl")
ltcusdt = pandas.read_pickle("pkls/ltcusdt_fut_ob.pkl")
solusdt = pandas.read_pickle("pkls/solusdt_fut_ob.pkl")
xrpusdt = pandas.read_pickle("pkls/xrpusdt_fut_ob.pkl")

ask_price_bch = numpy.array(bchusdt.ask_price)
ask_price_btc = numpy.array(btcusdt.ask_price)
ask_price_eth = numpy.array(ethusdt.ask_price)
ask_price_ltc = numpy.array(ltcusdt.ask_price)
ask_price_sol = numpy.array(solusdt.ask_price)
ask_price_xrp = numpy.array(xrpusdt.ask_price)

bid_price_bch = numpy.array(bchusdt.bid_price)
bid_price_btc = numpy.array(btcusdt.bid_price)
bid_price_eth = numpy.array(ethusdt.bid_price)
bid_price_ltc = numpy.array(ltcusdt.bid_price)
bid_price_sol = numpy.array(solusdt.bid_price)
bid_price_xrp = numpy.array(xrpusdt.bid_price)

timestamp_bch = numpy.array(bchusdt.timestamp)
timestamp_btc = numpy.array(btcusdt.timestamp)
timestamp_eth = numpy.array(ethusdt.timestamp)
timestamp_ltc = numpy.array(ltcusdt.timestamp)
timestamp_sol = numpy.array(solusdt.timestamp)
timestamp_xrp = numpy.array(xrpusdt.timestamp)

# variable params
open_treshold = 0.01
close_treshhold = 0.001
window_size_long = 500
window_size_short = 100
last_weight = 0.5
max_position_usd = 100

# const params
comission = 0.0001
delay = 1
start_usd = 100000.

# tmp param
data_part = 1000 # я запускал на 10000 то же самое получается



def test_params(open_treshold = 0.01,
                close_treshhold = 0.001,
                window_size_long = 500,
                window_size_short = 100,
                last_weight = 0.5,
                max_position_usd = 100,
                begin = 0,
                end = data_part):
    # print("Start signal generating")
    signals = [generate_signals(ask_price_bch[begin:end], bid_price_bch[begin:end], open_treshold, close_treshhold, window_size_long, window_size_short, last_weight),
               generate_signals(ask_price_btc[begin:end], bid_price_btc[begin:end], open_treshold, close_treshhold, window_size_long, window_size_short, last_weight),
               generate_signals(ask_price_eth[begin:end], bid_price_eth[begin:end], open_treshold, close_treshhold, window_size_long, window_size_short, last_weight),
               generate_signals(ask_price_ltc[begin:end], bid_price_ltc[begin:end], open_treshold, close_treshhold, window_size_long, window_size_short, last_weight),
               generate_signals(ask_price_sol[begin:end], bid_price_sol[begin:end], open_treshold, close_treshhold, window_size_long, window_size_short, last_weight),
               generate_signals(ask_price_xrp[begin:end], bid_price_xrp[begin:end], open_treshold, close_treshhold, window_size_long, window_size_short, last_weight)]
    # print("Signal generating ends")
    ask_prices = [ask_price_bch[begin:end],
                  ask_price_btc[begin:end],
                  ask_price_eth[begin:end],
                  ask_price_ltc[begin:end],
                  ask_price_sol[begin:end],
                  ask_price_xrp[begin:end]]
    bid_prices = [bid_price_bch[begin:end],
                  bid_price_btc[begin:end],
                  bid_price_eth[begin:end],
                  bid_price_ltc[begin:end],
                  bid_price_sol[begin:end],
                  bid_price_xrp[begin:end]]
    timestamps = [timestamp_bch[begin:end],
                  timestamp_btc[begin:end],
                  timestamp_eth[begin:end],
                  timestamp_ltc[begin:end],
                  timestamp_sol[begin:end],
                  timestamp_xrp[begin:end]]
    # print("Backtest started")
    LOG_USL = run_backtest(numpy.array(ask_prices), numpy.array(bid_prices), numpy.array(timestamps), 
                           numpy.array(signals), max_position_usd, comission, delay, start_usd)
    # print("Backtest finished")
    earnings = count_earnings(LOG_USL, bid_prices, comission)
    # print(f"Total earnings = {earnings- start_usd}")
    return -1. * earnings


def test_params_evo2(lst):
    return test_params(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5])


def test_params_evo3(lst):
    return test_params(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], data_part, 2 * data_part)


sol = optimize.differential_evolution(test_params_evo2, 
                                     [(0., 1.), (0., 1.), (100, 1000), (1, 100), (0., 0.5), (1, 1000)],
                                     args=(),
                                     strategy='best1bin',
                                     maxiter=1000,
                                     popsize=15,
                                     tol=0.01,
                                     mutation=(0.5, 1), 
                                     recombination=0.7, 
                                     seed=None, 
                                     callback=None, 
                                     disp=False, 
                                     polish=True, 
                                     init='latinhypercube', 
                                     atol=0, 
                                     updating='immediate', 
                                     workers=-1, 
                                     constraints=(), 
                                     x0=None)
print(f"Train results:\n args = {sol.x}\nvalue =  {-1. * sol.fun}")
print(f"Test results:\n value = {-1. * test_params_evo3(sol.x)}")
