#Finding disease with highest number of patients

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from sklearn.naive_bayes import MultinomialNB


print(datetime.datetime.now())

df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',dtype ='str')
df_selected_cols = df[['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()
ccn = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/icd_ccs.csv',dtype ='str')#ccn data import

# df_selected_cols  = df_selected_cols.head()

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

# joined_df['CLM_ADMSN_MNTH'] = pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).month#Extracting month only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_MNTH) from it
# joined_df['CLM_ADMSN_MNTH']  = joined_df['CLM_ADMSN_MNTH'] .astype(str).str.rjust(2,'0')#padding 0 in the front if only single digit month comes

# joined_df['CLM_ADMSN_YEAR'] = 0
	#pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).year#Extracting year only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_YEAR) from it
# joined_df['CLM_ADMSN_YEAR']  = joined_df['CLM_ADMSN_YEAR'] .astype(str).str.rjust(2,'0')#padding 0 in the front if only single digit day comes
#
# joined_df["CLM_MONTH_DATE"] = joined_df["CLM_ADMSN_YEAR"].map(str) + joined_df["CLM_ADMSN_MNTH"].map(str)

#Removing CLM_ADMSN_DT
joined_df.drop(['CLM_ADMSN_DT'], inplace=True, axis=1)


#Renaming Newly genrated YYYYMM as CLM_ADMSN_DT
# joined_df = joined_df.rename(columns={'CLM_MONTH_DATE': 'CLM_ADMSN_DT'})

#Column Names in this dataframe are: 	DESYNPUF_ID	ADMTNG_ICD9_DGNS_CD	ICD9_DGNS_CD_1	CLM_ADMSN_MNTH	CLM_ADMSN_YEAR	CLM_ADMSN_DT

# #calculate the number of patients for each disease to find out the disease with most number of patient admission
# final_df = joined_df.groupby('ADMTNG_ICD9_DGNS_CD', as_index=False)[['DESYNPUF_ID']].count()
# # final_df = final_df.rename(columns={'DESYNPUF_ID': 'Number_of_Patients'})
#
#
# #calculate the number of patients for all diseases in all months
# final_df = joined_df.groupby('CLM_ADMSN_WEEK', as_index=False)[['DESYNPUF_ID']].count()

# # final_df = final_df.rename(columns={'DESYNPUF_ID': 'Number_of_Patients_total'})
#
#
#
# # TOP 2 diseases found are Oth low resp(olr) and Chest Pain(cp). taking these two for example
# df_olr = joined_df.loc[joined_df['ADMTNG_ICD9_DGNS_CD'] == '133']#133 for olr
# df_cp = joined_df.loc[joined_df['ADMTNG_ICD9_DGNS_CD'] == '102']#102 for cp
#
# df_olr = df_olr[['DESYNPUF_ID','CLM_ADMSN_DT']].copy()
# df_olr = df_olr.groupby('CLM_ADMSN_DT', as_index=False)[['DESYNPUF_ID']].count()
#
#
#
# #joining olr and main df
# df_olr_admissionrate = pd.merge(df_olr, final_df, left_on='CLM_ADMSN_DT', right_on='CLM_ADMSN_DT')
#
#
# #dataframe after calculating admission rates:
# df_olr_admissionrate['Admission_Rate'] = (df_olr_admissionrate.DESYNPUF_ID_x.astype(int)/df_olr_admissionrate.DESYNPUF_ID_y.astype(int))*1000
#
#
# #drop DESYNPUF_ID from dataframe:
# columns = ['DESYNPUF_ID_x','DESYNPUF_ID_y']
# df_olr_admissionrate.drop(columns, inplace=True, axis=1)
#
#
# df_olr_admissionrate.plot(x="CLM_ADMSN_DT", y=["Admission_Rate"], kind="line", color = 'c')
# # joined_df.to_csv('out_final_df.csv', sep=',')
#
#
# df_apriori = joined_df[['ADMTNG_ICD9_DGNS_CD','ICD9_DGNS_CD_1','CLM_ADMSN_DT']].copy()
# df_apriori.to_csv('out.csv', sep=',')
#

#selecting only admission diag codes and week:
df_symp_week = joined_df[['ADMTNG_ICD9_DGNS_CD', 'CLM_ADMSN_WEEK']].copy()

df_disease = joined_df[['ICD9_DGNS_CD_1']].copy()
records_sym_date = []
records_dis = []

for i in range(0,46565765):#number of rows
	records_sym_date.append([int(df_symp_week.values[i, j]) for j in range(0, 2)]) #Number of columns

records_sym_date = np.array([np.array(xi) for xi in records_sym_date])

# print(type(records_sym_date))


for i in range(0, 87878979):#number of rows
	records_dis.append([int(df_disease.values[i, j]) for j in range(0, 1)]) #Number of columns

records_dis = np.asarray(records_dis)
records_sym_date = np.asarray(records_sym_date)


# print("here are records")
print (records_sym_date)
print(records_dis)

# for i in range(len(records_sym_date)):
# 	records_sym_date[i] = int(records_sym_date[i])

clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf.fit(records_sym_date, records_dis.ravel())#Converting column vector to row vector

print(records_sym_date[2:3])
print("The result is: ", clf.predict([]))

#
#
# print (records)
#
# from apyori import apriori
# rules = apriori(records, min_support = 0.01, min_confidence = 0.2, min_lift = 3, min_length = 2)
#
#
#
# results = list(rules)
# print(results)
#
#
# plt.show()
#
# # apriori.py -f DATASET.csv -s minSupport  -c minConfidence
#

print(datetime.datetime.now())
