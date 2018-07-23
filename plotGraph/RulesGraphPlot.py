#Finding disease with highest number of patients

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from sklearn.naive_bayes import MultinomialNB


print(datetime.datetime.now())

df = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/rules_final.csv',dtype ='str')
print(df.head())
#From Rules, Top 3 diseases found are: 203-203, 122-122, 109-109, 108-108, 254-254
#133-108 is such pair where lhs <> rhs

# # TOP 2 diseases found are Oth low resp(olr) and Chest Pain(cp). taking these two for example
df_203 = df.loc[df['symptom'] == '203']#133 for olr
df_203 = df_203.loc[df_203['disease'] == '203']#133 for olr
df_203 = df_203[['week','conf']].copy()

df_203 = pd.to_numeric(df_203)
print(df_203.head())

print (df_203.dtypes)


# df_203.plot(x="week", y=["conf"], kind="line", color = 'c')

# plt.show()
