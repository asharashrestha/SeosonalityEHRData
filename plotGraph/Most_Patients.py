#Finding disease with highest number of patients

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from sklearn.naive_bayes import MultinomialNB



print(datetime.datetime.now())

# df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',dtype ='str')
df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/sample_set_10000.csv',dtype ='str')


#for test data
# df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Test_Data/DE1_0_2008_to_2010_Inpatient_Claims_Sample_7.csv',dtype ='str')

df_selected_cols = df[['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()
ccn = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 1/icd_ccs.csv',dtype ='str')#ccn data import

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
# joined_df.drop(['CLM_ADMSN_DT'], inplace=True, axis=1)


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
# df_symp_week.to_csv('out_joined.csv', sep=',')
#selecting only admission diag codes and week:
df_symp_week = joined_df[['ADMTNG_ICD9_DGNS_CD', 'CLM_ADMSN_WEEK','ICD9_DGNS_CD_1']].copy()

df_symp_week['ADMTNG_ICD9_DGNS_CD'] =  'S_' + df_symp_week['ADMTNG_ICD9_DGNS_CD'].map(str)
df_symp_week['CLM_ADMSN_WEEK'] =  'W_' + df_symp_week['CLM_ADMSN_WEEK'].map(str)
df_symp_week['ICD9_DGNS_CD_1'] =  'D_' + df_symp_week['ICD9_DGNS_CD_1'].map(str)


# df_disease = joined_df[['ICD9_DGNS_CD_1']].copy()
df_symp_week.to_csv('out_train.csv', sep=',')

# df_symp_week = df_symp_week.head()
#
#
# df_symp_week['key_sym_week'] = list(zip(df_symp_week.ADMTNG_ICD9_DGNS_CD, df_symp_week.CLM_ADMSN_WEEK))#Converting list of columns to tuple to form new column
#
# df_symp_week['value_dis_null'] = list(zip(df_symp_week.ICD9_DGNS_CD_1))#Converting list of columns to tuple to form new column
#
# df_symp_week.drop(['ADMTNG_ICD9_DGNS_CD','CLM_ADMSN_WEEK','ICD9_DGNS_CD_1'], inplace=True, axis=1)
# print(df_symp_week)
# mydict = dict(zip(df_symp_week.ADMTNG_ICD9_DGNS_CD, df_symp_week.CLM_ADMSN_WEEK))
# testdata = [{('W_10', 'S_157'): ('D_2',)}, {('W_10', 'S_157'): ('D_12',)}, {('W_10', 'S_156'): ('D_14',)}]

# df_symp_week['new_dict'] = {df_symp_week['new_col']:df_symp_week['ICD9_DGNS_CD_1']}

# mydict = {}#Converting to dictionary conserving duplicates
# for x in range(len(df_symp_week)):
#     currentid = df_symp_week.iloc[x,3]
#     currentvalue = df_symp_week.iloc[x,2]
#     mydict.setdefault(currentid, [])
#     mydict[currentid].append(currentvalue)
#
# print(mydict)
#
# # df_symp_probs = df_symp_week.groupby('ADMTNG_ICD9_DGNS_CD', as_index=False)[['DESYNPUF_ID']].count()
#
# df_symp_probs = df_symp_week.groupby('ADMTNG_ICD9_DGNS_CD', as_index=False).size().div(len(df_symp_week))
#
# df_week_probs = df_symp_week.groupby('CLM_ADMSN_WEEK').size().div(len(df_symp_week))
# # df_dis_probs = df_symp_week.groupby('ICD9_DGNS_CD_1').size().div(len(df_symp_week))
#
# print(df_symp_probs)
#
# df_symp_probs = df_symp_probs.to_frame()
#
# # df_symp_probs.astype('int32')
# # df_symp_week.astype('int32')
# df_week_probs = df_week_probs.to_frame()
# # df_dis_probs = df_dis_probs.to_frame()
#
# df_symp_week = pd.merge(df_symp_week, df_symp_week, left_on='ADMTNG_ICD9_DGNS_CD', right_on='ADMTNG_ICD9_DGNS_CD')
# print(df_symp_week)
#
# print(type(df_symp_probs))
# # print(df_symp_week)
# # #
# # #
# # #
# # # df_symp_probs = df_symp_week.groupby(['ADMTNG_ICD9_DGNS_CD','CLM_ADMSN_WEEK']).size().div(len(df_symp_week))
# # #
# # # print(df_symp_probs)
# # #
# # # df_dis_given_symp_probs = df_symp_week.groupby(['ICD9_DGNS_CD_1', 'ADMTNG_ICD9_DGNS_CD']).size().div(len(df_symp_week)).div(df_symp_probs, axis=0, level='ADMTNG_ICD9_DGNS_CD')
# #
# # print("-----------")
# # print(df_dis_given_symp_probs)
# #
# # records_sym_date = []
# # records_dis = []
# #
# # #71612
# # for i in range(0,5):#number of rows
# # 	records_sym_date.append([str(df_symp_week.values[i, j]) for j in range(0, 2)]) #Number of columns
# #
# # records_sym_date = np.array([np.array(xi) for xi in records_sym_date])
# # #
# # # print((records_sym_date))
# #
# #
# # for i in range(0, 5):#number of rows
# # 	records_dis.append([str(df_disease.values[i, j]) for j in range(0, 1)]) #Number of columns
# #
# # # print("-------")
# # # print((records_dis))
# # # print(df_symp_week)
# #
# #
# # # records_dis = np.asarray(records_dis)
# # # records_sym_date = np.asarray(records_sym_date)
# #
# # #
# # # clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
# # # clf.fit(records_sym_date, records_dis.ravel())#Converting column vector to row vector
# # # #
# # # print(records_sym_date[4:3])
# # # print("The result is: ", clf.predict(records_sym_date[4:3]))
# #
# # #
# # # from apyori import apriori
# # # rules = apriori(records, min_support = 0.01, min_confidence = 0.2, min_lift = 3, min_length = 2)
# # #
# # #
# # #
# # # results = list(rules)
# # # print(results)
# # #
# # #
# # # plt.show()
# # #
# # # # apriori.py -f DATASET.csv -s minSupport  -c minConfidence
# # #
