# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import pandas as pd 
import numpy as np
# For feature scaling
from sklearn import preprocessing as pp


def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw or
        ../interim) into cleaned data ready to be analyzed (saved in 
        ../processed or ../interim).
    """
    logger = logging.getLogger(__name__)
    logger.info('building features...')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
