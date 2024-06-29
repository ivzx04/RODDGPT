from polygon import RESTClient
import  pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
from dateutil import rrule
from mplfinance.original_flavor import candlestick_ohlc


#this is an example file to show how to use some of our APIS, they use the rest API format and 
# return data in these Agg objects which will take some time to learn, the important thing is 
# with this we can easily query for data (although i had a bit of a tough time displaying it 
# correcty lmao) candlesticks are kinda hard to graph

AUTH_STR = ""

client = RESTClient(AUTH_STR)


price_data = client.get_aggs(ticker = "AAPL",
                            timespan= "day",
                            multiplier = 1, 
                            from_ = '2024-01-01',
                            to=  '2024-01-10')

df = pd.DataFrame(price_data)
ohlc = df.loc[:, ['open', 'high', 'low', 'close']] 


start = datetime.datetime(2024, 1, 1)
end = datetime.datetime(2024, 1, 9)
rule = rrule.rrule(dtstart=start, freq=rrule.DAILY,
    byweekday=[rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR]
)
date_range = rule.between(start, end, inc=True)
ohlc['Date'] = date_range

ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num) 
ohlc = ohlc.astype(float) 
  
fig, ax = plt.subplots() 
  
candlestick_ohlc(ax, ohlc.values, width=0.6, 
                 colorup='green', colordown='red', alpha=0.8) 

ax.set_xlabel('Date') 
ax.set_ylabel('Price') 
fig.suptitle('Daily Candlestick Chart of AAPL') 
  
# Formatting Date 
date_format = mpl_dates.DateFormatter('%d-%m-%Y') 
ax.xaxis.set_major_formatter(date_format) 
fig.autofmt_xdate() 
  
fig.tight_layout() 
  
plt.show() 