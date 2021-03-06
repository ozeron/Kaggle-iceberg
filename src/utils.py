import pandas as pd
import numpy as np
from os import path
import pickle

PROJECT_HOME = path.normpath(path.join(__file__, '../..'))
BAND_1 = 'band_1'
BAND_2 = 'band_2'

HEIGHT = 75
WIDTH = 75


def load_dataframe(mode):
    file_path = path.join(PROJECT_HOME, 'data', mode, 'data.json')
    return pd.read_json(file_path)

def transform_dataset(df):
    X_band_1 = np.array([np.array(band).astype(np.float32).reshape(HEIGHT, WIDTH) for band in df[BAND_1]])
    X_band_2 = np.array([np.array(band).astype(np.float32).reshape(HEIGHT, WIDTH) for band in df[BAND_2]])
    return np.concatenate([X_band_1[:, np.newaxis, :, :],
                           X_band_2[:, np.newaxis, :, :],
                          ],axis=1)

def save_submission(source, predicted, filename='sub.csv'):
    submission = pd.DataFrame()
    submission['id'] = source['id']
    submission['is_iceberg'] = predicted.reshape((predicted.shape[0]))
    submission.to_csv(filename, index=False)
    return submission

def save_history(history, model_name):
    with open(history_object_path(model_name), 'wb') as file:
        pickle.dump(history, file)

def open_history(name):
    with open(history_object_path(name), 'rb') as f:
        return pickle.load(f)

def history_object_path(name):
    filename = '%s_history.pckl' % name
    return path.normpath(path.join(PROJECT_HOME, 'history', filename))

def n_random(array, size=5):
    indexes = np.random.choice(np.arange(array.shape[0]), size)
    return array[indexes]
