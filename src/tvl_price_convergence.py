import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame as df
from scipy import stats
from pandas import Series
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)

coins_prices=pd.read_csv("C:/Users/Owner/factor_strategy/src/factor_price_data/after_pretreatment/tvl_factor_test/20181102-20220306 log_return.txt", sep = ",", encoding = "utf-8", engine = "c")
factor_exposure=pd.read_csv("C:/Users/Owner/factor_strategy/src/factor_price_data/after_pretreatment/tvl_factor_test/factor_tvl_growth.txt", sep = ",", encoding = "utf-8", engine = "c")


#設置Datetime、resample
coins_prices['Datetime']=pd.to_datetime(coins_prices['Datetime'])
log_return=coins_prices.set_index(coins_prices.Datetime).drop(columns={'Datetime'})

factor_exposure['Datetime']=pd.to_datetime(factor_exposure['Datetime'])
factor_exposure=factor_exposure.set_index(factor_exposure.Datetime).drop(columns={'Datetime'})
factor_exposure=factor_exposure.resample(rule='W',closed='left',label='right').sum(min_count=1)
log_return=log_return.resample(rule='W',closed='left',label='right').sum(min_count=1)

convergence=pd.merge(factor_exposure['ethereum'],log_return['ethereum'],how='outer',left_index=True,right_index=True).iloc[10:,]
convergence.columns=['tvl_growth','return_growth']
a=pd.DataFrame(convergence['return_growth']-convergence['tvl_growth'],columns=['TRI'])
b=pd.merge(a,convergence['return_growth'],how='outer',left_index=True,right_index=True)
b['return_growth']=b['return_growth'].cumsum()


plt.figure().set_size_inches(20,4)
plt.subplot(2, 2, 1)
np.exp(b['return_growth']).plot()
plt.xticks(rotation='vertical')
plt.grid()

plt.subplot(2, 2, 3)
np.exp(b['TRI']).plot()
plt.xticks(rotation='vertical')
plt.grid()

plt.show()
print(np.exp(b))

