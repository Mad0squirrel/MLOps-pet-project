"""Script for training and evaluating model."""

import os

import click
import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from dotenv import load_dotenv
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

load_dotenv()
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "")
RANDOM_STATE = int(os.environ.get("RANDOM_STATE", "0"))


TARGET = "price"
CAT_FEATURES = ["type of house", "number of rooms", "area of apartment", "repair", "terrace", "bathroom"]


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

    df = pd.get_dummies(df, columns=CAT_FEATURES, prefix=CAT_FEATURES, drop_first=True)
    click.echo(list(df.columns))

    x = df.drop(columns=[TARGET]).values
    y = df[TARGET].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=RANDOM_STATE)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("ml-project")
    with mlflow.start_run(run_name="ridge-regression"):

        linear_model = Ridge(alpha=10, tol=1e-4, solver="svd")
        linear_model.fit(x_train, y_train)
        predicts = linear_model.predict(x_test)

        mlflow.log_params(linear_model.get_params())

        r2_score_value = r2_score(y_test, predicts)
        root_mean_squared_error_value = root_mean_squared_error(y_test, predicts)
        mlflow.log_metric("r2_score", r2_score_value)
        mlflow.log_metric("rMSE", root_mean_squared_error_value)

        mlflow.sklearn.log_model(linear_model, "linear_model")

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        y_min, y_max = y_test.min(), y_test.max()
        ax.plot([y_min, y_max], [y_min, y_max], c="g")
        ax.scatter(y_test, predicts, c="r")
        mlflow.log_figure(fig, "prediction_result.png")


if __name__ == "__main__":
    cli()