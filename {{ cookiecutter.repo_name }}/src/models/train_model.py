# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# For GridSearchCV and RandomSearchCV
from sklearn import model_selection as ms
# For modeling
from sklearn import linear_model as lm
from sklearn import ensemble as ens
# For scoring
from sklearn import metrics

import sacred
ex = sacred.Experiment()


@ex.main
def main(input_filepath, output_filepath):
    """ Runs training scripts to train models and
    search hyperparameter space to optimize. Sacred
    is also featured for experiment versioning and documentation
    support
    """
    logger = logging.getLogger(__name__)
    logger.info('training model...')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    ex.run()
