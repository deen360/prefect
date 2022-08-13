import pandas as pd
import pickle
import s3fs
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from dateutil.relativedelta import relativedelta
from datetime import datetime

from prefect import task, flow, get_run_logger
import mlflow
from prefect.task_runners import SequentialTaskRunner

#mlflow.set_tracking_uri("http://127.0.0.1:5000")
#mlflow.set_experiment("my-experiment-1")





mlflow.sklearn.autolog()
@task
def read_dataframe(path):
    logger = get_run_logger()

    df = pd.read_parquet(path)
    logger.info(f"input file succesfully loaded from {path}")
    return  df

@task
def preparing_features(df_train, df_val):

    logger = get_run_logger()
    categorical = ['squareMeters']
    df_train_data = df_train[categorical]
    df_val_data = df_val[categorical]
    #we convert the columns to a dictionary
    train_dicts = df_train_data[categorical].to_dict(orient='records')
    val_dicts = df_val_data[categorical].to_dict(orient='records')
    #dictionary to vector converter
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    X_val = dv.transform(val_dicts)
    target = 'price'
    y_train = df_train[target].values
    y_val = df_val[target].values
    logger.info(f"the traing feature is {categorical} and the predicted feature is {target}")
    return X_train, X_val, y_train, y_val, dv

@task
def train_predict_model(dv, model, X_train, X_val, y_train, y_val):
     with mlflow.start_run():
    
        logger = get_run_logger()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        mean_squared_error(y_val, y_pred, squared=False)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        logger.info(f"The MSE of validation is: {rmse}")
        filename = "models/linear-reg.b"
        pickle.dump((dv, model), open(filename,'wb'))
        mlflow.log_artifact(local_path="models/linear-reg.b", artifact_path="local_models_pickle")
        mlflow.sklearn.log_model(model, artifact_path="models_mlflow")
        logger.info(f"{filename} has been successfully logged")



@flow(task_runner=SequentialTaskRunner())
def main(train_path: str="s3://mlops-project-dataset-deen/paris-housing-dataset/ParisHousing_period_01.parquet", val_path: str="s3://mlops-project-dataset-deen/paris-housing-dataset/ParisHousing_period_02.parquet"):
  
    mlflow.set_tracking_uri("sqlite:///backend.db")
    mlflow.set_experiment("my-experiment-1")
    df_train = read_dataframe(train_path)
    df_val = read_dataframe(val_path)
    X_train, X_val, y_train, y_val, dv = preparing_features(df_train, df_val)
    model = LinearRegression()
    train_predict_model(dv, model, X_train, X_val, y_train, y_val)
    logger = get_run_logger()
    logger.info("training automation is successful")
