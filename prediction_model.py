import numpy as np
import pandas as pd
import tensorflow as tf

# noinspection PyTypeChecker
__model:tf.keras.Model = None

def dataframe_to_dataset(df:pd.DataFrame, shuffle:bool=False)->tf.data.TFRecordDataset:
    """
    Convert pandas dataframe to TensorFlow records dataset (i.e. binary)
    :param df: Pandas dataframe
    :param shuffle: Bool indication if dataset should be shuffled
    :return: tf_records dataset
    """

    df = df.copy()
    if "duration" in df.columns:
        df = df.drop("duration",axis=1)
    labels = df.pop("y") if "y" in df.columns else [-1] * len(df)
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(df))

    ds = ds.batch(len(df)) # expand dims

    return ds

def get_model() -> tf.keras.Model:
    """
    Get model object and save globally so only needs loading once
    :return: The TensorFlow saved model (keras bundled)
    """
    global __model

    if __model is None:
        __model = tf.keras.models.load_model("simple_bank_model.model")

    return __model

def predict_liklihood(df:pd.DataFrame)->np.ndarray:
    """
    Predict liklihood for examples (1 example per row of dataframe)
    :param df: Pandas dataframe of examples
    :return: 1D array of liklihoods
    """

    model = get_model()

    input_data = dataframe_to_dataset(df)
    predictions:np.ndarray = model.predict(input_data).ravel()

    return predictions



