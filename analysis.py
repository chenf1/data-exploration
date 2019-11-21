#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from scipy import stats


# In[ ]:


import statsmodels


# In[ ]:


#pd.__version__


# # Import demographic and hospitalization dataset.
#    clean data: check missing data, reset data types

# In[ ]:


#import demographic
#encoding='iso-8859-1'
demogrh = pd.read_csv('/home/chenf1/pc4/data/demographic.csv',encoding = "ISO-8859-1",dtype={'patientid':'str','siteid':'str',"funddiagnosistxt":"str","funddiagnosis":"str"})


# In[ ]:


demogrh.isnull().sum()


# In[ ]:


#fill missing data
demogrh["antenataldiag"] = demogrh["antenataldiag"].fillna(9)
demogrh.antenataldiag.value_counts()


# In[ ]:


demogrh.loc[:,demogrh.select_dtypes(include ='int64').columns] = demogrh.select_dtypes(include ='int64').apply(lambda x: x.astype('category'))
demogrh["antenataldiag"] = demogrh["antenataldiag"].astype("category")


# In[ ]:


demogrh.dtypes


# In[ ]:


#import hospitalization
hopita = pd.read_sas('/home/chenf1/pc4/data/hospitalization.sas7bdat')


# In[ ]:


hopita.isnull().sum()


# In[ ]:


###insurance type####
hopita["insprimtype"] = hopita["insprimtype"].fillna(9)
hopita.insprimtype.value_counts()


# In[ ]:


hopita.loc[:,['hosptype','hospadmitagegroup','insprimtype','hospdischstat','cicueverunplannedyn','dnreveryn','withdrawaleveryn','ecmoeveryn']]=hopita.loc[:,['hosptype','hospadmitagegroup','insprimtype','hospdischstat','cicueverunplannedyn','dnreveryn','withdrawaleveryn','ecmoeveryn']].apply(lambda x: x.astype('category'))
hopita.loc[:,['patientID','siteid','hospitalizationid']] = hopita.astype({'patientID':'str','siteid':'str','hospitalizationid':'str'})


# In[ ]:


hopita.dtypes


# In[ ]:


hopita.describe()


# # Table 1 summary table(1)--demo and hopit

# In[ ]:


# gender
demogrh.gender.value_counts()


# In[ ]:


demogrh.dtypes


# In[ ]:


# gender vs. race
blk_sex = demogrh[demogrh['raceblack'] == 1].gender.value_counts()
wht_sex = demogrh[demogrh['racecaucasian'] == 1].gender.value_counts()
asn_sex = demogrh[demogrh['raceasian'] == 1].gender.value_counts()
hisp_sex = demogrh[demogrh['ethnicity'] == 1].gender.value_counts()
oth_sex = demogrh[(demogrh['ethnicity'] != 1) & (demogrh['raceblack'] != 1) & (demogrh['racecaucasian'] != 1) & (demogrh['raceasian'] !=1)].gender.value_counts()

race_sex = pd.concat([blk_sex,wht_sex,asn_sex,hisp_sex,oth_sex], keys=['black', 'white','Asian','Hispanic','Others'])
race_sex


# In[ ]:


hopita.dtypes


# In[ ]:


#age group
hopita.hospadmitagegroup.value_counts() 


# In[ ]:


#weight group


# In[ ]:


#Antenatal diagnosis
demogrh.antenataldiag.value_counts() 


# In[ ]:


#Extra-cardiac abnormality
demogrh.extracardyn.value_counts()


# In[ ]:


#Chromosomal abnormality
demogrh.chromsyndyn.value_counts()


# In[ ]:


#Hospitalization type
hopita.hosptype.value_counts() 


# In[ ]:


#Unplanned initial CICU admission
hopita.cicueverunplannedyn.value_counts() 


# # merge two dataframe, race variables with hopitalization IDs

# In[ ]:


hopita = hopita.rename(columns={"patientID": "patientid"})


# In[ ]:


hospita_race = pd.merge(hopita, demogrh, how='left', on = ['patientid'])


# In[ ]:


#hopita.patientid = hopita.patientid.str.replace('.0','').astype('str')


# # import demo from sas file
# and merge with hospitablizaion: hospita_race

# In[ ]:


#import demographics from sas
demo_sas = pd.read_sas('/home/chenf1/pc4/data/demographic.sas7bdat')


# In[ ]:


demo_sas.dtypes


# In[ ]:


demo_sas.isnull().sum()


# In[ ]:


#fill missing data
#demo_sas["antenataldiag"] = demo_sas["antenataldiag"].fillna("9.0")
#demo_sas["antenataldiag"] = demo_sas["antenataldiag"].astype("category")
#demo_sas.antenataldiag.value_counts()


# In[ ]:


demo_sas.loc[:,['patientid','siteid','funddiagnosis','funddiagnosistxt']] = demo_sas.astype({'patientid':'str','siteid':'str',"funddiagnosis":"str",'funddiagnosistxt':'str'})


# In[ ]:


demo_sas.loc[:,demo_sas.select_dtypes(include ='float64').columns] = demo_sas.select_dtypes(include ='float64').apply(lambda x: x.astype('category'))


# In[ ]:


demo_sas.head(4)


# In[ ]:


demo_sas.sort_values(by=['patientid'],ascending=False)


# In[ ]:


#race_summ = pd.DataFrame(demo_sas.groupby(['raceasian','raceblack','racecaucasian','ethnicity','racenativeam','racenativepi','raceother']).size())
#race_summ


# In[ ]:


#create new race category variable: 1. hispanic, 2.black, 3.white, 4.asian,5.multiple & others, 9.unknown
#demo_sas["race_grp"] = demo_sas[['raceblack','racecaucasian','raceasian','ethnicity']].apply(lambda x: 1 if (x['ethnicity'] == 1.0) 
#                                                                                                     else 2 if ((x['raceblack'] ==1.0) & (x['racecaucasian'] ==0.0) & (x['raceasian'] ==0.0)) 
#                                                                                                     else 3 if ((x['raceblack'] ==0.0) & (x['racecaucasian'] ==1.0) & (x['raceasian'] ==0.0))
#                                                                                                     else 4 if ((x['raceblack'] ==0.0) & (x['racecaucasian'] ==0.0) & (x['raceasian'] ==1.0))
#                                                                                                     else 5 if ((x['raceblack'] + x['racecaucasian'] + x['raceasian'] == 2.0) | (x['raceblack'] + x['racecaucasian'] + x['raceasian'] == 3.0) )
#                                                                                                     else 9 if ((x['raceblack'] ==9.0) & (x['racecaucasian'] ==9.0) & (x['raceasian'] ==9.0))
#                                                                                                     else 6, axis = 1)


# In[ ]:


#create new race category variable: 1. hispanic, 2.black, 3.white, 4.asian,5. multiple & others, 9.unknown
demo_sas["race_grp"] = demo_sas[['raceblack','racecaucasian','raceasian','ethnicity']].apply(lambda x: 1 if (x['ethnicity'] == 1.0) 
                                                                                                     else 2 if ((x['raceblack'] ==1.0) & (x['racecaucasian'] ==0.0) & (x['raceasian'] ==0.0)) 
                                                                                                     else 3 if ((x['raceblack'] ==0.0) & (x['racecaucasian'] ==1.0) & (x['raceasian'] ==0.0))
                                                                                                     else 4 if ((x['raceblack'] ==0.0) & (x['racecaucasian'] ==0.0) & (x['raceasian'] ==1.0))
                                                                                                     else 9 if ((x['raceblack'] ==9.0) & (x['racecaucasian'] ==9.0) & (x['raceasian'] ==9.0))
                                                                                                     else 5, axis = 1)


# In[ ]:


demo_sas["race_grp"].value_counts()


# # merge demo and hopi, create a regroup variable of race

# In[ ]:


