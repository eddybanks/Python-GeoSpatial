import numpy as np
import pandas as pd
import glob
from pandas import DataFrame, read_csv
from numpy import nan

files = {
    'undergrads': '/Users/edwinagbenyega/Documents/Datamart/data/geocoded/undergrads.csv',
    'grads': '/Users/edwinagbenyega/Documents/Datamart/data/geocoded/grads.csv',
    'chunks': './chunks/'
}

def break_up_files(file, name):
    for k,v in enumerate(read_csv(file, chunksize=2500)):
        v['Main_Street_Line1'] = v['PE_STREET_LINE1'].map(str)
        v['Main_Street_Line2'] = v['PE_STREET_LINE2'].map(str)
        v['Main_Street_Line3'] = v['PE_STREET_LINE3'].map(str)
        v['Main_City'] = v['PE_CITY']
        v['Main_State'] = v['PE_STATE_PROVINCE']
        v['Main_Postal_Code'] = v['PE_POSTAL_CODE']
        v['Main_County'] = v['PE_COUNTY_CODE_DESC']
        v.to_csv(name.format(k))

    for file in glob.glob('./chunks/*.csv'):
        v = read_csv(file)
        v['Main_Street_Line1'].fillna(v['MA_STREET_LINE1'].map(str), inplace=True)
        v['Main_Street_Line2'].fillna(v['MA_STREET_LINE2'].map(str), inplace=True)
        v['Main_Street_Line3'].fillna(v['MA_STREET_LINE3'].map(str), inplace=True)
        v['Main_City'].fillna(v['MA_CITY'], inplace=True)
        v['Main_State'].fillna(v['MA_STATE_PROVINCE'], inplace=True)
        v['Main_Postal_Code'].fillna(v['MA_POSTAL_CODE'], inplace=True)
        v['Main_County'].fillna(v['MA_COUNTY_CODE_DESC'], inplace=True)
        v['Main_Street'] = v[['Main_Street_Line1', 'Main_Street_Line2', 'Main_Street_Line3']].apply(lambda x: ' '.join(x), axis=1)
        v.to_csv(file)



break_up_files(files['undergrads'], './chunks/ug_chunks{}.csv')
break_up_files(files['grads'], './chunks/gr_chunks{}.csv')
