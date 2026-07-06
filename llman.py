from ollama import Client
import xgboost as xgb
import shap
import numpy as np
import pandas as pd
import joblib
class LLM:
    def __init__(self, filename, scaler_file, X):
        self.loaded_model = xgb.XGBClassifier()
        self.loaded_model.load_model(filename)
        self.scaler = joblib.load(scaler_file)
        self.X = pd.DataFrame(
            self.scaler.transform(X), columns=X.columns, index=X.index
        )
        self.explainer = shap.Explainer(self.loaded_model, X)
        #self.shap_values = self.explainer(X)
    
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
            "Encoded socioeconomic deprivation level (Index of Multiple Deprivation): 0=0-10%, 1=10-20%, 2=20-30%, 3=30-40%, 4=40-50%, 5=50-60%, 6=60-70%, 7=70-80%, 8=80-90%, 9=90-100%. ",


        "education_enc":
            "Encoded highest education level achieved before enrolling: 0=No Formal Qualifications, 1=Lower Than A Level, 2=A Level or Equivalent, 3=HE Qualification, 4=Postgraduate Qualification.",

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
            "Whether the student has declared a disability (1 = Yes, 0 = No)."
    }
    client = Client(host="http://localhost:11434")

    def ask_llm(self,prompt):
        response = self.client.chat(
            model="gemma4:e2b",
            messages=[
                {
                    "role": "system",
                    "content":
                    """
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
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
    def explain_student(self, student_id, df):
        idx = df.loc[df["id_student"] == student_id].index[0]
        sample = self.X.loc[idx]
        shap_values = self.explainer(sample.to_frame().T)
        prediction = self.loaded_model.predict(sample.to_frame().T)[0]
        prompt = self.build_prompt(sample, shap_values, prediction)
        return self.ask_llm(prompt)
    def build_prompt(self,sample, shap_values, prediction):
        print(sample,shap_values,prediction)
        # Handle new SHAP Explanation objects
        if isinstance(shap_values, shap.Explanation):
            shap_values = shap_values.values

        shap_values = np.asarray(shap_values).flatten()

        df = pd.DataFrame({
            "Feature": sample.index,
            "Value": sample.values,
            "SHAP": shap_values
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
