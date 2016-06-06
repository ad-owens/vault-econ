# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 17:19:22 2015

@author: aowens
"""

from pyearth import Earth
from matplotlib import pyplot
import pandas as pd
from pandas import DataFrame
import numpy as np
    
    

#Import Data
data = pd.read_clipboardsv('/Users/aowens/Documents/SEM Research/Gears Performance/Bidding Analysis/Rounds Regressions 5 - no brand.csv')
df_origin = DataFrame(data)
orig_bid_price_adj = df_origin['Bid Price Adj']

##### Adjust the Bid level####

#bid_range=np.arange(-1,1,.01)

bid_range = (1,2,3)

for i in bid_range:
    bid_adjust =bid_range(i)
    
###Fix me!###
df_cpc = df_origin.copy()

del df_cpc['Bid Price Adj']
df_cpc['Bid Price Adj']= bid_adjust*df_origin['OLD_AVG_NEW_MAX_BID']

est_bid_price_adj=df_cpc['Bid Price Adj']

#CPC Model    
y_cpc = df_origin['New Avg_CPC']
X = df_origin[['Old ROI', 
         'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         'New Conv_Rate',
         'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         #'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         'New Value_Click',
         'Old Value_Click']]
 
#Fit an Earth model
model = Earth(max_degree=1, max_terms=40)
model.fit(X,y_cpc)

print model.trace()
print model.summary()

X_cpc_hat = df_cpc[['Old ROI', 
         'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         'New Conv_Rate',
         'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         #'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         'New Value_Click',
         'Old Value_Click']]

#Print the model
print model.trace()
print model.summary()

y_cpc_hat = model.predict(X_cpc_hat)

#Plot the model

pyplot.figure()
pyplot.plot(y_cpc,'r.')
pyplot.plot(y_cpc_hat,'b.')
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title('MARS Regression')
pyplot.show()


'''
#Build Conv_Rate Model
#Build conv table
df_conv = df_origin.copy()

del df_conv['Bid Price Adj']
df_conv['Bid Price Adj']= bid_adjust*df_origin['OLD_AVG_NEW_MAX_BID']
del df_conv['New Avg_CPC']
df_conv['New Avg_CPC']=y_cpc_hat

#MARS model for conv table
y_conv = df_origin['New Conv_Rate']
X_conv = df_origin[['Old ROI', 
         #'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         #'New Conv_Rate',
         #'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         #'New Value_Click',
         'Old Value_Click']]

model = Earth(max_degree=3, max_terms=40)
model.fit(X_conv,y_conv)

print model.trace()
print model.summary()

X_conv_hat = df_conv[['Old ROI', 
         #'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         #'New Conv_Rate',
         #'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         #'New Value_Click',
         'Old Value_Click']]

y_conv_hat = model.predict(X_conv_hat)

#Plot the model

pyplot.figure()
pyplot.plot(df_origin['New Conv_Rate'],'r.')
pyplot.plot(y_conv_hat,'b.')
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title('MARS Regression')
pyplot.show()

#Build Value_Click Model Table
df_value = df_origin.copy()

del df_value['Bid Price Adj']
df_value['Bid Price Adj']= bid_adjust*df_origin['OLD_AVG_NEW_MAX_BID']
del df_value['New Avg_CPC']
df_value['New Avg_CPC']=y_cpc_hat
#del df_value['New Conv_Rate']
#df_value['New Conv_Rate']=y_conv_hat

#MARS value model
y_value = df_origin['New Value_Click']
X_value = df_origin[['Old ROI', 
         'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         'New Conv_Rate',
         #'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         #'New Value_Click',
         'Old Value_Click']]

model = Earth(max_degree=2, max_terms=40)
model.fit(X_value,y_value)

print model.trace()
print model.summary()

X_value_hat = df_value[['Old ROI', 
         'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         'New Conv_Rate',
         #'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         #'New Value_Click',
         'Old Value_Click']]

y_value_hat = model.predict(X_value_hat)

#Plot the model

pyplot.figure()
pyplot.plot(df_origin['New Value_Click'],'r.')
pyplot.plot(y_value_hat,'b.')
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title('MARS Regression')
pyplot.show()
'''
#Build Predict ROI Table

df_ROI = df_origin.copy()

del df_ROI['Bid Price Adj']
df_ROI['Bid Price Adj']= bid_adjust*df_origin['OLD_AVG_NEW_MAX_BID']
del df_ROI['New Avg_CPC']
df_ROI['New Avg_CPC']=y_cpc_hat
#del df_ROI['New Conv_Rate']
#df_ROI['New Conv_Rate']=y_conv_hat
#del df_ROI['New Value_Click']
#df_ROI['New Value_Click']=y_value_hat

y_ROI = df_origin['New ROI']
X_ROI = df_origin[['Old ROI', 
         #'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         'New Conv_Rate',
         #'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         'New Value_Click',
         'Old Value_Click']]

model = Earth(max_degree=3, max_terms=40)
model.fit(X_ROI,y_ROI)

print model.trace()
print model.summary()

X_ROI_hat = df_ROI[['Old ROI', 
         #'Old Adj_Value', 
         'Old Conv_Rate',
         'Old Contr_Per_offer', 
         'Bid Price Adj',  
         'OLD_AVG_NEW_MAX_BID', 
         'New Conv_Rate',
         #'New Contr_Per_offer',                 
         'New CTR',
         'Old CTR', 
         'New Qual_Score', 
         'Old Qual_Score',
         'Old Avg_Position',
         'Old Impressions',
         'New Impressions',
         'New Avg_CPC',
         'Old Avg_CPC',
         'New Keyword Density', 
         'Old Keyword Density',
         'New Value_Click',
         'Old Value_Click']]

y_ROI_hat = model.predict(X_ROI_hat)

#Plot the model

pyplot.figure()
pyplot.plot(df_origin['New ROI'],'r.')
pyplot.plot(y_ROI_hat,'b.')
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title('MARS Regression')
pyplot.show()

df_ROI['y_ROI_errors']=df_origin['New ROI']-y_ROI_hat

print 'Bid Price Adj: '+str(np.mean(orig_bid_price_adj))
print 'Adj Bid Price Ajd: '+str(np.mean(est_bid_price_adj))
print '----------'
print 'Predicted Mean Avg_CPC: '+str(np.mean(y_cpc_hat))
print 'Mean Avg_CPC: '+str(np.mean(y_cpc))
print '----------'
print 'Predicted Mean ROI: '+str(np.mean(y_ROI_hat))
print 'Mean ROI: '+str(np.mean(df_origin['New ROI']))
#print 'Predicted Mean Value_Click: '+str(np.mean(y_value_hat))
#print 'Predicted Max Value_Click: '+str(np.max(y_value_hat))
#print 'Mean Value_Click: '+str(np.mean(y_value))
#print 'Max Value_Click: '+str(np.max(y_value))
print '----------'
print 'Predicted Max Avg_CPC: '+str(np.max(y_cpc_hat))
print 'Max Avg_CPC: '+str(np.max(y_cpc))
print '----------'
print 'Predicted Max ROI: ' +str(np.max(y_ROI_hat))
print 'Max ROI: '+str(np.max(df_origin['New ROI']))

df_ROI['y_ROI_hat']=y_ROI_hat
#save results to file

np.savetxt("y_ROI_hat.csv", df_ROI(), delimiter=";")
