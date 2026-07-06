import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold,train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
import joblib
xgb_params = {
    "model__n_estimators": [100, 200, 300, 500],
    "model__max_depth": [3, 5, 7, 9],
    "model__learning_rate": [0.01, 0.05, 0.1, 0.2, 0.3],
    "model__subsample": [0.7, 0.8, 0.9, 1.0],
    "model__colsample_bytree": [0.7, 0.8, 0.9, 1.0],
    "model__min_child_weight": [1, 3, 5]
}

def tune_model(model, param_grid, X_train, y_train, cv):
    search = RandomizedSearchCV(
        estimator=model,param_distributions=param_grid,n_iter=80,
        scoring="recall",
        cv=cv,random_state=42,
        n_jobs=-1,
        refit=True
    )

    search.fit(X_train, y_train)

    print(f"Best CV Recall: {search.best_score_:.4f}")
    print(f"Best Parameters: {search.best_params_}\n")

    return search.best_estimator_

def evaluate_model(name, model, X, y):
    print(f"--- {name} ---")
    y_pred = model.predict(X)
    print(classification_report(y, y_pred))
 


def mlm(df):
    X = df.drop(columns=["at_risk"])
    y = df["at_risk"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    print("Tuning XGBoost...")
    pipeline = ImbPipeline(steps=[('scaler',  StandardScaler()),
                                  ('smote',   SMOTE(random_state=42)),('model',   XGBClassifier(eval_metric="logloss", random_state=42))])
    best_xgb = tune_model(pipeline, xgb_params, X_train, y_train, cv)
    evaluate_model("XGBoost", best_xgb, X_test, y_test)

    best_xgb["model"].save_model("xgbopt.json")
    joblib.dump(best_xgb["scaler"], "scaler.pkl")   # save the fitted scaler too

    return "xgbopt.json", "scaler.pkl"