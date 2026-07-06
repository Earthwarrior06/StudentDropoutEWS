import streamlit as st
import pandas as pd

from dataman import dataman
from mlman import mlm
from llman import LLM

st.set_page_config(page_title="Student Early Warning System", layout="wide")

st.title("Student Dropout Early Warning System")

st.header("Upload OULAD Files")

reg_file = st.file_uploader("Student Registration", type="csv")
info_file = st.file_uploader("Student Information", type="csv")
vle_file = st.file_uploader("Student VLE", type="csv")
course_file = st.file_uploader("Courses", type="csv")

module = st.text_input("Module Code", value="BBB")
presentation = st.text_input("Presentation", value="2014J")

if all([reg_file, info_file, vle_file, course_file]):

    reg = pd.read_csv(reg_file)
    info = pd.read_csv(info_file)
    svle = pd.read_csv(vle_file)
    course = pd.read_csv(course_file)

    if st.button("Prepare Dataset"):

        with st.spinner("Engineering features..."):

            train_df, prediction_df = dataman(
                reg,
                info,
                course,
                svle,
                module,
                presentation
            )
            

        st.success("Dataset prepared.")

        st.write("Training rows:", len(train_df))
        st.write("Prediction rows:", len(prediction_df))

        st.session_state["train_df"] = train_df
        st.session_state["prediction_df"] = prediction_df


if "train_df" in st.session_state:

    if st.button("Train XGBoost"):

        with st.spinner("Training model..."):

            model_file, scaler_file = mlm(st.session_state["train_df"])

        st.success("Training complete.")

        st.session_state["model_file"] = model_file


if "model_file" in st.session_state:

    pred_df = st.session_state["prediction_df"]

    X_pred = pred_df.drop(columns=["id_student", "at_risk"])

    llm = LLM(
        st.session_state["model_file"], scaler_file,
        X_pred
    )
    y_true = pred_df["at_risk"]

    print("\n===== Evaluation on Prediction Dataset =====")
    from sklearn.metrics import classification_report

    y_pred = llm.loaded_model.predict(X_pred)
    print(classification_report(y_true, y_pred))
    predictions = llm.loaded_model.predict(X_pred)
    probabilities = llm.loaded_model.predict_proba(X_pred)[:, 1]

    results = pred_df.copy()
    results["Prediction"] = predictions
    results["Risk Probability"] = probabilities

    st.header("Predictions")

    st.dataframe(
        results[
            ["id_student", "Prediction", "Risk Probability"]
        ]
    )

    student = st.selectbox(
        "Select Student",
        results["id_student"]
    )

    if st.button("Explain Prediction"):

        explanation = llm.explain_student(student, pred_df)

        st.subheader("LLM Explanation")

        st.write(explanation)