#Important Importing
import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from Altituderegression import timeseries
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

#Loading Required Station
file = r"KTPK.txt"
n,e,u,Df = timeseries(file)

#data
y = Df

#Test Data (Uncomment to use--also modify dates and column name)
#data = sm.datasets.co2.load_pandas()
#y = data.data

#Resampling to monthly averages
# The 'MS' string groups the data in buckets by start of the month
y = y['N'].resample('MS').mean()
print(y)

# The term bfill means that we use the value before filling in missing values
y = y.fillna(y.bfill())

#Plot Data
y.plot(figsize=(15, 6))
plt.show()

#First Parameter Selection Method
#Differenciating the data
diff1 = y.diff().fillna(y)
diff2 = diff1.diff().fillna(diff1)

#Plot ACF (anything outside the shaded banded is stat. significant any line outside helps determine the number of moving average values)
plot_acf(diff2)
plt.show()

#Plot PACF (anything outside the band is useful to determine the number of autoregressive terms)
plot_pacf(diff2)
plt.show()
#SARMIAX values are ARIMA(p,d,q) with p = autoregressive terms, d = differenciating terms, q = moving average terms

#Definition for Parameter Selection for ARIMA model
def Par_sel(y):
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    #Fitting best p,d,q to dataset
    warnings.filterwarnings("ignore") # specify to ignore warning messages

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()

                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue


#Fitting an ARIMAX Time-series model
mod = sm.tsa.statespace.SARIMAX(y,
                                order=(2, 3, 4),
                                seasonal_order=(0, 0, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

#Print summary of fitted model
print(results.summary().tables[1])

#Print diagnostics of fitted model
results.plot_diagnostics(figsize=(15, 12))
plt.show()
            
#Validating Forecasts
pred = results.get_prediction(start=pd.to_datetime('2004-01-01'), dynamic=False)
pred_ci = pred.conf_int()



#### Producing and Testing non-dynamic and dynamic forecasts ####
#Non-dynamic forecast
ax = y['1999':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('Displacement')
plt.legend()
plt.show()
#Quantifying accuracy of forecasts
y_forecasted = pred.predicted_mean
y_truth = y['2004-01-01':]
# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

#Dynamic forecasts
pred_dynamic = results.get_prediction(start=pd.to_datetime('2004-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()
#Plot dynamic forecasts
ax = y['1999':].plot(label='observed', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2004-01-01'), y.index[-1],
                 alpha=.1, zorder=-1)
ax.set_xlabel('Date')
ax.set_ylabel('Displacement')
plt.legend()
plt.show()
#Second accuracy Test
# Extract the predicted and true values of our time series
y_forecasted = pred_dynamic.predicted_mean
y_truth = y['2004-01-01':]
# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))


#Producing the actual and final forecast
# Get forecast 500 steps ahead in future
pred_uc = results.get_forecast(steps=500)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()

#Plot forecast
ax = y.plot(label='observed', figsize=(20, 15))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Displacement')

plt.legend()
plt.show()
