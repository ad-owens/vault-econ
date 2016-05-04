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
import seaborn as sns


######## Import Data ###########

data = pd.read_csv('~/datascience/hotels.csv')
df_origin = DataFrame(data)
orig_bid_price_adj = df_origin['Bid Price Adj']
y_cpc = df_origin['New Avg_CPC']

########## CPC Model #############
X = df_origin[['Old ROI', 
               'Old Adj_Value', 
               'Old Conv_Rate',
               'Old Contr_Per_offer', 
               'Bid Price Adj', 
               'OLD_AVG_NEW_MAX_BID', 
               'New Conv_Rate',
               'New Contr_Per_offer',
               'New CTR','Old CTR', 
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

############ Fit an Earth model ##############
model_cpc = Earth(max_degree=1, max_terms=40)
model_cpc.fit(X,y_cpc)
print model_cpc.trace()
print model_cpc.summary()

####### Adjust the Bid level ##########
bid_range = np.arange(-1,1.01,.01)

########## make new dataframes for regression and output tables ###########
df_bid_adj=pd.DataFrame(bid_range, index=bid_range)
df_bid_adj['Predicted Mean CPC','Mean Avg_CPC','Predicted Mean ROI','Mean ROI'] 

bid_adjust_cpc= []
bid_adjust_roi= []
df_cpc = df_origin.copy()
    
for i in bid_range:
    df_cpc['Bid Perc Adj'] = i
    df_cpc['Bid Price Adj']=df_origin['OLD_AVG_OLD_MAX_BID']*i
    est_bid_adjust=df_cpc['Bid Price Adj']
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
    y_cpc_hat = model_cpc.predict(X_cpc_hat)
    bid_adjust_cpc.append(np.mean(y_cpc_hat))
    
    print 'Bid Change Level: '+str(np.mean(df_cpc['Bid Perc Adj']))
    print 'Predicted Mean Avg_CPC: '+str(np.mean(y_cpc_hat))
    print 'Mean Avg_CPC: '+str(np.mean(y_cpc))

############# Print the model ######
print model_cpc.trace()
print model_cpc.summary()

########### Plot the model ############

pyplot.figure()
pyplot.plot(y_cpc,'r.')
pyplot.plot(y_cpc_hat,'b.')
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title('MARS Regression')
pyplot.show()

###########Build Predict ROI Table#############

df_ROI = df_origin.copy()

del df_ROI['Bid Price Adj']
df_ROI['Bid Price Adj']= bid_adjust*df_origin['OLD_AVG_NEW_MAX_BID']
del df_ROI['New Avg_CPC']
df_ROI['New Avg_CPC']=y_cpc_hat

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

########## Plot the model #############
pyplot.figure()
pyplot.plot(df_origin['New ROI'],'r.')
pyplot.plot(y_ROI_hat,'b.')
pyplot.xlabel('x')
pyplot.ylabel('y')
pyplot.title('MARS Regression')
pyplot.show()

df_ROI['y_ROI_errors']=df_origin['New ROI']-y_ROI_hat

print 'Bid Price Adj: '+str(np.mean(orig_bid_price_adj))
print 'Adj Bid Price Ajd: '+str(np.mean(est_bid_adj))
print '----------'
print 'Predicted Mean Avg_CPC: '+str(np.mean(y_cpc_hat))
print 'Mean Avg_CPC: '+str(np.mean(y_cpc))
print '----------'
print 'Predicted Mean ROI: '+str(np.mean(y_ROI_hat))
print 'Mean ROI: '+str(np.mean(df_origin['New ROI']))
print '----------'
print 'Predicted Max Avg_CPC: '+str(np.max(y_cpc_hat))
print 'Max Avg_CPC: '+str(np.max(y_cpc))
print '----------'
print 'Predicted Max ROI: ' +str(np.max(y_ROI_hat))
print 'Max ROI: '+str(np.max(df_origin['New ROI']))

df_ROI['y_ROI_hat']=y_ROI_hat

#save results to file
np.savetxt("y_ROI_hat.csv", df_ROI(), delimiter=";")
