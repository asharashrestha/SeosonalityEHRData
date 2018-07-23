
import pandas as pd
import datetime

df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/20 Sample Data /DE1_0_2008_to_2010_Inpatient_Claims_Sample_3.csv',dtype ='str')

#selecting only columns we are interested in
df_selected_cols = df[['ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()
ccs= pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 1/icd_ccs_No_Dups.csv',dtype ='str')#ccs data import
ccs.drop('OPTIONAL_CCS_CATEGORY', inplace = True, axis =1)
ccs.drop('OPTIONAL_CCS_CATEGORY_DESCRIPTION', inplace = True, axis =1)
ccs.drop('ICD_9_CM_CODE_DESCRIPTION', inplace = True, axis =1)

print(len(df_selected_cols))

# #Joining With ADMTNG_ICD9_DGNS_CD
# joined_df = pd.merge(df_selected_cols, ccs, left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code', how = 'left')
# print(len(joined_df))
#
#
# #dropping unwanted columns:
# columns = ['CCS_CATEGORY', 'ICD9_Code', 'ADMTNG_ICD9_DGNS_CD']
# joined_df.drop(columns, inplace=True, axis=1)
# joined_df = joined_df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'ADMTNG_ICD9_DGNS_CD'})
# print(len(joined_df))
 #Joining With ICD9_DGNS_CD_1
joined_df = pd.merge(df_selected_cols, ccs, left_on='ICD9_DGNS_CD_1', right_on='ICD9_Code', how = 'left')


#dropping unwanted columns:
columns = ['CCS_CATEGORY', 'ICD9_Code', 'ICD9_DGNS_CD_1']
joined_df.drop(columns, inplace=True, axis=1)
joined_df = joined_df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'ICD9_DGNS_CD_1'})
print(len(joined_df))
joined_df = joined_df.groupby([ 'ICD9_DGNS_CD_1']).size().reset_index(name='counts')

joined_df.to_csv('freq_3.csv', sep=',')