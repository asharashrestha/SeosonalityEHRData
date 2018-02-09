#Finding disease with highest number of patients

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',dtype ='str')
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

joined_df['CLM_ADMSN_MNTH'] = pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).month#Extracting month only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_MNTH) from it
joined_df['CLM_ADMSN_MNTH']  = joined_df['CLM_ADMSN_MNTH'] .astype(str).str.rjust(2,'0')#padding 0 in the front if only single digit month comes

joined_df['CLM_ADMSN_YEAR'] = pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).year#Extracting year only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_YEAR) from it
# joined_df['CLM_ADMSN_YEAR']  = joined_df['CLM_ADMSN_YEAR'] .astype(str).str.rjust(2,'0')#padding 0 in the front if only single digit day comes
#
joined_df["CLM_MONTH_DATE"] = joined_df["CLM_ADMSN_YEAR"].map(str) + joined_df["CLM_ADMSN_MNTH"].map(str)

#Removing CLM_ADMSN_DT
joined_df.drop(['CLM_ADMSN_DT'], inplace=True, axis=1)

#Renaming Newly genrated YYYYMM as CLM_ADMSN_DT
joined_df = joined_df.rename(columns={'CLM_MONTH_DATE': 'CLM_ADMSN_DT'})
#Column Names in this dataframe are: 	DESYNPUF_ID	ADMTNG_ICD9_DGNS_CD	ICD9_DGNS_CD_1	CLM_ADMSN_MNTH	CLM_ADMSN_YEAR	CLM_ADMSN_DT

#calculate the number of patients for each disease to find out the disease with most number of patient admission
final_df = joined_df.groupby('ADMTNG_ICD9_DGNS_CD', as_index=False)[['DESYNPUF_ID']].count()
# final_df = final_df.rename(columns={'DESYNPUF_ID': 'Number_of_Patients'})


#calculate the number of patients for all diseases in all months
final_df = joined_df.groupby('CLM_ADMSN_DT', as_index=False)[['DESYNPUF_ID']].count()

final_df.to_csv('out_final_df.csv', sep=',')
# final_df = final_df.rename(columns={'DESYNPUF_ID': 'Number_of_Patients_total'})



# TOP 2 diseases found are Oth low resp(olr) and Chest Pain(cp). taking these two for example
df_olr = joined_df.loc[joined_df['ADMTNG_ICD9_DGNS_CD'] == '133']#133 for olr
df_cp = joined_df.loc[joined_df['ADMTNG_ICD9_DGNS_CD'] == '102']#102 for cp

df_olr = df_olr[['DESYNPUF_ID','CLM_ADMSN_DT']].copy()
df_olr = df_olr.groupby('CLM_ADMSN_DT', as_index=False)[['DESYNPUF_ID']].count()



#joining olr and main df
df_olr_admissionrate = pd.merge(df_olr, final_df, left_on='CLM_ADMSN_DT', right_on='CLM_ADMSN_DT')


#dataframe after calculating admission rates:
df_olr_admissionrate['Admission_Rate'] = (df_olr_admissionrate.DESYNPUF_ID_x.astype(int)/df_olr_admissionrate.DESYNPUF_ID_y.astype(int))*1000


#drop DESYNPUF_ID from dataframe:
columns = ['DESYNPUF_ID_x','DESYNPUF_ID_y']
df_olr_admissionrate.drop(columns, inplace=True, axis=1)

df_olr_admissionrate.to_csv('out.csv', sep=',')

df_olr_admissionrate.plot(x="CLM_ADMSN_DT", y=["Admission_Rate"], kind="line", color = 'c')
plt.show()

