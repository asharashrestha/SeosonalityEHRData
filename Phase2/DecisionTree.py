import pandas as pd
import datetime as dt
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import tree
import graphviz


# importing the beneficiaries file
df_ben = pd.read_csv(
    '/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv',
    dtype='str')
ccs = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 1/icd_ccs_No_Dups.csv',
                  dtype='str')  # ccs data import
# removing unnecessary columns from ccs
remove_cols = ['OPTIONAL_CCS_CATEGORY_DESCRIPTION', 'OPTIONAL_CCS_CATEGORY', 'ICD_9_CM_CODE_DESCRIPTION']

ccs.drop(remove_cols, inplace=True, axis=1)

# importing claims file
df_clm = pd.read_csv(
    '/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/Paper 2/20 Sample Data /DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv',
    dtype='str')

df = pd.merge(df_clm, df_ben, left_on='DESYNPUF_ID', right_on='DESYNPUF_ID', how='left')

df = df[['CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1', 'BENE_BIRTH_DT', 'BENE_DEATH_DT',
         'BENE_SEX_IDENT_CD']].copy()
# check if Date of Birth is NULL
df_dob = df.query('BENE_BIRTH_DT != BENE_BIRTH_DT')
# print(df_dob.head())
# check if gender is NULL
df_deathdf_sex = df.query('BENE_SEX_IDENT_CD != BENE_SEX_IDENT_CD')
# print(df_sex.head())

# check if date of death is NULL
df_death = df.query('BENE_DEATH_DT != BENE_DEATH_DT')

# Converting Admission Date to DateTime
df['CLM_ADMSN_DT'] = pd.DatetimeIndex(df['CLM_ADMSN_DT']).month.map(str)

# calculating Age
now = pd.Timestamp(dt.datetime.now())
df['now'] = pd.to_datetime(now)
df['now'] = pd.to_datetime(df['now'], format='%Y%m%d')

df['dob'] = pd.to_datetime(df['BENE_BIRTH_DT'], format='%Y%m%d')
df['dod'] = pd.to_datetime(df['BENE_DEATH_DT'], format='%Y%m%d')
df['dod'] = df.dod.combine_first(df.now)

df['age'] = pd.to_numeric((df['dod'] - df['dob']).astype('m8[Y]'), downcast='signed')

df = df[['CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1', 'BENE_SEX_IDENT_CD', 'age']].copy()

# Separating Summer and Winter Month (if Dec, Jan, Feb then Winter. if Jun, Jul, Aug then Summer else "Season")
df['Season'] = 'Season'
df['Season'] = np.where(df.CLM_ADMSN_DT == '1', 'Winter',
                        np.where(df.CLM_ADMSN_DT == '2', 'Winter',
                                 np.where(df.CLM_ADMSN_DT == '12', 'Winter',
                                          np.where(df.CLM_ADMSN_DT == '6', 'Summer',
                                                   np.where(df.CLM_ADMSN_DT == '7', 'Summer',
                                                            np.where(df.CLM_ADMSN_DT == '8', 'Summer', 'Season'
                                                                     ))))))

# Remove all other data except Summer and Winter

df = df[df['Season'].isin(['Summer', 'Winter'])]
df.drop('CLM_ADMSN_DT', inplace=True, axis=1)

# joining Admission Diag Code and ICD Code with CCS

df = pd.merge(df, ccs, left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code', how='left')
# dropping unwamted columns
columns = ['CCS_CATEGORY', 'ICD9_Code', 'ADMTNG_ICD9_DGNS_CD']
df.drop(columns, inplace=True, axis=1)
df = df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'ADMTNG_ICD9_DGNS_CD'})

df = pd.merge(df, ccs, left_on='ICD9_DGNS_CD_1', right_on='ICD9_Code', how='left')
# dropping unwamted columns
columns = ['CCS_CATEGORY', 'ICD9_Code', 'ICD9_DGNS_CD_1']
df.drop(columns, inplace=True, axis=1)
df = df.rename(columns={'CCS_CATEGORY_DESCRIPTION': 'ICD9_DGNS_CD_1'})

