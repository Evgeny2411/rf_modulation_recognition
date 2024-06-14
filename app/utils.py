import datetime
import sqlite3
from pathlib import Path

import numpy as np
import pywt

DATABASE = "signals.db"

SIGNALS_FOLDER = Path(__file__).parent / "iq_signals"


def set_true_label(modulation, signal_id):
    """
    Update or insert the true label for a given signal ID in the True_labels table.

    Parameters:
    modulation (str): The true label to be set for the signal.
    signal_id (int): The ID of the signal for which the true label is to be set.

    Returns:
    None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM True_labels WHERE signal_id = ?",
        (signal_id,),
    )
    record = cursor.fetchone()

    if record:
        cursor.execute(
            "UPDATE True_labels SET true_label = ? WHERE signal_id = ?",
            (modulation, signal_id),
        )
    else:
        cursor.execute(
            "INSERT INTO True_labels (true_label, signal_id) VALUES (?, ?)",
            (modulation, signal_id),
        )

    conn.commit()
    conn.close()


def get_signal_by_id(row_id):
    """
    Retrieve a signal from the database based on the provided row ID.

    Parameters:
    - row_id (int): The ID of the row in the database from which to retrieve the signal.

    Returns:
    - list: A list of float values representing the signal.

    Raises:
    - NoSignalFoundError: If no signal is found for the given row ID.
    - DatabaseConnectionError: If there is an issue connecting to the database.
    - SignalLoadingError: If there is an issue loading the signal data from the file.
    """
    with get_db_connection() as conn:
        if conn is None:
            raise Exception("Error connecting to the database.")

        signal = conn.execute(
            "SELECT filename FROM Signals WHERE id = ?", (row_id,)
        ).fetchone()

        if signal is None:
            raise Exception("No signal found for the given row ID")

        filepath = f"{signal[0]}"
        if not Path(filepath).is_file():
            raise Exception("Signal file does not exist.")
        return np.load(filepath).astype(float).tolist()


def fetch_all_signals():
    """
    Fetches all signals from the database.

    Returns:
        list: A list of tuples containing the id and filename of each signal.
    """
    with get_db_connection() as conn:
        query = "SELECT id, filename FROM Signals"
        try:
            signals = conn.execute(query).fetchall()
        except Exception as e:
            print(f"Error occurred: {e}")
            signals = []
    return signals


DEFAULT_LABEL = "Unrecognized"


def get_true_label(row_id: int) -> str:
    """
    Get the true label for a given row ID from the database.

    Parameters:
    - row_id (int): The ID of the row for which the true label is to be fetched.

    Returns:
    - str: The true label corresponding to the given row ID. If the true label is not found in the database, returns the DEFAULT_LABEL.

    Raises:
    - sqlite3.Error: If an error occurs while fetching the true label from the database.

    Example:
    get_true_label(1)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT true_label FROM True_labels WHERE signal_id = ?",
                (row_id,),
            )
            record = cursor.fetchone()

            if record:
                return record[0]
            else:
                return DEFAULT_LABEL
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        return "Error occurred while fetching true label"


def save_signal_to_db(signal, prediction):
    """
    Save a signal and its prediction to the database.

    Parameters:
    - signal: numpy array, the signal data to be saved
    - prediction: int, the prediction associated with the signal

    Returns:
    None
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        current_datetime = datetime.datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H_%M_%S")

        observation_name = (
            SIGNALS_FOLDER / f"observation_{current_date}_{current_time}.npy"
        )

        try:
            cursor.execute(
                "INSERT INTO Signals (filename) VALUES (?)",
                (str(observation_name),),
            )
            signal_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO Model_predictions (signal_id, prediction) VALUES (?, ?)",
                (signal_id, prediction),
            )
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    np.save(observation_name, signal)


def get_prediction_label(row_id: int) -> str:
    """
    Get the prediction label for a given row ID from the Model_predictions table.

    Parameters:
    row_id (int): The ID of the row for which the prediction label is requested.

    Returns:
    str: The prediction label associated with the given row ID. Returns 'Unrecognized' if no record is found or 'Error occurred while fetching prediction label' in case of an exception.

    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT prediction FROM Model_predictions WHERE signal_id = ?",
                (row_id,),
            )
            record = cursor.fetchone()

            if record:
                return record[0]
            else:
                return DEFAULT_LABEL
        except Exception as e:
            print(f"Error: {e}")
            return "Error occurred while fetching prediction label"


def get_fft(data):
    """
    Calculate the Fast Fourier Transform (FFT) of a one-dimensional array-like input data.

    Parameters:
        data (array-like): The input data for which FFT needs to be calculated.

    Returns:
        list: A list of real values representing the FFT of the input data.

    Raises:
        ValueError: If the input data is not a one-dimensional array-like structure.

    Note:
        This function uses numpy's FFT implementation to calculate the FFT of the input data.
    """
    try:
        fft = np.fft.fft(np.asarray(data))
        return fft.real.tolist()

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_wavelet(data):
    """
    Calculate the power spectrum of a given data using wavelet decomposition.

    Parameters:
    - data (array-like): Input data to perform wavelet decomposition.

    Returns:
    - power_spectrum (array): Power spectrum of the input data after wavelet decomposition.

    If an error occurs during the process, None is returned.
    """
    try:
        wavelet = pywt.wavedec(data, "db1")
        power_spectrum = [
            [float(val) for val in np.abs(coeff.flatten()) ** 2] for coeff in wavelet
        ]
        return power_spectrum
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn
