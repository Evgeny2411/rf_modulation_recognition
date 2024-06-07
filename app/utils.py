import sqlite3

import numpy as np
import pywt

DATABASE = "signals.db"


def set_true_label(modulation, signal_id):
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
    conn = get_db_connection()
    signal = conn.execute(
        "SELECT filename FROM Signals WHERE id = ?", (row_id,)
    ).fetchone()

    filepath = f"{signal[0]}"
    return np.load(filepath)


def get_all_signals():
    conn = get_db_connection()
    signals = conn.execute("SELECT id, filename FROM Signals").fetchall()
    conn.close()
    return signals


def get_true_label(row_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT true_label FROM True_labels WHERE signal_id = ?",
        (row_id,),
    )
    record = cursor.fetchone()

    if record:
        return record[0]
    else:
        return "Unrecognized"


def get_fft(data):
    fft = np.fft.fft(data)
    return fft


def get_wavelet(data):
    wavelet = pywt.wavedec(data, "db1")
    power_spectrum = [
        [float(val) for val in np.abs(coeff.flatten()) ** 2] for coeff in wavelet
    ]
    return power_spectrum


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    # conn.row_factory = sqlite3.Row
    return conn