#panda version issure, need upgrade to 23
hospita_race = hopita.merge(demo_sas[['patientid','raceblack','racecaucasian','raceasian','ethnicity']], left_on = ["patientid"] , right_on = ["patientid"], sort = True, how = 'left')


# In[ ]:


hospita_race.head(4)


# In[ ]:


hospita_race.dtypes


# In[ ]:


hospita_race.isnull().sum()


# In[ ]:


hospita_race[['raceblack','racecaucasian','raceasian','ethnicity']].apply(lambda x: x.value_counts())


# In[ ]:


#create new race category variable: 1. hispanic, 2.black, 3.white, 4.asian,5.multiple & others, 9.unknown
hospita_race["race_grp"] = hospita_race[['raceblack','racecaucasian','raceasian','ethnicity']].apply(lambda x: 1 if (x['ethnicity'] == 1.0) 
                                                                                                     else 2 if ((x['raceblack'] ==1.0) & (x['racecaucasian'] ==0.0) & (x['raceasian'] ==0.0)) 
                                                                                                     else 3 if ((x['raceblack'] ==0.0) & (x['racecaucasian'] ==1.0) & (x['raceasian'] ==0.0))
                                                                                                     else 4 if ((x['raceblack'] ==0.0) & (x['racecaucasian'] ==0.0) & (x['raceasian'] ==1.0))
                                                                                                     else 9 if ((x['raceblack'] ==9.0) & (x['racecaucasian'] ==9.0) & (x['raceasian'] ==9.0))
                                                                                                     else 5, axis = 1)


# In[ ]:


"""def race_regrp(x):
    if (x['ethnicity'] == '1.0'): result = 1
    elif ((x['raceblack'] =='1.0') & (x['racecaucasian'] =='0.0') & (x['raceasian'] =='0.0')) : result = 2
    elif ((x['raceblack'] =='0.0') & (x['racecaucasian'] =='1.0') & (x['raceasian'] =='0.0')) : result = 3
    elif ((x['raceblack'] =='0.0') & (x['racecaucasian'] =='0.0') & (x['raceasian'] =='1.0')) : result = 4
    elif ((x['raceblack'] =='9.0') & (x['racecaucasian'] =='9.0') & (x['raceasian'] =='9.0')) : result = 5 
    else : result = 6
    return result
hospita_race["race_grp"] = hospita_race[['raceblack','racecaucasian','raceasian','ethnicity']].apply(race_regrp)"""


# In[ ]:


hospita_race.race_grp.value_counts()


# In[ ]:


hospita_race[['raceblack','racecaucasian','raceasian','ethnicity','race_grp']].head()


# # cross table and chi squre tests (Table 1)

# In[ ]:


hospita_race.dtypes


# In[ ]:


print(hospita_race.withdrawaleveryn.value_counts())
print(hospita_race.dnreveryn.value_counts())
print(hospita_race.insprimtype.value_counts())


# In[ ]:


###demo gender, extracardyn, chromsyndyn ,antenataldiag vs race###

#### hospitalization type, unplanned, age group, dnreveryn,withdrawaleveryn,insprimtype vs race###
#counts/freqs
#contingency_table = pd.crosstab(hospita_race['hosptype'], hospita_race['race_grp'],margins = True)
contingency_table = pd.crosstab(hospita_race['insprimtype'],hospita_race['race_grp'])
contingency_table


# In[ ]:


#chi square test
stats.chi2_contingency(np.array(contingency_table))[0:3]


# In[ ]:


#another way for chi square test
f_obs = np.array([contingency_table.iloc[0][0:6].values,
                  contingency_table.iloc[1][0:6].values,
                 contingency_table.iloc[2][0:6].values + contingency_table.iloc[3][0:6].values,
                 contingency_table.iloc[4][0:6].values])
print(f_obs)
stats.chi2_contingency(f_obs)[0:3]


# In[ ]:


