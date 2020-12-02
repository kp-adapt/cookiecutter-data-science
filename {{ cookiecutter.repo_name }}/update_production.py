"""A script for updating production models and maintaining versioning records.

Database credentials and model parameters are fetched from the .env file. The 
execute function runs validations to make sure the parameters are sending real
artifacts and valid versions to the db tables. An insert is made to the 
ml_model_version table, which holds a history of all versions of all models. A
delete is optionally made on the ml_production_models table for the last 
production model and an insert is made with the new one. The parameters are an
important driver of that process. Below are some parameter specific notes:
    - artifact_id refers to the artifact table column
    - project_name refers to the Adapt team project and model_name is intended 
      to stay the same across versions for that same modelling task within that
      project (i.e. this becomes useful in the case of multiple modelling tasks
      within a single project). 
    - github_repo refers to the ml specific repository where the model was 
      trained.
 """
import os
import pathlib
from sqlalchemy import create_engine
import urllib.parse as urllib
from dotenv import load_dotenv
import pandas as pd


def validate_artifact_exists(conn, artifact_id: int) -> bool:
    """Verify the artifact exists in the artifact table."""
    query = f"""SELECT * FROM dbo.artifact WHERE artifact_id = {artifact_id};"""
    df = pd.read_sql(query, conn)

    if df.empty:
        return True

    else: 
        return False


def validate_artifact_status(conn, artifact_id: int, project_name: str) -> bool:
    """A function to check whether the artifact is currently in production."""
    query = f"""SELECT p.* FROM dbo.ml_production_models AS p
                LEFT JOIN dbo.ml_model_versions AS v ON v.version_id = p.version_id 
                WHERE v.artifact_id = {artifact_id} 
                AND p.project_name = '{project_name}';"""
    df = pd.read_sql(query, conn)

    if df.empty:
        return False

    else:
        return True


def validate_version(conn, model_name: str, version: str, project_name: str) -> bool:
    """A function to check whether the input version is already in use."""
    query = f"""SELECT v.version FROM dbo.ml_model_versions as v
              JOIN dbo.ml_production_models AS p ON p.version_id = v.version_id
              WHERE p.model_name = '{model_name}' AND p.project_name = '{project_name}';"""
    df = pd.read_sql(query, conn)

    if df.empty:
        return False

    elif version == df.iloc[0,0]:
        return True

    else:
        return False


def execute(engine: object, artifact_id: int, version: str, project_name: str, 
            commit_id: str, model_name: str, model_type: str = None, 
            github_repo: str = None, replace_latest: bool = True) -> None:
    """Updates ml production and version tables with new model version.

    The function first checks to see whether the artifact has been deployed to 
    production in that project already, and if so, raises and error. Then it
    replaces the most recent version in the production table with the new input
    version. It also updates the version table to reflect the change.
    
    Parameters
    ----------
        engine : object
            A sqlalchemy engine object.

        artifact_id : int
            The sacred unique identifier for the production-ready model.

        version : str
            The new version string of the model.

        project_name : str
            The name of the project to deploy the model to.

        commit_id : str
            The github commit hash that contains corresponding support code to 
            deploy the production-ready model.

        model_name : str
            The name of the production-ready model.

        model_type : str {default: None}
            The type of model that was trained (i.e. the algorithm used).

        github_repo : str {default: None}
            The name of the github repository that the production-ready model is 
            associated to.

        replace_latest : bool {default: True}
            A flag to control production model replacement behavior.
            
    Notes
    -----
        replace_latest should almost always be set to True except in times when 
        a test is being run on multiple versions of the same model for the same
        project (i.e. a production run A/B test). As of the writing of this, that
        should be extremely rare.
    
    """
    with engine.connect() as conn:

        if validate_artifact_exists(conn, artifact_id):
            raise ValueError('The passed artifact_id relates to no known artifact. Expected a valid id.')

        if validate_artifact_status(conn, artifact_id, project_name):
            raise ValueError('The artifact_id is already in production. Expected a new artifact.')

        if validate_version(conn, model_name, version, project_name):
            raise ValueError('The version_id is already in use. Expected a new version_id.')

        # If replace_latest, delete most recent entry for the project in prod table
        if replace_latest:
            stmt = f"""DELETE FROM dbo.ml_production_models
                WHERE version_id = (
                    SELECT TOP 1 p.version_id FROM dbo.ml_production_models AS p 
                    JOIN dbo.ml_model_versions AS v ON p.version_id = v.version_id
                    WHERE p.project_name = '{project_name}' 
                    AND p.model_name = '{model_name}'
                    ORDER BY v.timestamp DESC
                );"""
            conn.execute(stmt)

        # Create a version entry
        insert = f"""INSERT INTO dbo.ml_model_versions (version, commit_id, artifact_id, timestamp)
            VALUES ('{version}', '{commit_id}', {artifact_id}, GETDATE());"""
        conn.execute(insert)

        # Retrieve version_id
        query = f"""SELECT version_id FROM dbo.ml_model_versions 
            WHERE version = '{version}' AND commit_id = '{commit_id}';"""
        version_id = conn.execute(query).fetchall()[0][0]

        # Create a production entry
        insert = f"""INSERT INTO dbo.ml_production_models (version_id,
            project_name, model_name, model_type, github_repo) 
            VALUES ({version_id}, '{project_name}', '{model_name}', 
            '{model_type}', '{github_repo}');"""
        conn.execute(insert)


if __name__ == '__main__':
    project_dir = pathlib.Path('.').resolve()
    load_dotenv(str(project_dir / '.env'))

    params = f"""
        Driver={os.getenv("DRIVER")};
        Server={os.getenv("SERVER")};
        Database={os.getenv("DATABASE")};
        Uid={os.getenv("USER")};
        Pwd={os.getenv("PASSWORD")};
        """

    # Gather SQL credentials and create db connection object
    db_params = urllib.quote_plus(params)
    db_url = f"mssql+pyodbc:///?odbc_connect={db_params}"
    engine = create_engine(db_url, fast_executemany=True)

    # Retrieve version parameters from .env
    new_version = {
        'artifact_id': os.getenv("ARTIFACT_ID"),
        'version': os.getenv("VERSION"),
        'project_name': os.getenv("PROJECT_NAME"),
        'model_name': os.getenv("MODEL_NAME"),
        'model_type': os.getenv("MODEL_TYPE"),
        'github_repo': os.getenv("GITHUB_REPO"),
        'commit_id': os.getenv("COMMIT_ID")
    }
    replace_last = os.getenv("REPLACE_LAST")

    execute(engine, replace_latest=replace_last, **new_version)