# Remove all data except for the ICD1 Codes as the 6 classes that we described
df = df[df['ICD9_DGNS_CD_1'].isin(
    ['Pneumonia', 'Asthma', 'Viral infect', 'COPD', 'Tuberculosis', 'Oth low resp', 'Bronchitis'])]
df = df.dropna(how='any', axis=0)


# Converting Season into numerical data
cleanup_season = {"Season": {"Summer": 1, "Winter": 2},
            "BENE_SEX_IDENT_CD": {"1": 1, "2": 2}}

df.replace(cleanup_season, inplace=True)
# creating dummy columns for different admission diagnosis codes
df = pd.get_dummies(df, columns=["ADMTNG_ICD9_DGNS_CD"])
print(df.head())

#Decision Tree start

import subprocess
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier, export_graphviz

def encode_target(df, target_column):
    """Add column to df with integers for the target.

    Args
    ----
    df -- pandas DataFrame.
    target_column -- column to map to int, producing
                     new Target column.

    Returns
    -------
    df_mod -- modified DataFrame.
    targets -- list of target names.
    """

    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod["Target"] = df_mod[target_column].replace(map_to_int)
    return (df_mod, targets)

#encoding the target i.e. ICD1 in our case
df2, targets = encode_target(df, "ICD9_DGNS_CD_1")

print("* df2.head()", df2[["Target", "ICD9_DGNS_CD_1"]].head(),
      sep="\n", end="\n\n")
print("* df2.tail()", df2[["Target", "ICD9_DGNS_CD_1"]].tail(),
      sep="\n", end="\n\n")
print("* targets", targets, sep="\n", end="\n\n")
df2.to_csv('dtree_temp.csv', sep=',')

df2.drop('ICD9_DGNS_CD_1', inplace=True, axis=1)
df2.to_csv('dtree.csv', sep=',')
##Featues
features = list(df2.columns[:])
print("* features:", features, sep="\n")

#fitting the decision tree
y = df2["Target"]
X = df2[features]
dt = DecisionTreeClassifier(min_samples_split=20, random_state=99)
# print(df2.head())




#Vizualize the tree
def visualize_tree(tree, feature_names):
    """Create tree png using graphviz.

    Args
    ----
    tree -- scikit-learn DecsisionTree.
    feature_names -- list of feature names.
    """
    with open("dt.dot", 'w') as f:
        export_graphviz(tree, out_file=f,
                        feature_names=feature_names)

    command = ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
    try:
        subprocess.check_call(command)
    except:
        exit("Could not run dot, ie graphviz, to "
             "produce visualization")



# visualize_tree(dt, features)

#training and testing set
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size = 0.3, random_state = 100)
# prediction = dt.predict([[1,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5]])
# print("Prediction: ", prediction)



#Decision Tree with Entropy as criterion
# clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
#  max_depth=3, min_samples_leaf=7)
# clf_entropy.fit(X_train, y_train)
#
# y_pred_en = clf_entropy.predict(X_test)
# print("Accuracy is for criterion as information gain ", accuracy_score(y_test,y_pred_en)*100)
# print("Confusion Matrix with information gain:\n", confusion_matrix(y_test, y_pred_en))
#

#Decision Tree with Criterion as Gini Index

clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100, max_depth=3)
clf_gini.fit(X_train, y_train)


y_pred = clf_gini.predict(X_test)
print("Accuracy with gini Index is ", accuracy_score(y_test,y_pred)*100)

print("Confusion Matrix with gini index:\n", confusion_matrix(y_test, y_pred))

# clf_gini.predict_proba(df2[:1, :])

# import graphviz
# dot_data = tree.export_graphviz(clf_gini, out_file=None)
# graph = graphviz.Source(dot_data)
# graph.render("df2")
# visualize_tree(clf_gini, features)

#Decision Tree Default Criterion
# dt.fit(X_train, y_train)
# y_pred = dt.predict(X_test)
# print("Accuracy is ", accuracy_score(y_test,y_pred)*100)