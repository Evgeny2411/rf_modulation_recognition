from tensorflow.keras.models import load_model
import numpy as np

class ModelInference:

    classes = ["32PSK","16APSK","32QAM","FM","GMSK","32APSK","OQPSK","8ASK"]
    threshold = 0.65

    def __init__(self, model_path):
        self.model = load_model(model_path)
        

    def transform_input(self, signal):

        i_data = signal[:, 0]
        q_data = signal[:, 1]
        complex_data = i_data + 1j*q_data

        amplitude = np.abs(complex_data)
        phase = np.angle(complex_data)

        amplitude_phase = np.stack((amplitude, phase), axis=-1)

        return (np.expand_dims(signal, axis=0), np.expand_dims(amplitude_phase, axis=0))


    def predict(self, X):

        prediction = self.model.predict(self.transform_input(X), verbose = 0)
        maximum = np.max(prediction)

        if maximum > self.threshold:
            return self.classes[np.argmax(prediction)]
        else:
            return "Unrecodnized"
