import numpy as np
from flask import Flask, g, jsonify, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit
from model_inference import ModelInference
from utils import (
    fetch_all_signals,
    get_fft,
    get_prediction_label,
    get_signal_by_id,
    get_true_label,
    get_wavelet,
    save_signal_to_db,
    set_true_label,
)
from zeromqAdapter import ZmqAdapter

# CONST
ZEROMQ_ADDRESS = "tcp://127.0.0.1:5557"
APP_ADDRESS = "http://127.0.0.1:5000"

app = Flask(__name__)
socketio = SocketIO(app)

adapter = ZmqAdapter(ZEROMQ_ADDRESS, APP_ADDRESS)


@app.route("/start_monitoring")
def get_data():
    adapter.run()
    return jsonify({"status": "Monitoring started"}), 200


@app.route("/receive_signal", methods=["POST"])
def receive_data():
    """
    Receive data from a request, predict using a model, save the signal and prediction to a database,
    calculate FFT and wavelet transform of the signal, emit the data through a socket, and return a JSON response.

    Returns:
        tuple: A tuple containing a JSON response with status and HTTP status code.
    """
    raw_frame = request.json

    if raw_frame:
        try:
            prediction = g.model.predict(raw_frame)
        except Exception as e:
            prediction = "Unrecognized"

        save_signal_to_db(raw_frame, prediction)

        fft = get_fft(raw_frame)
        wavelet = get_wavelet(raw_frame)

        recived_data = {
            "prediction": prediction,
            "original": raw_frame,
            "fft": fft,
            "wavelet": wavelet,
            "constellation": raw_frame,
        }

        socketio.emit("new_signal", recived_data)

        return jsonify({"status": "success"}), 200
    else:
        app.logger.error("No data received.")
        return jsonify({"status": "no data"}), 400


@app.route("/set_modulation_type", methods=["POST"])
def set_modulation():
    modulation = request.form["modulation"]
    signal_id = request.form["signal_id"]

    set_true_label(modulation, signal_id)

    return redirect(url_for("index"))


@app.route("/process_loaded_file", methods=["POST"])
def process_row():
    """
    Process a row of data by retrieving the signal, computing its FFT and wavelet transform, fetching the prediction
    label and true label from the database, and returning a JSON response with the processed information.

    Returns:
        JSON: A JSON response containing the true label, signal ID, prediction label, original signal, FFT,
        wavelet transform, and constellation of the signal.
    """
    row_id = request.json["id"]
    signal = get_signal_by_id(row_id)

    fft = get_fft(signal)
    wavelet = get_wavelet(signal)
    prediction = get_prediction_label(row_id)
    true_label = get_true_label(row_id)

    return jsonify(
        true_label=true_label,
        signal_id=row_id,
        prediction=prediction,
        original=signal,
        fft=fft,
        wavelet=wavelet,
        constellation=signal,
    )


@app.before_request
def load_model():
    """
    loads model file into app memory
    """
    if "model" not in g:
        g.model = ModelInference("models/main_model.h5")


@app.route("/")
def index():
    signals = fetch_all_signals()

    return render_template("index.html", signals=signals)


if __name__ == "__main__":
    socketio.run(app)