#percentages
#cross table row percentage
#pd.crosstab(hospita_race.hosptype,hospita_race.race_grp, normalize='index').round(4)*100
pd.crosstab(hospita_race.hosptype,hospita_race.race_grp).apply(lambda r: r/r.sum(), axis=1)
#cross table column percentage
pd.crosstab(hospita_race.hosptype,hospita_race.race_grp).apply(lambda r: r/r.sum(), axis=0)


# # import surgey hopitalization

# In[ ]:


#import surgery hopitablization
surg_hospi = pd.read_sas('/home/chenf1/pc4/data/surghosp.sas7bdat')


# In[ ]:


surg_hospi.isnull().sum()


# In[ ]:


surg_hospi.dtypes


# In[ ]:


#panda version issure, need upgrade to 23
surg_hospi = surg_hospi.rename(columns={"patientID": "patientid"})
surg_hospi['patientid'] = surg_hospi['patientid'].astype('str')


# In[ ]:


surg_hospi_race = surg_hospi.merge(demo_sas[['patientid','race_grp']], left_on = ["patientid"] , right_on = ["patientid"], sort = True, how = 'left')


# In[ ]:


surg_hospi_race.head()


# In[ ]:


surg_hospi_race.dtypes


# In[ ]:


print(surg_hospi_race.preopHighRiskYN.value_counts())
print(surg_hospi_race.preopLowRiskYN.value_counts())
print(surg_hospi_race.VentAdmitPostopYN.value_counts())
print(surg_hospi_race.STATcat.value_counts())
print(surg_hospi_race.PostopLactateYN.value_counts())
print(surg_hospi_race.PostopMAPyn.value_counts())
print(surg_hospi_race.PostopFiO2yn.value_counts())


# In[ ]:


surg_hospi_race[['CPBtm',"xClampTime","VISatSurg","VIS2hrPostop",'DHCAtm']].describe()


# In[ ]:


#two way tables
contingency_table = pd.crosstab(surg_hospi_race['STATcat'],surg_hospi_race['race_grp'])
print(contingency_table)
print(stats.chi2_contingency(np.array(contingency_table))[0:3])


# In[ ]:


# two way tables-- ttest/anova
surg_hospi_race[['race_grp','CPBtm',"xClampTime","VISatSurg","VIS2hrPostop",'DHCAtm']].groupby('race_grp').mean()


# In[ ]:


#ANOVA test
#'CPBtm',"xClampTime","VISatSurg","VIS2hrPostop",'DHCAtm'
f, p = stats.f_oneway(surg_hospi_race[surg_hospi_race['race_grp'] == 1].VIS2hrPostop.dropna(),
                      surg_hospi_race[surg_hospi_race['race_grp'] == 2].VIS2hrPostop.dropna(),
                      surg_hospi_race[surg_hospi_race['race_grp'] == 3].VIS2hrPostop.dropna(),
                      surg_hospi_race[surg_hospi_race['race_grp'] == 4].VIS2hrPostop.dropna(),
                      surg_hospi_race[surg_hospi_race['race_grp'] == 5].VIS2hrPostop.dropna(),
                      surg_hospi_race[surg_hospi_race['race_grp'] == 9].VIS2hrPostop.dropna())
 
print ('One-way ANOVA')
print ('=============')
print ('F value:', f)
print ('P value:', p, '\n')


# In[ ]:


import statsmodels.formula.api as smf
import statsmodels.api as sm


# # import encounter dataset

# In[ ]:


#import surgery hopitablization
enct = pd.read_sas('/home/chenf1/pc4/data/encounters.sas7bdat')
print(enct.isnull().sum())


# In[ ]:


print(enct.dtypes)


# In[ ]:


print(enct.CompHepaticFail.value_counts())
print(enct.CRRTarf.value_counts())
print(enct.CompStrokeHem.value_counts())
print(enct.CompSeizure.value_counts())
print(enct[enct.EncType==1].ECMOenc.value_counts())


# In[ ]:


#panda version issure, need upgrade to 23
enct.patientID = enct.patientID.astype("str")
enct_race = enct.merge(demo_sas[['patientid','race_grp']], left_on = ["patientID"] , right_on = ["patientid"], sort = True, how = 'left')


