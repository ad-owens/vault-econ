# HDMA Classification Prediction

The python scripts and data contained in this folder is a machine learning exercise to predict the outcome of loan applications.  This analysis focuses on Decition Trees, Gradiented Boosted Machines (XGBoost), and Neural Nets.  The data is provided by the Consumer Finance Protection Bureau as part of the Home Mortgage Disclosure Act (HDMA) http://www.consumerfinance.gov/data-research/hmda/.

The data_engineering.py script utilizes the HDMA API to pull the data and transform categorical data into dummy variables.  The HDMA is very large at 100 GB spreading from 2007-2015 and transforming categorical variables would greatly increase size.  This analysis focuses on post-crisis housing from 2010-2015 and samples only 10,000 each year.  


