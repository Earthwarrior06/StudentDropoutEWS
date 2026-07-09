import pandas as pd
import numpy as np

def dataman(reg,info,course,svle,codemod,codepres):
    info=info.merge(reg,on=["id_student","code_module","code_presentation"])
    svle['week'] = (svle['date'] // 7)+1
    for w in [1, 2, 3]:
        wk = (svle[svle['week'] == w].groupby(['id_student', 'code_module', 'code_presentation'])['sum_click'].sum().rename(f'clicks_week{w}'))
        info = info.merge(wk, on=['id_student', 'code_module', 'code_presentation'], how='left')
        info[f'clicks_week{w}'] = info[f'clicks_week{w}'].fillna(0).astype(int)
    info['click_trend'] = info['clicks_week3'] - info['clicks_week1']   
    info=info.merge(course,  on=['code_module','code_presentation'], how='left')
    last_click = svle.groupby(['id_student', 'code_module', 'code_presentation'])['date'].max().rename('last_click_day')
    info = info.merge(last_click, on=['id_student', 'code_module', 'code_presentation'], how='left')
    info['days_since_last_click'] = info['module_presentation_length']-info['last_click_day']
    unique_res = svle.groupby(['id_student', 'code_module', 'code_presentation'])['id_site'].nunique().rename('unique_resources')
    info = info.merge(unique_res, on=['id_student', 'code_module', 'code_presentation'], how='left')
    info['unique_resources'] = info['unique_resources'].fillna(0).astype(int)
    info['days_since_last_click']=info['days_since_last_click'].fillna(info['module_presentation_length']).astype(int)
    info['unregistered_early'] = (
    info['date_unregistration'].notna() &
    (info['date_unregistration'] < info['module_presentation_length'])
    ).astype(int)
    info['registered_late'] = (info['date_registration'] > 0).astype(int)



    info.drop(columns=['date_registration', 'date_unregistration'], inplace=True)
    eduo = {'No Formal quals': 0, 'Lower Than A Level': 1,
                'A Level or Equivalent': 2, 'HE Qualification': 3,
                'Post Graduate Qualification': 4}
    info['education_enc'] = info['highest_education'].map(eduo)
    ageo = {'0-35':1,'35-55':2,'55<=':3}
    info['age_enc'] = info['age_band'].map(ageo).astype(int)
    reso = {'Pass': 0, 'Distinction': 0, 'Fail': 1, 'Withdrawn': 1}
    info['at_risk'] = info['final_result'].map(reso)
    imdo = {
        '0-10%':0, '10-20':1, '20-30%':2, '30-40%':3, '40-50%':4,
        '50-60%':5, '60-70%':6, '70-80%':7, '80-90%':8, '90-100%':9
    }

    info["imd_band_enc"] = info["imd_band"].map(imdo)


    TrueData = info[(info["code_module"] == codemod) &(info["code_presentation"] == codepres)]
    info = info[~(
    (info["code_module"] == codemod) &
    (info["code_presentation"] == codepres)
    )]


    info["imd_band_enc"] = (
    info["imd_band_enc"]
    .fillna(
        info.groupby("region")["imd_band_enc"]#["region", "final_result"]
            .transform("median")
    ))
    info["imd_band_enc"] = info["imd_band_enc"].round().astype(int)
    TrueData["imd_band_enc"] = (
    TrueData["imd_band_enc"]
    .fillna(
        TrueData.groupby("region")["imd_band_enc"]
            .transform("median")
    )
    )
    TrueData["imd_band_enc"] = TrueData["imd_band_enc"].round().astype(int)
    engineered= info[["gender","region","num_of_prev_attempts","studied_credits",
                  "disability","clicks_week1","clicks_week2","clicks_week3",
                  "click_trend","module_presentation_length","unregistered_early",
                  "days_since_last_click","unique_resources","registered_late",
                  "imd_band_enc","education_enc","age_enc",
                  "at_risk"]]
    engineered2= TrueData[["id_student","gender","region","num_of_prev_attempts","studied_credits",
                  "disability","clicks_week1","clicks_week2","clicks_week3",
                  "click_trend","module_presentation_length","unregistered_early",
                  "days_since_last_click","unique_resources","registered_late",
                  "imd_band_enc","education_enc","age_enc",
                  "at_risk"]]
    e2 = pd.get_dummies(engineered,dtype=int)
    f2=pd.get_dummies(engineered2,dtype=int)
    return e2,f2