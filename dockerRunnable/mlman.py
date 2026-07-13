import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
import joblib
from typing import Tuple, Optional

_XGB_PARAMS = {
    "model__n_estimators": [100, 200, 300, 500],
    "model__max_depth": [3, 5, 7, 9],
    "model__learning_rate": [0.01, 0.05, 0.1, 0.2, 0.3],
    "model__subsample": [0.7, 0.8, 0.9, 1.0],
    "model__colsample_bytree": [0.7, 0.8, 0.9, 1.0],
    "model__min_child_weight": [1, 3, 5],
}


class MLManager:
    def __init__(self, train_df: pd.DataFrame) -> None:
        self.X: pd.DataFrame = train_df.drop(columns=["at_risk"])
        self.y: pd.Series = train_df["at_risk"]
        self.pipeline: Optional[ImbPipeline] = None
        self.model: Optional[XGBClassifier] = None
        self.scaler: Optional[StandardScaler] = None

    def train(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, stratify=self.y, random_state=42
        )
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        print("Tuning XGBoost...")
        pipeline = ImbPipeline(steps=[
            ("scaler", StandardScaler()),
            ("smote", SMOTE(random_state=42)),
            ("model", XGBClassifier(eval_metric="logloss", random_state=42)),
        ])

        search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=_XGB_PARAMS,
            n_iter=80,
            scoring="recall",
            cv=cv,
            random_state=42,
            n_jobs=-1,
            refit=True,
        )
        search.fit(X_train, y_train)

        print(f"Best CV Recall: {search.best_score_:.4f}")
        print(f"Best Parameters: {search.best_params_}\n")

        self.pipeline = search.best_estimator_
        self.model = self.pipeline["model"]
        self.scaler = self.pipeline["scaler"]

        print("--- XGBoost Evaluation ---")
        print(classification_report(y_test, self.pipeline.predict(X_test)))

    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        predictions = self.pipeline.predict(X)
        probabilities = self.pipeline.predict_proba(X)[:, 1]
        return predictions, probabilities

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> str:
        y_pred = self.pipeline.predict(X)
        report = classification_report(y, y_pred)
        print(report)
        return report

    def save(
        self,
        model_path: str = "xgbopt.json",
        scaler_path: str = "scaler.pkl",
    ) -> None:
        self.model.save_model(model_path)
        joblib.dump(self.scaler, scaler_path)

    def load(
        self,
        model_path: str = "xgbopt.json",
        scaler_path: str = "scaler.pkl",
    ) -> None:
        self.model = XGBClassifier()
        self.model.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
