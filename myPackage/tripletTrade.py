from Investar import Analyzer
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestock_ohlc
import matplotlib.dates as mdates

mk = Analyzer.MarketDB()
df = mk.get_daily_price("엔씨소프트", "2017-01-01")