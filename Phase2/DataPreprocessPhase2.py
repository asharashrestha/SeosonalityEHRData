import pandas as pd
import datetime as dt
import numpy as np
#importing the beneficiaries file
df_ben = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv',dtype ='str')
ccs= pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 1/icd_ccs_No_Dups.csv',dtype ='str')#ccs data import
#removing unnecessary columns from ccs
remove_cols = ['OPTIONAL_CCS_CATEGORY_DESCRIPTION','OPTIONAL_CCS_CATEGORY','ICD_9_CM_CODE_DESCRIPTION']

ccs.drop(remove_cols, inplace = True, axis =1)

#importing claims file
df_clm = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/20 Sample Data /DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',dtype ='str')

df = pd.merge(df_clm, df_ben, left_on='DESYNPUF_ID', right_on='DESYNPUF_ID', how = 'left')

df = df[[ 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1', 'BENE_BIRTH_DT','BENE_DEATH_DT','BENE_SEX_IDENT_CD']].copy()
#check if Date of Birth is NULL
df_dob = df.query('BENE_BIRTH_DT != BENE_BIRTH_DT')
# print(df_dob.head())
#check if gender is NULL
df_deathdf_sex = df.query('BENE_SEX_IDENT_CD != BENE_SEX_IDENT_CD')
# print(df_sex.head())

#check if date of death is NULL
df_death = df.query('BENE_DEATH_DT != BENE_DEATH_DT')

#Converting Admission Date to DateTime
df['CLM_ADMSN_DT']  = pd.DatetimeIndex(df['CLM_ADMSN_DT']).month.map(str)

#calculating Age
now = pd.Timestamp(dt.datetime.now())
df['now'] = pd.to_datetime(now)
df['now'] = pd.to_datetime(df['now'], format= '%Y%m%d')


df['dob'] = pd.to_datetime(df['BENE_BIRTH_DT'], format= '%Y%m%d')
df['dod'] = pd.to_datetime(df['BENE_DEATH_DT'], format= '%Y%m%d')
df['dod'] = df.dod.combine_first(df.now)

df['age'] = pd.to_numeric((df['dod'] - df['dob']).astype('m8[Y]'), downcast='signed')

df = df[[ 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1','BENE_SEX_IDENT_CD','age']].copy()

#Separating Summer and Winter Month (if Dec, Jan, Feb then Winter. if Jun, Jul, Aug then Summer else "Season")
df['Season']  = 'Season'
df['Season'] = np.where(df.CLM_ADMSN_DT=='1', 'Winter',
                           np.where(df.CLM_ADMSN_DT=='2','Winter',
                                    np.where(df.CLM_ADMSN_DT == '12','Winter',
                                             np.where(df.CLM_ADMSN_DT == '6', 'Summer',
                                                      np.where(df.CLM_ADMSN_DT == '7', 'Summer',
                                                               np.where(df.CLM_ADMSN_DT == '8', 'Summer', 'Season'
                                                                        ))))))

# Remove all other data except Summer and Winter

df = df[df['Season'].isin(['Summer','Winter'])]
df.drop('CLM_ADMSN_DT', inplace=True, axis=1)



#joining Admission Diag Code and ICD Code with CCS

df = pd.merge(df, ccs, left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code', how = 'left')
#dropping unwamted columns
columns = ['CCS_CATEGORY', 'ICD9_Code', 'ADMTNG_ICD9_DGNS_CD']
df.drop(columns, inplace=True, axis=1)
df = df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'ADMTNG_ICD9_DGNS_CD'})

df = pd.merge(df, ccs, left_on='ICD9_DGNS_CD_1', right_on='ICD9_Code', how = 'left')
#dropping unwamted columns
columns = ['CCS_CATEGORY', 'ICD9_Code', 'ICD9_DGNS_CD_1']
df.drop(columns, inplace=True, axis=1)
df = df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'ICD9_DGNS_CD_1'})


#Remove all data except for the ICD1 Codes as the 6 classes that we described
df = df[df['ICD9_DGNS_CD_1'].isin(['Pneumonia', 'Asthma', 'Viral infect', 'COPD','Tuberculosis', 'Oth low resp', 'Bronchitis'])]
df = df.dropna(how='any',axis=0)

#selecting only object data types
df = df.select_dtypes(include=['object']).copy()
cleanup_season = {"Season":     {"Summer": 1, "Winter": 2}}
    # ,
    #             "num_cylinders": {"four": 4, "six": 6, "five": 5, "eight": 8,
    #                               "two": 2, "twelve": 12, "three":3 }}
    
df.replace(cleanup_season, inplace=True)
#creating dummy columns for different admission diagnosis codes
df = pd.get_dummies(df, columns=["ADMTNG_ICD9_DGNS_CD"])
print(df.head())
# print(df.dtypes)

# df.to_csv('dob.csv', sep=',')