# In[ ]:


enct_race.dtypes


# In[ ]:


enct_race.head()


# In[ ]:


#two way table by race
#two way tables
tmp = enct_race[enct_race.EncType==1]
contingency_table = pd.crosstab(tmp.ECMOenc,tmp.race_grp)
print(contingency_table)
print(stats.chi2_contingency(np.array(contingency_table))[0:3])


# # import medical hopitalization data

# In[ ]:


#import surgery hopitablization
med_hosp = pd.read_sas('/home/chenf1/pc4/data/medhosp.sas7bdat')
print(med_hosp.isnull().sum())


# In[ ]:


med_hosp.dtypes


# In[ ]:


#panda version issure, need upgrade to 23
med_hosp.patientID = med_hosp.patientID.astype("str")
med_hosp_race = med_hosp.merge(demo_sas[['patientid','race_grp']], left_on = ["patientID"] , right_on = ["patientid"], sort = True, how = 'left')


# In[ ]:


med_hosp_race.head()


# In[ ]:


med_hosp_race.dtypes


# In[ ]:


# data error for VIS2hrMed
for colmns in med_hosp_race[['myocarditisYN','cardiomyopathyYN','adhfYN','chronicHFyn','transplantRejectYN','Vent2hrMedYN','PHTNyn', 
                            'BNPyn','CrYN','LactateYN']]:
    print(med_hosp_race[colmns].value_counts())


# In[ ]:


med_hosp_race.describe()


# In[ ]:


print(enct[enct.EncType==2.0].ECMOenc.value_counts())


# In[ ]:


#two way table by race
#'myocarditisYN','cardiomyopathyYN','adhfYN','chronicHFyn','transplantRejectYN','Vent2hrMedYN','PHTNyn','BNPyn','CrYN','LactateYN'
contingency_table = pd.crosstab(med_hosp_race.CrYN,med_hosp_race.race_grp)
contingency_table


# In[ ]:


print(stats.chi2_contingency(np.array(contingency_table))[0:3])


# In[ ]:


# two way tables-- ttest/anova
med_hosp_race[['race_grp',"VIS2hrMed"]].groupby('race_grp').mean()


# In[ ]:


#ANOVA test
stats.f_oneway(med_hosp_race[med_hosp_race['race_grp'] == 1].VIS2hrMed.dropna(),
                      med_hosp_race[med_hosp_race['race_grp'] == 2].VIS2hrMed.dropna(),
                      med_hosp_race[med_hosp_race['race_grp'] == 3].VIS2hrMed.dropna(),
                      med_hosp_race[med_hosp_race['race_grp'] == 4].VIS2hrMed.dropna(),
                      med_hosp_race[med_hosp_race['race_grp'] == 5].VIS2hrMed.dropna(),
                      med_hosp_race[med_hosp_race['race_grp'] == 9].VIS2hrMed.dropna())
 


# # import ECMO records 

# In[ ]:


#import surgery hopitablization
ecmo = pd.read_sas('/home/chenf1/pc4/data/ecmo.sas7bdat')
print(ecmo.isnull().sum())


# In[ ]:


ecmo.head()


# In[ ]:


# the number of patients
ecmo.shape
#ecmo.patientID.unique().shape


# In[ ]:


#attach race
ecmo.patientID = ecmo.patientID.astype("str")
ecmo_race = ecmo.merge(demo_sas[['patientid','race_grp']], left_on = ["patientID"] , right_on = ["patientid"], sort = True, how = 'left')


# In[ ]:


ecmo_race.head()


# In[ ]:


# unique ecmo patients broken down by race
ecmo_race[['patientID','race_grp']].groupby('race_grp').nunique()


# In[ ]:


# broken down ecmo by race
ecmo_race[['patientID','race_grp']].groupby('race_grp').count()


# In[ ]:


ecmo_race[['patientID','ECMOreason','race_grp']].groupby(['ECMOreason','race_grp']).count()

