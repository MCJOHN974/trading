import pandas
from get_ewma import get_ewma
from generate_signals import generate_signals
from run_backtest import run_backtest
from count_earnings import count_earnings


# Пробуем посмотреть на данные
bchusdt = pandas.read_pickle("pkls/bchusdt_fut_ob.pkl")
btcusdt = pandas.read_pickle("pkls/btcusdt_fut_ob.pkl")
ethusdt = pandas.read_pickle("pkls/ethusdt_fut_ob.pkl")
ltcusdt = pandas.read_pickle("pkls/ltcusdt_fut_ob.pkl")
solusdt = pandas.read_pickle("pkls/solusdt_fut_ob.pkl")
xrpusdt = pandas.read_pickle("pkls/xrpusdt_fut_ob.pkl")

ask_price_bch = bchusdt.ask_price
print(ask_price_bch)
