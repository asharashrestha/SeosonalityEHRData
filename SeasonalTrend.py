import pandas as pd
import pandas.tseries as ser
import glob, os
import numpy as np

filepath = '/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2'
file1 = 'DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv'
file2 = 'DE1_0_2008_to_2010_Inpatient_Claims_Sample_2.csv'
file3 = 'DE1_0_2008_to_2010_Inpatient_Claims_Sample_3.csv'

files = [file1, file2, file3]
df = pd.DataFrame(columns=['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1', 'sourcefilename'])


for file in files:
    df_temp = pd.read_csv(filepath + '/' + file, dtype='str')
    print(file + '==> ' + str(len(df_temp)))

    df_temp = df_temp[['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()

    df_temp['sourcefilename'] = file

    df.append(df_temp, ignore_index = True)
    df = pd.concat([df, df_temp])


df['CLM_ADMSN_DT'] = np.where(df.sourcefilename == file1, 0, df.my_channel)

# new_df = df['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1'].copy()

