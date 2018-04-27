
import pandas as pd
import datetime
print(datetime.datetime.now())

# df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/sample_set_10000.csv',dtype ='str')
df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/DE1_0_2008_to_2010_Inpatient_Claims_Sample_3.csv',dtype ='str')

#selecting only columns we are interested in
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

#parsing the date field CLM_ADMSN_DT
joined_df['CLM_ADMSN_DT']=pd.to_datetime(joined_df['CLM_ADMSN_DT'], format="%Y%m%d")

#Extracting week only from CLM_ADMSN_DT and creating new column CLM_ADMSN_WEEK from it
joined_df['CLM_ADMSN_WEEK'] = pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).week

df_symp_week = joined_df[['ADMTNG_ICD9_DGNS_CD', 'CLM_ADMSN_WEEK','ICD9_DGNS_CD_1']].copy()

df_symp_week['ADMTNG_ICD9_DGNS_CD'] =  'S_' + df_symp_week['ADMTNG_ICD9_DGNS_CD'].map(str)
df_symp_week['CLM_ADMSN_WEEK'] =  'W_' + df_symp_week['CLM_ADMSN_WEEK'].map(str)
df_symp_week['ICD9_DGNS_CD_1'] =  'D_' + df_symp_week['ICD9_DGNS_CD_1'].map(str)


df_symp_week.to_csv('out_sample.csv', sep=',')
#Group by ICD9_DGNS_CD_1 and creating a new table from it
df_disease_group = df_symp_week.groupby(['ICD9_DGNS_CD_1']).size().reset_index(name='Prob_Dis')

#joining with grouped disease count
joined_df = pd.merge(df_symp_week, df_disease_group, left_on='ICD9_DGNS_CD_1', right_on='ICD9_DGNS_CD_1')

reccount = len(joined_df)

#Calculating P(Disease)
joined_df['Prob_Dis'] = (joined_df.Prob_Dis.astype(int)/reccount)

print(joined_df.head())
print(len(joined_df))

#Creating table grouping Symptom and Disease
df_disease_symptom_group = df_symp_week.groupby(['ICD9_DGNS_CD_1', 'ADMTNG_ICD9_DGNS_CD']).size().reset_index(name='Prob_Sym_Dis')

#joining with grouped disease_symptom count on condition equating ICD9_DGNS_CD_1 and ADMTNG_ICD9_DGNS_CD
joined_df = pd.merge(joined_df, df_disease_symptom_group, how = 'left', left_on=['ICD9_DGNS_CD_1', 'ADMTNG_ICD9_DGNS_CD'], right_on=['ICD9_DGNS_CD_1', 'ADMTNG_ICD9_DGNS_CD'])
joined_df['Prob_Sym_Dis'] = (joined_df.Prob_Sym_Dis.astype(int)/reccount)


#Creating table grouping Week and Disease
df_disease_week_group = df_symp_week.groupby(['ICD9_DGNS_CD_1', 'CLM_ADMSN_WEEK']).size().reset_index(name='Prob_Week_Dis')

#joining with grouped disease_symptom count on condition equating ICD9_DGNS_CD_1 and CLM_ADMSN_WEEK
joined_df = pd.merge(joined_df, df_disease_week_group, how = 'left', left_on=['ICD9_DGNS_CD_1', 'CLM_ADMSN_WEEK'], right_on=['ICD9_DGNS_CD_1', 'CLM_ADMSN_WEEK'])
joined_df['Prob_Week_Dis'] = (joined_df.Prob_Week_Dis.astype(int)/reccount)

#Calculating P(S|D) [See if Prob_Sym|Dis can have more decimal points]
joined_df['Prob_Sym_given_Dis'] = (joined_df.Prob_Sym_Dis.astype('double')/joined_df.Prob_Dis.astype('double')).astype('double')

#Calculating P(W|D) [See if Prob_Week|Dis can have more decimal points]
joined_df['Prob_Week_given_Dis'] = (joined_df.Prob_Week_Dis.astype('double')/joined_df.Prob_Dis.astype('double')).astype('double')

#Probability of  D^C
joined_df['Prob_D_comp'] = (1 - joined_df.Prob_Dis.astype('double'))

#Calculating P(S and W)
joined_df['Prob_Sym_Week'] = (joined_df.Prob_Sym_given_Dis.astype('double') *
                                                      joined_df.Prob_Week_given_Dis.astype('double') *
                                                      joined_df.Prob_Dis.astype('double') ) + \
                                                     ((1- joined_df.Prob_Sym_given_Dis.astype('double') )*
                                                      (1-joined_df.Prob_Week_given_Dis.astype('double') )*
                                                      (1- joined_df.Prob_Dis.astype('double')) )

#Calculating P(S and W | Disease)
joined_df['Prob_Sym_Week_given_disease'] = (joined_df.Prob_Sym_given_Dis.astype('double') *
                                                                                joined_df.Prob_Week_given_Dis.astype('double') )
#Finally calculating P(D|S and W)
joined_df['Prob_Sym_Week_given_disease'] = (joined_df.Prob_Sym_Week_given_disease.astype('double') * joined_df.Prob_Dis.astype('double')) /(joined_df.Prob_Sym_Week.astype('double') )

joined_df.to_csv('cond_prob.csv', sep=',')

print(joined_df.head())