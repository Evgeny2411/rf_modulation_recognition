import numpy as np
from flask import Flask, g, jsonify, redirect, render_template, request, url_for
from model_inference import ModelInference
from utils import (
    get_all_signals,
    get_fft,
    get_signal_by_id,
    get_true_label,
    get_wavelet,
    set_true_label,
)
from zeromqAdapter import ZmqAdapter

# CONST
ALLOWED_VALUES = [
    "32PSK",
    "16APSK",
    "32QAM",
    "FM",
    "GMSK",
    "32APSK",
    "OQPSK",
    "8ASK",
    "Unrecognized",
]

ZEROMQ_ADDRESS = "tcp://127.0.0.1:5557"
APP_ADDRESS = "http://127.0.0.1:5000"

app = Flask(__name__)

adapter = ZmqAdapter(ZEROMQ_ADDRESS, APP_ADDRESS)


@app.route("/start_monitoring")
def get_data():
    adapter.run()
    return jsonify({"status": "Monitoring started"}), 200

@app.route("/recieve_signal", methods=['POST'])
def recieve_data():
    raw_frame = request.json

    fft = get_fft(raw_frame)
    wavelet = get_wavelet(raw_frame)
    prediction = g.model.predict(raw_frame)
    return jsonify(
        prediction=prediction,
        original=raw_frame,
        fft=fft,
        wavelet=wavelet,
        constellation=raw_frame,
    )


@app.route("/set_modulation_type", methods=["POST"])
def set_modulation():
    modulation = request.form["modulation"]
    signal_id = request.form["signal_id"]

    set_true_label(modulation, signal_id)

    return redirect(url_for("index"))


@app.route("/process_loaded_file", methods=["POST"])
def process_row():
    row_id = request.json["id"]
    signal = get_signal_by_id(row_id)

    fft = get_fft(signal)
    wavelet = get_wavelet(signal)
    prediction = g.model.predict(signal)
    true_label = get_true_label(row_id)

    return jsonify(
        true_label=true_label,
        signal_id=row_id,
        prediction=prediction,
        original=signal.astype(float).tolist(),
        fft=fft.astype(float).tolist(),
        wavelet=wavelet,
        constellation=signal.astype(float).tolist(),
    )


@app.before_request
def load_model():
    if "model" not in g:
        g.model = ModelInference("models/model.h5")


@app.route("/")
def index():
    # recieved_signal = receive_data()
    signals = get_all_signals()

    return render_template("index.html", signals=signals)


if __name__ == "__main__":
    app.run(debug=True)
