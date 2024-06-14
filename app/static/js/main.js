
$(document).ready(function () {
    var selectedRowId = null;
    $('tr[data-id]').click(function () {
        $('tr[data-id]').removeClass('active');
        $(this).addClass('active');
        selectedRowId = $(this).data('id');
    });

    $('#load-file').click(function () {
        if (selectedRowId !== null) {
            $.ajax({
                url: '/process_loaded_file',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ id: selectedRowId }),
                success: function (response) {
                    plotIQTimeDomain(response.original, 'original', 'Original Data');
                    plotFFT(response.fft, 'fft', 'FFT Data');
                    plotSpectrogram(response.wavelet, 'wavelet', 'Wavelet Data');
                    plotConstellation(response.constellation, 'constellation', 'Constellation Data');
                    $('#id_field').val(response.signal_id);
                    document.querySelector('h3.model-prediction').textContent = 'Model prediction of modulation: ' + response.prediction;
                    document.querySelector('h3.true-label').textContent = 'Setted True Label of modulation: ' + response.true_label;
                    selectedRowId = null;
                    $('tr[data-id]').removeClass('active');
                    document.querySelector('.plot-grid').classList.remove('hidden');
                },
                error: function (error) {
                    console.log('Error:', error);
                }
            });
        } else {
            alert('Please select a row before submitting.');
        }
    });
});

function startMonitoring() {
    $.ajax({
        url: '/start_monitoring',
        method: 'GET',
        success: function (response) {
            console.log('Monitoring process initiated successfully');
            fetch_data();
        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
}
document.addEventListener('DOMContentLoaded', (event) => {
    var button = document.querySelector('.button-fancy');

    button.addEventListener('click', function () {
        this.classList.add('active');
    });
});

var socket = io();


socket.on('new_signal', function (data) {
    plotIQTimeDomain(data.original, 'original', 'Original Data');
    plotFFT(data.fft, 'fft', 'FFT Data');
    plotSpectrogram(data.wavelet, 'wavelet', 'Wavelet Data');
    plotConstellation(data.constellation, 'constellation', 'Constellation Data');
    document.querySelector('.plot-grid').classList.remove('hidden');
    document.querySelector('.button-fancy').classList.remove('active');
    document.querySelector('h3.model-prediction').textContent = 'Model prediction of modulation: ' + data.prediction;
    document.querySelector('h3.true-label').textContent = 'Setted True Label of modulation: Empty';
});

function plotConstellation(data, divId, title) {
    var I = data.map(function (value) { return value[0]; });
    var Q = data.map(function (value) { return value[1]; });

    var trace = {
        x: I,
        y: Q,
        mode: 'markers',
        type: 'scatter',
        marker: { size: 6, color: 'blue' }
    };

    var layout = {
        title: title,
        xaxis: {
            title: 'In-Phase'
        },
        yaxis: {
            title: 'Quadrature'
        },
        autosize: false,
        width: 500,
        height: 500,
        showlegend: false
    };

    Plotly.newPlot(divId, [trace], layout);
}
function plotSpectrogram(data, divId, title) {
    var z = data;
    var x = Array.from({ length: data[0].length }, (_, i) => i + 1);
    var y = Array.from({ length: data.length }, (_, i) => i + 1);

    var trace = {
        x: x,
        y: y,
        z: z,
        type: 'heatmap',
        colorscale: 'Jet'
    };

    var layout = {
        title: title,
        xaxis: {
            title: 'Time'
        },
        yaxis: {
            title: 'Frequency'
        }
    };

    Plotly.newPlot(divId, [trace], layout);
}
function plotFFT(data, divId, title) {
    var magnitude = data.map(function (value) { return Math.sqrt(value[0] * value[0] + value[1] * value[1]); });
    var frequency = Array.from({ length: data.length }, (_, i) => i + 1);

    var trace = {
        x: frequency,
        y: magnitude,
        mode: 'lines',
        name: 'Magnitude',
        line: {
            color: 'blue',
            width: 2
        }
    };

    var layout = {
        title: title,
        xaxis: {
            title: 'Frequency'
        },
        yaxis: {
            title: 'Magnitude'
        }
    };

    Plotly.newPlot(divId, [trace], layout);
}
function plotIQTimeDomain(data, divId, title) {
    var I = data.map(function (value) { return value[0]; });
    var Q = data.map(function (value) { return value[1]; });
    var time = Array.from({ length: data.length }, (_, i) => i + 1);

    var traceI = {
        x: time,
        y: I,
        mode: 'lines',
        name: 'In-Phase',
        line: {
            color: 'blue',
            width: 2
        }
    };

    var traceQ = {
        x: time,
        y: Q,
        mode: 'lines',
        name: 'Quadrature',
        line: {
            color: 'red',
            width: 2
        }
    };

    var layout = {
        title: title,
        xaxis: {
            title: 'Time'
        },
        yaxis: {
            title: 'Amplitude'
        }
    };

    Plotly.newPlot(divId, [traceI, traceQ], layout);
}