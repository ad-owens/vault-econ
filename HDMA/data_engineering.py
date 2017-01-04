import pandas as pd
import csv
import requests
import glob
import time

start_time = time.time()

#/////////////////////  Pull 2010-2015 samples from hdma API  /////////////////////

def get_hdma(year, limit, offset):
    
    headers = {"Content-Type":"text/csv;charset=UTF-8"}
    
    url = 'https://api.consumerfinance.gov:443/data/hmda/slice/hmda_lar.csv?%24where=as_of_year%3D'+str(year)+'&%24limit='+str(limit)+'&%24offset='+str(offset)
  
    print url  #just checking....
    
    response = requests.get(url, headers=headers, verify=False)
    hdma_csv = response.content
    
    file_name = 'hdma_data/hdma'+ str(year) +'.csv'

    text_file = open(file_name, "w")
    text_file.write(hdma_csv)
    text_file.close()

##### Define parameters for API pull
years = [2010, 2011, 2012, 2013, 2014, 2015]
size = 60000
sample_offset = 200

for i in years:
    get_hdma(i, size, sample_offset)

print("--- API Pull Finished: %s minutes  ---" % str((time.time() - start_time)/60))

#/////////////////////  Separate Dummy and Continuous Variables  /////////////////////

dummy_variables = ['agency_name','applicant_ethnicity_name','applicant_race_name_1',
                   'applicant_race_name_2','applicant_race_name_3','applicant_race_name_4','applicant_race_name_5',
                   'applicant_sex_name','application_date_indicator','as_of_year','co_applicant_ethnicity_name',
                   'co_applicant_race_name_1','co_applicant_race_name_2','co_applicant_race_name_3','co_applicant_race_name_4',
                   'co_applicant_race_name_5','co_applicant_sex_name','county_name','denial_reason_name_1',
                   'denial_reason_name_2','denial_reason_name_3','edit_status_name','hoepa_status_name',
                   'lien_status_name','loan_purpose_name','loan_type_name','msamd_name','owner_occupancy_name',
                   'preapproval_name','property_type_name','purchaser_type_name','state_abbr','respondent_id']
                   
                  #included classification variable in cont_variables
cont_variables = ['action_taken','action_taken_name','applicant_income_000s','census_tract_number','sequence_number',
                'hud_median_family_income','loan_amount_000s','number_of_1_to_4_family_units',
                 'number_of_owner_occupied_units','minority_population','population','rate_spread',
                 'tract_to_msamd_income']    

def split_hdma_df(df):
    df_dummy = pd.get_dummies(df[dummy_variables])
    df_cont = df[cont_variables]    
    
    df_total = pd.concat([df_cont,df_dummy], axis = 1)
    
    print "Dummy Dataframe Shape:"+str(df_dummy.shape)
    print "Continuous Dataframe Shape:"+str(df_cont.shape)
    print "Total Data Shape:"+str(df_total.shape)
    
    return df_total

#/////////////////////  Combine all dataframes split variable types  /////////////////////

path = "hdma_data"
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0, low_memory=False)
    list_.append(df)

df_total = pd.concat(list_)

df_featured = split_hdma_df(df_total).to_csv('hdma_total.csv', index=False)

print("--- Total Time:%s minutes ---" % str((time.time() - start_time)/60))
