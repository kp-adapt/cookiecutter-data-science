import os
import pathlib
import pickle
import logging
from sqlalchemy import create_engine
import urllib.parse as urllib
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sacred import Experiment
from room_of_requirement.ml import SqlObserver


project_dir = pathlib.Path('.').resolve()
load_dotenv(str(project_dir / '.env'))

params = f"""
    Driver={os.getenv("DRIVER")};
    Server={os.getenv("SERVER")};
    Database={os.getenv("DATABASE")};
    Uid={os.getenv("USER")};
    Pwd={os.getenv("PASSWORD")};
    """
db_params = urllib.quote_plus(params)
dev_conn = f"mssql+pyodbc:///?odbc_connect={db_params}"

# Create and experiment object (optionally naming it) and add SQL observer.
ex = Experiment("train_model")
ex.observers.append(SqlObserver(dev_conn))


@ex.config
def config():
    """Add variables to experiment such as parameters and filepaths.

    Any function that is defined BELOW this function in the script and that uses
    the @ex.capture decorator will allow you to share the variables defined in 
    this functions namespace as function parameters.

    Read more here: https://sacred.readthedocs.io/en/stable/configuration.html
    """
    MODEL_PATH = str(project_dir / 'your_path')
    DATA_PATH = str(project_dir / 'your_path')

    # Don't include a return or yield statement!


@ex.capture
def train_model(MODEL_PATH: str, DATA_PATH: str):
    """Conduct a computational experiment and save the resulting artifacts to db.

    A function that captures (notice @ex.capture decorator) the configuration 
    variables for use in an experiment run. Load data (or call functions that load
    your data) and save as a resource, train models and save as an artifact. Log
    results. The second link below has more on adding resources and artifacts.

    Read more here: https://sacred.readthedocs.io/en/stable/experiment.html#capture-functions
    Read more here: https://sacred.readthedocs.io/en/stable/collected_information.html?highlight=artifacts#resources-and-artifacts
    """
    logger = logging.getLogger(__name__)
    logger.info('Loading data and adding resource...')

    ex.add_resource(DATA_PATH)
    with open(DATA_PATH, 'rb') as f:
        df = pickle.load(f)

    logger.info('Scaling data...')
    scaler = StandardScaler()
    data = scaler.fit_transform(df)

    logger.info('Splitting data...')

    y = data[:, 14:]
    X = data[:, :14]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

    logger.info('training model...')

    model = "your model instance goes here."
    model.fit(X_train, y_train)

    logger.info('Recording model scores...')

    train_mse = model.score(X_train, y_train)
    test_mse = model.score(X_test, y_test)

    ex.log_scalar(name='add_your_metric_name_here', value=train_mse)
    ex.log_scalar(name='add_your_metric_name_here', value=test_mse)

    # Pickle and store resulting python object (model, grid search object, etc.).
    logger.info(f'Pickling model to: {MODEL_PATH}')
    pickle.dump(model, open(MODEL_PATH, 'wb'))

    logger.info('Adding model as artifact...')
    ex.add_artifact(MODEL_PATH)


@ex.automain
def main():
    """Main function that runs the experiment using @ex.automain decorator.
    
    Read more here: https://sacred.readthedocs.io/en/stable/experiment.html
    """
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    train_model()
