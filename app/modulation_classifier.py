#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulation_classifier
# Author: Yevhenii Borysenko
# Description: Generator radiosignals for diploma project
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import modulation_classifier_epy_block_0 as epy_block_0  # embedded python block



class modulation_classifier(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Modulation_classifier", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulation_classifier")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "modulation_classifier")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1024000
        self.QAM32 = QAM32 = digital.constellation_16qam().base()
        self.QAM32.set_npwr(1.0)
        self.APSK32 = APSK32 = digital.constellation_qpsk().base()
        self.APSK32.set_npwr(1.0)
        self.APSK16 = APSK16 = digital.constellation_qpsk().base()
        self.APSK16.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://*:5557', 100, False, (-1), '', True, True)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=2,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.epy_block_0 = epy_block_0.blk(example_param=1.0)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=32,
            mod_code="none",
            differential=True,
            samples_per_symbol=2,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=2,
            bt=0.35,
            verbose=False,
            log=False,
            do_unpack=True)
        self.digital_constellation_modulator_2 = digital.generic_mod(
            constellation=QAM32,
            differential=True,
            samples_per_symbol=2,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_modulator_1 = digital.generic_mod(
            constellation=APSK16,
            differential=True,
            samples_per_symbol=2,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=APSK32,
            differential=True,
            samples_per_symbol=2,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc([1+1j, 1-1j, -1+1j, -1-1j], 2)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(1)
        self.blocks_throttle2_0_4_1 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_4_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_4 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_3 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "items" == "auto" else max( int(float(1024) * samp_rate) if "items" == "time" else int(1024), 1) )
        self.blocks_throttle2_0_2_1 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_2 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_1 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_head_0_3_1 = blocks.head(gr.sizeof_gr_complex*1, 1024000)
        self.blocks_head_0_3_0 = blocks.head(gr.sizeof_gr_complex*1, 1024000)
        self.blocks_head_0_3 = blocks.head(gr.sizeof_gr_complex*1, 1024000)
        self.blocks_head_0_1 = blocks.head(gr.sizeof_gr_complex*1, 1024000)
        self.blocks_head_0_0 = blocks.head(gr.sizeof_gr_complex*1, 1024000)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 1024000)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_random_source_x_0_0 = blocks.vector_source_i(list(map(int, numpy.random.randint(0, 7, 1024))), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1024))), False)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_throttle2_0_1, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_1, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_2, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_selector_0, 7))
        self.connect((self.blocks_head_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_head_0_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_head_0_1, 0), (self.blocks_selector_0, 6))
        self.connect((self.blocks_head_0_3, 0), (self.blocks_selector_0, 4))
        self.connect((self.blocks_head_0_3_0, 0), (self.blocks_selector_0, 5))
        self.connect((self.blocks_head_0_3_1, 0), (self.blocks_selector_0, 3))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_throttle2_0_3, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_throttle2_0_2, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_head_0_0, 0))
        self.connect((self.blocks_throttle2_0_1, 0), (self.blocks_head_0_1, 0))
        self.connect((self.blocks_throttle2_0_2, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_throttle2_0_2_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_throttle2_0_3, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_throttle2_0_4, 0), (self.blocks_head_0_3, 0))
        self.connect((self.blocks_throttle2_0_4_0, 0), (self.blocks_head_0_3_0, 0))
        self.connect((self.blocks_throttle2_0_4_1, 0), (self.blocks_head_0_3_1, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle2_0_4_0, 0))
        self.connect((self.digital_constellation_modulator_1, 0), (self.blocks_throttle2_0_4, 0))
        self.connect((self.digital_constellation_modulator_2, 0), (self.blocks_throttle2_0_4_1, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_throttle2_0_2_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_stream_mux_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "modulation_classifier")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_2.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_2_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_3.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_4.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_4_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_0_4_1.set_sample_rate(self.samp_rate)

    def get_QAM32(self):
        return self.QAM32

    def set_QAM32(self, QAM32):
        self.QAM32 = QAM32

    def get_APSK32(self):
        return self.APSK32

    def set_APSK32(self, APSK32):
        self.APSK32 = APSK32

    def get_APSK16(self):
        return self.APSK16

    def set_APSK16(self, APSK16):
        self.APSK16 = APSK16




def main(top_block_cls=modulation_classifier, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
