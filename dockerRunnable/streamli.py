import streamlit as st
import pandas as pd

from dataman import dataman
from mlman import MLManager
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
            st.session_state.train_df, st.session_state.prediction_df = dataman(
                reg, info, course, svle, module, presentation
            )

        st.success("Dataset prepared.")
        st.write("Training rows:", len(st.session_state.train_df))
        st.write("Prediction rows:", len(st.session_state.prediction_df))

if "train_df" in st.session_state:

    if st.button("Train XGBoost"):

        with st.spinner("Training model..."):
            print("1")
            st.session_state.ml_manager = MLManager(st.session_state.train_df)
            print("2")
            st.session_state.ml_manager.train()
            print("3")
            pred_df = st.session_state.prediction_df
            print("4")
            X_pred = pred_df.drop(columns=["id_student", "at_risk"])
            print("5")
            st.session_state.llm = LLM(st.session_state.ml_manager, X_pred)
            print("6")
            st.session_state.predictions, st.session_state.probabilities = (
                st.session_state.ml_manager.predict(X_pred)
            )
            print("\nEvaluation on Prediction Dataset")
            st.session_state.ml_manager.evaluate(X_pred, pred_df["at_risk"])

            results = pred_df.copy()
            results["Prediction"] = st.session_state.predictions
            results["Risk Probability"] = st.session_state.probabilities
            st.session_state.results = results

        st.success("Training complete.")

if "results" in st.session_state:

    st.header("Predictions")

    st.dataframe(
        st.session_state.results[["id_student", "Prediction", "Risk Probability"]]
    )

    st.session_state.selected_student = st.selectbox(
        "Select Student",
        st.session_state.results["id_student"],
    )

    if st.button("Explain Prediction"):

        explanation = st.session_state.llm.explain_student(
            st.session_state.selected_student,
            st.session_state.prediction_df,
        )

        st.subheader("LLM Explanation")
        st.write(explanation)
