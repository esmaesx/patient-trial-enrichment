import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier


def train_models(df, target_col="outcome", seed=7):
    X = df.drop(columns=[target_col])
    y = df[target_col].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed, stratify=y
    )

    models = {
        "logreg": Pipeline(
            [
                ("scaler", StandardScaler(with_mean=True, with_std=True)),
                ("clf", LogisticRegression(max_iter=200, class_weight="balanced")),
            ]
        ),
        "gboost": GradientBoostingClassifier(random_state=seed),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        proba = model.predict_proba(X_test)[:, 1]
        results[name] = {
            "model": model,
            "roc_auc": roc_auc_score(y_test, proba),
            "pr_auc": average_precision_score(y_test, proba),
            "brier": brier_score_loss(y_test, proba),
            "y_test": y_test,
            "proba": proba,
        }

    return results
