# I. Framing of the dataset
## 1. ER Diagram
<img width="797" height="752" alt="image" src="https://github.com/user-attachments/assets/c257a148-26ea-49ad-964f-29ae9e348f9f" />


## 2. Each Table With Column definition 
**courses.csv**
File contains the list of all available modules and their presentations. The columns are:

- code_module – code name of the module, which serves as the identifier.
- code_presentation – code name of the presentation. It consists of the year and “B” for the presentation starting in February and “J” for the presentation starting in October.
- length – length of the module-presentation in days.
The structure of B and J presentations may differ and therefore it is good practice to analyse the B and J presentations separately. Nevertheless, for some presentations the corresponding previous B/J presentation do not exist and therefore the J presentation must be used to inform the B presentation or vice versa. In the dataset this is the case of CCC, EEE and GGG modules.

**studentInfo.csv**
This file contains demographic information about the students together with their results. File contains the following columns:

- code_module – an identification code for a module on which the student is registered.
- code_presentation – the identification code of the presentation during which the student is registered on the module.
- id_student – a unique identification number for the student.
- gender – the student’s gender.
- region – identifies the geographic region, where the student lived while taking the module-presentation.
- highest_education – highest student education level on entry to the module presentation.
- imd_band – specifies the [Index of Multiple Depravation](https://en.wikipedia.org/wiki/Deprivation_index) band of the place where the student lived during the module-presentation.
- age_band – band of the student’s age.
- num_of_prev_attempts – the number times the student has attempted this module.
- studied_credits – the total number of credits for the modules the student is currently studying.
- disability – indicates whether the student has declared a disability.
- final_result – student’s final result in the module-presentation.
**studentRegistration.csv**
This file contains information about the time when the student registered for the module presentation. For students who unregistered the unregistered date is also recorded. File contains five columns:

- code_module – an identification code for a module.
- code_presentation – the identification code of the presentation.
- id_student – a unique identification number for the student.
- date_registration – the date of student’s registration on the module presentation, this is the number of days measured relative to the start of the module-presentation (e.g. the negative value -30 means that the student registered to module presentation 30 days before it started).
- date_unregistration – the student’s unregistered date from the module presentation, this is the number of days measured relative to the start of the module-presentation. Students, who completed the course have this field empty. Students who unregistered have Withdrawal as the value of the final_result column in the studentInfo.csv file.

**studentVle.csv**
The studentVle.csv file contains information about each student’s interactions with the materials in the VLE.
This file contains the following columns:

- code_module – an identification code for a module.
- code_presentation – the identification code of the module presentation.
- id_student – a unique identification number for the student.
- id_site – an identification number for the VLE material.
- date – the date of student’s interaction with the material measured as the number of days since the start of the module-presentation.
- sum_click – the number of times a student interacts with the material in that day.

**vle.csv**
The csv file contains information about the available materials in the VLE. Typically, these are html pages, pdf files, etc. Students have access to these materials online and their interactions with the materials are recorded.
The vle.csv file contains the following columns:

- id_site – an identification number of the material.
- code_module – an identification code for module.
- code_presentation – the identification code of presentation.
- activity_type – the role associated with the module material.
- week_from – the week from which the material is planned to be used.
- week_to – week until which the material is planned to be used.
## 3. Tables Used (and why)
- StudentInfo: Since it contains all the primary information, including but not limited to final_result,imd_band,age_band,gender,region
- StudentRegistration: As will be shown later, it was used to figure out individual that unregistered early or registered late
- Courses: Used to figure out module lengths, so as to figure out duration since latest activity
- StudentVle: Used to figure out activity trends based on clicks
- ~~Vle: Used to figure out ratio of where the activity of each student is focused~~ *Explained later why the table and its features were removed*  
## 4. Relation between tables


# II. Major observations
## 1. Missing Data and Issues
```bash
data_assess.isnull().sum()
```
```bash
code_module                0
code_presentation          0
id_student                 0
gender                     0
region                     0
highest_education          0
imd_band                1111
age_band                   0
num_of_prev_attempts       0
studied_credits            0
disability                 0
final_result               0
dtype: int64
```
the above shows us that null values exist in the imd_band
it is ~3% of total values that are null
```bash
data_assess["imd_band"].value_counts()
```
```bash
20-30%     3654
30-40%     3539
10-20      3516
0-10%      3311
40-50%     3256
50-60%     3124
60-70%     2905
70-80%     2879
80-90%     2762
90-100%    2536
```
The imd_band 10-20 band lacks a percentage


## 2. Correlations
<img width="567" height="571" alt="image" src="https://github.com/user-attachments/assets/8c4a5ac2-90ff-4cd5-940e-60da267d6587" />
<img width="567" height="571" alt="image" src="https://github.com/user-attachments/assets/039f373f-dddf-4861-8aca-6ead9e5e35ff" />
<img width="567" height="481" alt="image" src="https://github.com/user-attachments/assets/3dbe723f-201d-4c8a-8e1a-9384537b2eff" />
<img width="567" height="430" alt="image" src="https://github.com/user-attachments/assets/d93f4a23-788b-4746-9e74-db57ecf15c1e" />

Gender appears to have near zero effect on final result

<img width="567" height="429" alt="image" src="https://github.com/user-attachments/assets/f01bf31b-b360-4e89-bdd9-a7963464cc6e" />
<img width="589" height="429" alt="image" src="https://github.com/user-attachments/assets/45a2c471-f0c1-4556-b370-4a2e5dd91a80" />

```bash
disability
N    29429
Y     3164
```
The data shows us that disability does seem to affect passing outcome but it is important to note that the number of people with disabilities is disproportionately smaller

<img width="567" height="609" alt="image" src="https://github.com/user-attachments/assets/a846a30d-e189-4305-afc0-60617613f15b" />

```bash
highest_education
A Level or Equivalent          14045
Lower Than A Level             13158
HE Qualification                4730
No Formal quals                  347
Post Graduate Qualification      313
```
It is very apparent that the higher the level of education, people are far less likely to fail

<img width="1635" height="933" alt="image" src="https://github.com/user-attachments/assets/255b1e52-5b94-49bf-9ddd-96ed720a5970" />


# III. Features Engineered
## 1. Mention all features engineered (With definitions)
- clicks_week1/2/3 Total VLE clicks per week (weeks 1-3 only)
- click_trend Week 3 clicks minus Week 1 clicks
- days_since_last_click Days since last recorded activity
- ~~assessment_click_ratio Proportion of clicks on quiz/assessment activity types~~ Only lowered ML model Accuracy
- unique_resources Number of distinct resources accessed
- registered_late Binary: registered after course start date
- unregistered_early Binary: unregistered before course end
- num_of_prev_attempts Number of previous attempts at the module
- imd_band_enc Deprivation index — ordinal encoded 0-9
- education_enc Highest education level — ordinal encoded 0-4
- at_risk Binary: Withdrawn/Fail:1 Distinction/Pass:0
## 2. Mention Why Features Were engineered a certain way

## 3. Mention which features were scrapped and why

# IV. ML Models 
## 1. Mention Which Were Used(tested)
- LogisticRegression
- RandomForestClassifier
- XGBClassifier
## 2. Mention accuracy percentages

## 3. Mention Final Choice of ML model

# V. LLM Details
## 1. LLM Used and Details
- gemma4:e2b ran through Ollama
  - gemma4:e2b was chosen given that it requires minimal resources, but the model can be upgraded depending on the users GPU capability 
## 2. Prompt Engineering Details
### - Model Instructions
```bash
  You are an educational analytics assistant.

Your goal is to explain why the machine learning model made its prediction in language that an academic advisor or student can understand.

Rules:
1. Use ONLY the supplied feature descriptions, values and SHAP values.
2. Never invent facts or causal relationships.
3. Treat SHAP values only as evidence of influence on the prediction.
4. Do not claim that a feature "caused" the student to be at risk.
5. If something cannot be inferred, explicitly say so.
6. Avoid mentioning raw SHAP numbers unless helpful.
7. Focus on what influenced the model most.
8. Write naturally instead of listing features.
9. Explain technical features in plain English.
10. Finish with a short overall summary.
```
### - Prompt
```bash
 def build_prompt(
        self,
        sample: pd.Series,
        shap_values: shap.Explanation,
        prediction: int,
    ) -> str:
        print(sample, shap_values, prediction)

        sv = shap_values.values if isinstance(shap_values, shap.Explanation) else shap_values
        sv = np.asarray(sv).flatten()

        df = pd.DataFrame({
            "Feature": sample.index,
            "Value": sample.values,
            "SHAP": sv,
        })
        df["abs_shap"] = df["SHAP"].abs()
        df = df.sort_values("abs_shap", ascending=False).head(10)

        feature_text = ""
        for _, row in df.iterrows():
            description = self.FEATURE_DESCRIPTIONS.get(row.Feature, "No description available.")
            feature_text += (
                f"- {row.Feature}\n"
                f"  Description: {description}\n"
                f"  Value: {row.Value}\n"
                f"  SHAP: {row.SHAP:.4f}\n\n"
            )

        return f"""
Prediction:
{prediction}

The following are the only available facts.

{feature_text}

Please produce the explanation using exactly these sections.

## Overall assessment
Explain in one or two sentences whether the model considers this student more or less likely to be at risk.

## Main factors increasing the prediction
Describe the 3-5 strongest positive contributors in plain English.

## Main factors reducing the prediction
Describe the strongest negative contributors.

## What this means
Summarise the overall pattern without making causal claims.

Guidelines:
- Avoid saying "SHAP value = ..."
- Avoid bulleting every feature individually.
- Combine related features into a narrative.
- Translate encoded variables into readable language.
- Refer to VLE as the online learning platform.
- If a feature is encoded, explain its meaning.
- Never speculate beyond the supplied information.
"""
```
### - Feature Descriptions
```bash
FEATURE_DESCRIPTIONS = {
        "num_of_prev_attempts":
            "Number of previous times the student has attempted this module.",

        "studied_credits":
            "Total academic credits the student is enrolled in during this presentation.",

        "clicks_week1":
            "Total number of interactions with the Virtual Learning Environment (VLE) during Week 1.",

        "clicks_week2":
            "Total number of interactions with the Virtual Learning Environment (VLE) during Week 2.",

        "clicks_week3":
            "Total number of interactions with the Virtual Learning Environment (VLE) during Week 3.",

        "click_trend":
            "Change in VLE activity over the first three weeks. Positive values indicate increasing engagement, while negative values indicate decreasing engagement.",

        "module_presentation_length":
            "Duration of the module presentation in days.",

        "days_since_last_click":
            "Number of days between the student's last recorded VLE activity and the prediction date.",

        "unique_resources":
            "Number of different learning resources accessed by the student.",

        "registered_late":
            "Whether the student registered after the official start of the module (1 = Yes, 0 = No).",

        "unregistered_early":
            "Whether the student withdrew before the end of the module (1 = Yes, 0 = No).",

        "imd_band_enc":
            "Encoded socioeconomic deprivation level (Index of Multiple Deprivation): "
            "0=0-10%, 1=10-20%, 2=20-30%, 3=30-40%, 4=40-50%, 5=50-60%, 6=60-70%, 7=70-80%, 8=80-90%, 9=90-100%.",

        "education_enc":
            "Encoded highest education level achieved before enrolling: "
            "0=No Formal Qualifications, 1=Lower Than A Level, 2=A Level or Equivalent, "
            "3=HE Qualification, 4=Postgraduate Qualification.",

        "age_band_enc":
            "Encoded age band at enrollment: 1=0-35 years, 2=35-55 years, 3=55 years or older.",

        "gender_F":
            "Whether the student is female (1 = Female, 0 = Not Female).",

        "gender_M":
            "Whether the student is male (1 = Male, 0 = Not Male).",

        "region_East Anglian Region":
            "Whether the student is from the East Anglian Region (1 = Yes, 0 = No).",

        "region_East Midlands Region":
            "Whether the student is from the East Midlands Region (1 = Yes, 0 = No).",

        "region_Ireland":
            "Whether the student is from Ireland (1 = Yes, 0 = No).",

        "region_London Region":
            "Whether the student is from the London Region (1 = Yes, 0 = No).",

        "region_North Region":
            "Whether the student is from the North Region (1 = Yes, 0 = No).",

        "region_North Western Region":
            "Whether the student is from the North Western Region (1 = Yes, 0 = No).",

        "region_Scotland":
            "Whether the student is from Scotland (1 = Yes, 0 = No).",

        "region_South East Region":
            "Whether the student is from the South East Region (1 = Yes, 0 = No).",

        "region_South Region":
            "Whether the student is from the South Region (1 = Yes, 0 = No).",

        "region_South West Region":
            "Whether the student is from the South West Region (1 = Yes, 0 = No).",

        "region_Wales":
            "Whether the student is from Wales (1 = Yes, 0 = No).",

        "region_West Midlands Region":
            "Whether the student is from the West Midlands Region (1 = Yes, 0 = No).",

        "region_Yorkshire Region":
            "Whether the student is from the Yorkshire Region (1 = Yes, 0 = No).",

        "disability_N":
            "Whether the student has not declared a disability (1 = Yes, 0 = No).",

        "disability_Y":
            "Whether the student has declared a disability (1 = Yes, 0 = No).",
    }
```
## 3. Effectiveness at Explaining 
- Example Explanation
```bash
LLM Explanation
Overall assessment
The model predicts a specific outcome based on the combination of student engagement history, academic background, and activity patterns within the online learning platform.

Main factors increasing the prediction
The factors that tend to increase this prediction relate to aspects such as the breadth of learning resources accessed and prior educational background. Specifically, accessing a large number of unique learning resources and having attained a higher level of formal education are positively associated with the outcome. Furthermore, indicators related to socioeconomic status and the duration of the module presentation also contributed to this prediction.

Main factors reducing the prediction
The factors that tend to reduce this prediction are primarily related to recent engagement in the online platform. A longer time has passed since the student's last recorded activity on the Virtual Learning Environment (VLE), and lower interaction rates observed during Week 2 of the module were also noted.

What this means
Overall, the prediction is influenced by a balance between past academic achievement and recent engagement with the online learning platform. While factors related to education level and resource access positively influence the assessment, recent inactivity on the VLE has been a significant mitigating factor.  
```
# VI. Streamlit
## 1. Explain Mistakes made 
## 2. Explain basic understanding 
## 3. Explain Choices made
