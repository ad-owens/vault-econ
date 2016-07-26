
import sqlite3
from pandas.io import sql
import pandas as pd
import unicodedata as uni
import urllib2
import json
from urllib2 import HTTPError
import re

#######  Obtain Internal List of Cars to Pull from Database #######

# This Data Engineering/API Script uses sqlite3 for database pull.

conn = sqlite3.connect('~/database_name.db')
df = pd.read_sql_query('select * from table_name;', conn)

#make a few empty columns in the dataframe

make = []
for row in list(df['make']):
    make.append(str(row))

year = []
for row in list(df['year']):
    year.append(str(row))

model = []
for row in list(df['model']):
    model.append(str(row))

mileage = []
for row in list(df['miles']):
    mileage.append(str(row))

# Not all car models match Edmunds database with internal tables.  Create Dictionary
model_dict = {'GLA':'GLA-Class', 'SLK':'SLK-Class', 'CLA':'CLA-Class', 'G37 Sedan': 'GSedan', \
              'MKT Town Car': 'MKT', 'Ram Pickup 2500': '2500', 'MKZ Hybrid':'MKZ','MAZDA3':'3',\
              'Ram Pickup 1500':'1500','Ram Pickup 3500': '3500','Expedition EL':'Expedition',\
              'Promaster Cargo':'PromasterCargoVan','Corvette':'CorvetteStingray',\
              'Wrangler Unlimited':'Wrangler', 'Express Passenger':'Express','ProMaster Cargo':'PromasterCargoVan'\
             }

#setup api defitions with given assumptions of condition and zip_code
edmunds_api_key = '#############'
condition = 'Clean'
zip_code = '75052'

def edmunds_styleID(make, model, year):
    url = 'https://api.edmunds.com/api/vehicle/v2/' + make + '/' + model + '/' + year + '/'+ \
    '?fmt=json&api_key=' + edmunds_api_key
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    for item in data['styles']:
        return item['id']


def edmunds_TMV(styleID, mileage):
    url = 'https://api.edmunds.com/v1/api/tmv/tmvservice/calculateusedtmv?styleid='\
    +styleID+'&condition='+ condition +'&mileage='+mileage+'&zip='+zip_code+'&fmt=json&api_key='+edmunds_api_key
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    return data.get('tmv').get('nationalBasePrice').get('usedTmvRetail')

# Now let's run through our internal car list to pull styleID and, ultimately, usedRetail price from Edmunds API.
# After some trial and error, I added a few exceptions to catch as many different model descriptions as possible.
# The exceptions still didn't match everything and a dictionary was created.

styleID = []

for x, y, z in zip(make, model, year):
    try: styleID.append(str(edmunds_styleID(x,y,z)))
    except HTTPError:
        y2 = re.sub(r"\s+", "", y)
        try: styleID.append(str(edmunds_styleID(x,y2,z)))
        except HTTPError:
            y_replace = str(model_dict.get(y))
            try: styleID.append(str(edmunds_styleID(x,y_replace,z)))
            except HTTPError:
                styleID.append("NA")

usedTmvRetail = []

for x, y in zip(styleID, mileage):
    try: usedTmvRetail.append(str(edmunds_TMV(x,y)))
    except HTTPError:
        usedTmvRetail.append("None")

# Data obtained!!!!  A couple more dataframe manipulations....
usedTMVRetail = ['' if x is None else x for x in usedTmvRetail]
df_results = pd.DataFrame({'styleID':styleID,'usedTMVRetail':usedTMVRetail})
df_results = df_results.replace(['None'], '') # Replace the 'None' values with blanks for easier computations
df_total = pd.concat([df, df_results], axis = 1

# write to database
df_total.to_sql(name='vroom_total', flavor = 'sqlite',con=conn)

