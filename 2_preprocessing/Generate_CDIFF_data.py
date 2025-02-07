import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from math import pi
import sys
import os
import scipy as sc
import warnings

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
warnings.filterwarnings('ignore')

mydir = os.path.expanduser("~/GitHub/HAIs/")

#########################################################################################
########################## IMPORT PSI DATA ##############################################

main_df = pd.read_pickle(mydir + "1_data/Facility.pkl")
main_df.drop(['Address', 'City', 'County Name', 'Phone Number', 'ZIP Code'], 
             axis = 1, inplace=True)
main_df['file_date'] = main_df['file_date'].str[-8:]

print(list(main_df), '\n')
#print(main_df.head())
#print(list(set(main_df['Measure Name'])))

main_df = main_df[main_df['Measure Name'].isin([
    'Clostridium Difficile (C.Diff): Observed Cases', 
    'Clostridium Difficile (C.Diff)', 
    'C.diff Observed Cases', 
    'Clostridium Difficile (C.Diff): Patient Days', 
    'Clostridium difficile (C.diff.) Laboratory-identified Events (Intestinal infections)', 
    'Clostridium difficile (C.diff.) intestinal infections', 
    'C.diff Upper Confidence Limit', 
    'Clostridium Difficile (C.Diff): Lower Confidence Limit', 
    'C.diff Predicted Cases', 
    'Clostridium Difficile (C.Diff): Upper Confidence Limit', 
    'Clostridium Difficile (C.Diff): Predicted Cases', 
    'C.diff Lower Confidence Limit', 
    'C.diff Patient Days',
    
    ])]


main_df['Facility and File Date'] = main_df['Facility ID'] + '-' + main_df['file_date']
print(main_df['Facility and File Date'].iloc[0])

cdiff_df = main_df[main_df['Measure Name'].isin([
    'Clostridium Difficile (C.Diff): Observed Cases', 
    'C.diff Observed Cases',
    
    'Clostridium Difficile (C.Diff)', 
    'Clostridium difficile (C.diff.) Laboratory-identified Events (Intestinal infections)', 
    'Clostridium difficile (C.diff.) intestinal infections', 
     
    'Clostridium Difficile (C.Diff): Patient Days', 
    'C.diff Patient Days',
    
    'C.diff Upper Confidence Limit', 
    'Clostridium Difficile (C.Diff): Upper Confidence Limit', 
    
    'Clostridium Difficile (C.Diff): Lower Confidence Limit', 
    'C.diff Lower Confidence Limit', 
    
    'C.diff Predicted Cases', 
    'Clostridium Difficile (C.Diff): Predicted Cases', 
    
    ])]


d = {
     'Clostridium Difficile (C.Diff): Observed Cases': 'CDIFF Observed Cases',
     'C.diff Observed Cases': 'CDIFF Observed Cases',
    
     'Clostridium Difficile (C.Diff)': 'CDIFF',
     'Clostridium difficile (C.diff.) Laboratory-identified Events (Intestinal infections)': 'CDIFF',
     'Clostridium difficile (C.diff.) intestinal infections': 'CDIFF',
     
     'Clostridium Difficile (C.Diff): Patient Days': 'CDIFF patient days',
     'C.diff Patient Days': 'CDIFF patient days',
    
     'C.diff Upper Confidence Limit': 'CDIFF upper CL',
     'Clostridium Difficile (C.Diff): Upper Confidence Limit': 'CDIFF upper CL',
    
     'Clostridium Difficile (C.Diff): Lower Confidence Limit': 'CDIFF lower CL',
     'C.diff Lower Confidence Limit': 'CDIFF lower CL',
    
     'C.diff Predicted Cases': 'CDIFF Predicted Cases',
     'Clostridium Difficile (C.Diff): Predicted Cases': 'CDIFF Predicted Cases',

     }

cdiff_df['Measure Name'].replace(to_replace=d, inplace=True)

print(list(set(cdiff_df['Measure Name'].tolist())))

df = pd.DataFrame(columns=['Facility and File Date'])
IDs = list(set(cdiff_df['Facility and File Date'].tolist()))

dates = []
IDs2 = []
IDs3 = []
measures = ['CDIFF', 'CDIFF upper CL', 'CDIFF Predicted Cases', 'CDIFF patient days', 
            'CDIFF lower CL', 'CDIFF Observed Cases']

measure_lists = [ [] for _ in range(len(measures)) ]

for i, ID in enumerate(IDs):
    print(len(IDs) - i)
    
    tdf = cdiff_df[cdiff_df['Facility and File Date'] == ID]
    
    dates.append(tdf['file_date'].iloc[0])
    IDs2.append(ID)
    IDs3.append(tdf['Facility ID'].iloc[0])
    
    for j, measure in enumerate(measures):
        tdf2 = 0
        try:
            tdf2 = tdf[tdf['Measure Name'] == measure]
            val = tdf2['Score'].iloc[0]
        except:
            val = np.nan
            
        measure_lists[j].append(val)
        
df['Facility and File Date'] = IDs2
df['Facility ID'] = IDs3

for i, measure in enumerate(measures):
    df[measure] = measure_lists[i]
df['file date'] = dates

print(list(df), '\n')

df['file date'] = pd.to_datetime(df['file date'], format="%Y%m%d")

df.to_pickle(mydir + "1_data/CDIFF_Data.pkl")
df.to_csv(mydir + "1_data/CDIFF_Data.csv")
