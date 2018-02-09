#Finding disease with highest number of patients

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',dtype ='str')
new_df = df[['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()

ccn = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/icd_ccs.csv',dtype ='str')


new_df= pd.merge(new_df, ccn[['ICD9_Code', 'CCS_CATEGORY_DESCRIPTION']], left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code', how='left')


new_df['CLM_ADMSN_DT']=pd.to_datetime(new_df['CLM_ADMSN_DT'], format="%Y%m%d") #parsing the date field CLM_ADMSN_DT.


new_df['CLM_ADMSN_MNTH'] = pd.DatetimeIndex(new_df['CLM_ADMSN_DT']).month#Extracting month only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_MNTH) from it
new_df['CLM_ADMSN_MNTH']  = new_df['CLM_ADMSN_MNTH'] .astype(str).str.rjust(2,'0')#padding 0 in the front if only single digit month comes

new_df['CLM_ADMSN_YEAR'] = pd.DatetimeIndex(new_df['CLM_ADMSN_DT']).year#Extracting year only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_YEAR) from it
# new_df['CLM_ADMSN_YEAR']  = new_df['CLM_ADMSN_YEAR'] .astype(str).str.rjust(2,'0')#padding 0 in the front if only single digit day comes

new_df["CLM_MONTH_DATE"] = new_df["CLM_ADMSN_YEAR"].map(str) + new_df["CLM_ADMSN_MNTH"].map(str)

print(new_df.head())

# final_df = new_df.groupby('CLM_MONTH_DATE', as_index=False)[['DESYNPUF_ID']].count()
#
# final_df = final_df.rename(columns={'DESYNPUF_ID': 'No. of Patients'})

# final_df.plot(x="CLM_MONTH_DATE", y=["No. of Patients"], kind="line", color = 'c')

count_df = new_df.groupby('CCS_CATEGORY_DESCRIPTION', as_index=False)[['DESYNPUF_ID']].count()
# count_df = new_df.rename(columns={'DESYNPUF_ID': 'No. of Patients'})
#
print(count_df.head())
# count_df.plot(x="ADMTNG_ICD9_DGNS_CD", y=["No. of Patients"], kind="line", color = 'c')
test = count_df.sort_values(['DESYNPUF_ID'], ascending=[False]) #sort descending
# test = count_df.sort_values('DESYNPUF_ID', ascending=False)
print(test.head())

#Oth low resp comes in number one with record of 4154. CHEST PAIN COMES IN NUMBER 2 with record of 3492 pneumonia in 3rd with 2494

# print("TOP 10 Only")
#
# plt.show()

