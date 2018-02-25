#Finding disease with highest number of patients

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

print(datetime.datetime.now())

#for test data
df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Test_Data/DE1_0_2008_to_2010_Inpatient_Claims_Sample_7.csv',dtype ='str')

df_selected_cols = df[['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()
ccn = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/icd_ccs.csv',dtype ='str')#ccn data import

#Joining With ADMTNG_ICD9_DGNS_CD
joined_df = pd.merge(df_selected_cols, ccn, left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code')

#dropping unwanted columns:
columns = ['ICD9_Code', 'ICD_9_CM_CODE_DESCRIPTION', 'CCS_CATEGORY_DESCRIPTION','OPTIONAL_CCS_CATEGORY', 'OPTIONAL_CCS_CATEGORY_DESCRIPTION', 'ADMTNG_ICD9_DGNS_CD']
joined_df.drop(columns, inplace=True, axis=1)
joined_df = joined_df.rename(columns={'CCS_CATEGORY': 'ADMTNG_ICD9_DGNS_CD'})

 #Joining With ICD9_DGNS_CD_1
joined_df = pd.merge(joined_df, ccn, left_on='ICD9_DGNS_CD_1', right_on='ICD9_Code')

#dropping unwanted columns:
columns = ['ICD9_Code', 'CCS_CATEGORY_DESCRIPTION', 'ICD_9_CM_CODE_DESCRIPTION', 'OPTIONAL_CCS_CATEGORY', 'OPTIONAL_CCS_CATEGORY_DESCRIPTION', 'ICD9_DGNS_CD_1']
joined_df.drop(columns, inplace=True, axis=1)
joined_df = joined_df.rename(columns={'CCS_CATEGORY': 'ICD9_DGNS_CD_1'})


joined_df['CLM_ADMSN_DT']=pd.to_datetime(joined_df['CLM_ADMSN_DT'], format="%Y%m%d") #parsing the date field CLM_ADMSN_DT.

joined_df['CLM_ADMSN_WEEK'] = pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).week #Extracting week only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_WEEK from it

#Removing CLM_ADMSN_DT
joined_df.drop(['CLM_ADMSN_DT'], inplace=True, axis=1)


#selecting only admission diag codes and week:
df_symp_week = joined_df[['ADMTNG_ICD9_DGNS_CD', 'CLM_ADMSN_WEEK','ICD9_DGNS_CD_1']].copy()
df_symp_week['ADMTNG_ICD9_DGNS_CD'] =  'S_' + df_symp_week['ADMTNG_ICD9_DGNS_CD'].map(str)
df_symp_week['CLM_ADMSN_WEEK'] =  'W_' + df_symp_week['CLM_ADMSN_WEEK'].map(str)
df_symp_week['ICD9_DGNS_CD_1'] =  'D_' + df_symp_week['ICD9_DGNS_CD_1'].map(str)


# df_disease = joined_df[['ICD9_DGNS_CD_1']].copy()
df_symp_week.to_csv('out_test.csv', sep=',')


df_symp_week['key_sym_week'] = list(zip(df_symp_week.ADMTNG_ICD9_DGNS_CD, df_symp_week.CLM_ADMSN_WEEK))#Converting list of columns to tuple to form new column

df_symp_week['value_dis_null'] = list(zip(df_symp_week.ICD9_DGNS_CD_1))#Converting list of columns to tuple to form new column

df_symp_week.drop(['ADMTNG_ICD9_DGNS_CD','CLM_ADMSN_WEEK','ICD9_DGNS_CD_1'], inplace=True, axis=1)

test_data = []

for index, row in df_symp_week.iterrows():
    dict = {}
    dict[row['key_sym_week']] = row['value_dis_null']
    test_data.append(dict.copy())

