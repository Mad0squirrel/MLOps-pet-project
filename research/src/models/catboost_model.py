"""Script for training and evaluating model."""

import os

import click
import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from catboost import CatBoostRegressor
from dotenv import load_dotenv
from mlflow.models import infer_signature
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

load_dotenv()
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "")
RANDOM_STATE = int(os.environ.get("RANDOM_STATE", "0"))

TARGET = "price"
CAT_FEATURES = ["type of house", "number of rooms", "area of apartment" "repair", "terrace", "bathroom"]

@click.command()
@click.argument("dataset_file", type=click.Path(readable=True))
def cli(dataset_file: str) -> None:
    """Train and evaluate linear model.
    
    Parameters
    ----------
     dataset_file: str 
    
    Returns
    -------
     nothing
    
    """
    df = pd.read_csv(dataset_file)
    x = df.drop(columns=[TARGET])
    y = df[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=RANDOM_STATE)
    
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("ml-project")
    with mlflow.start_run(run_name="catboost"):
        
        catboost_model = CatBoostRegressor(n_estimators=150, max_depth=6, random_state=RANDOM_STATE)
        catboost_model.fit(x_train, y_train, cat_features=CAT_FEATURES)
        predicts = catboost_model.predict(x_test)
        signature = infer_signature(x_test, predicts)
        
        mlflow.log_params(catboost_model.get_params())
        
        r2_score_value = r2_score(y_test, predicts)
        root_mean_squared_error_value = root_mean_squared_error(y_test, predicts)
        mlflow.log_metric("r2_score", r2_score_value)
        mlflow.log_metric("rMSE", root_mean_squared_error_value)
        
        mlflow.catboost.log_model(
            cb_model=catboost_model,
            artifact_path="catboost",
            signature=signature,
            registered_model_name="catboost-reg-model",
        )
        
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        y_min, y_max = y_test.min(), y_test.max()
        ax.plot([y_min, y_max], [y_min, y_max], c="g")
        ax.scatter(y_test, predicts, c="r")
        mlflow.log_figure(fig, "prediction_result.png")
        del fig
        
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        feature_names = [c for c in df.columns if c != TARGET]
        feature_importance_list = pd.Series(catboost_model.feature_importances_, index=feature_names)
        feature_importance_list.nlargest(10).plot(kind="barh", ax=ax)
        mlflow.log_figure(fig, "feature_importance.png")


if __name__ == "__main__":
    cli()