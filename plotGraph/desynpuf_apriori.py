import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

ccn = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/icd_ccs.csv',dtype ='str')

# print(ccn.head())


df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',dtype ='str')
new_df = df[['ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()
new_df_1 = new_df.fillna(0)

# print(new_df_1.head())




new_df_2= pd.merge(new_df_1, ccn[['ICD9_Code', 'CCS_CATEGORY_DESCRIPTION']], left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code', how='left')
new_df_3= pd.merge(new_df_2, ccn[['ICD9_Code', 'CCS_CATEGORY_DESCRIPTION']], left_on='ICD9_DGNS_CD_1', right_on='ICD9_Code', how='left')

# print(new_df_3.head())


final_df = new_df_3[['CCS_CATEGORY_DESCRIPTION_x', 'CCS_CATEGORY_DESCRIPTION_y']].copy()

print(final_df.head())
print(len(final_df.index))
records = []

for i in range(0, 72523):#number of rows
	records.append([str(final_df.values[i, j]) for j in range(0, 2)]) #Number of columns

from apyori import apriori
rules = apriori(records, min_support = 0.01, min_confidence = 0.2, min_lift = 3, min_length = 2)

results = list(rules)
print(results)


