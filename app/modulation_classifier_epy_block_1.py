"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(self,
            name="selector_controller",
            in_sig=[np.int32],
            out_sig=None)
        self.message_port_register_out(gr.pmt.intern("selector_ctrl"))
        self.counter = 0

    def work(self, input_items, output_items):
        random_values = input_items[0]
        for value in random_values:
            if self.counter % 5 == 0:
                self.message_port_pub(gr.pmt.intern("selector_ctrl"), gr.pmt.from_long(value))
            self.counter += 1
        return len(input_items[0])

