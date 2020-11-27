#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2020 Theo Hussey
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Leds
    ("user_led", 0, Pins("W13"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("W14"), IOStandard("LVCMOS33")),
]

_ps7_io = [
    # PS7
    ("ps7_clk",   0, Pins(1)),
    ("ps7_porb",  0, Pins(1)),
    ("ps7_srstb", 0, Pins(1)),
    ("ps7_mio",   0, Pins(54)),
    ("ps7_ddram", 0,
        Subsignal("addr",    Pins(15)),
        Subsignal("ba",      Pins(3)),
        Subsignal("cas_n",   Pins(1)),
        Subsignal("ck_n",    Pins(1)),
        Subsignal("ck_p",    Pins(1)),
        Subsignal("cke",     Pins(1)),
        Subsignal("cs_n",    Pins(1)),
        Subsignal("dm",      Pins(4)),
        Subsignal("dq",      Pins(32)),
        Subsignal("dqs_n",   Pins(4)),
        Subsignal("dqs_p",   Pins(4)),
        Subsignal("odt",     Pins(1)),
        Subsignal("ras_n",   Pins(1)),
        Subsignal("reset_n", Pins(1)),
        Subsignal("we_n",    Pins(1)),
        Subsignal("vrn",     Pins(1)),
        Subsignal("vrp",     Pins(1)),
    ),
]

# _usb_uart_pmod_io = [
#     # USB-UART PMOD on JB:
#     # - https://store.digilentinc.com/pmod-usbuart-usb-to-uart-interface/
#     ("usb_uart", 0,
#         Subsignal("tx", Pins("pmodb:1")),
#         Subsignal("rx", Pins("pmodb:2")),
#         IOStandard("LVCMOS33")
#     ),
# ]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("data1", "A20 H16 B19 B20 C20 H17 D20 D18 H18 D19 F20 E19 F19 K17"),
    # ("data2", "T20 U20 V20 W20 Y18 Y19 W18 W19"),
    # ("data3", "V15 W15 T11 T10 W14 Y14 T12 U12"),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk125"
    default_clk_period = 1e9/125e6

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7z010-clg400-1", _io,  _connectors, toolchain="vivado")
        self.add_extension(_ps7_io)
        # self.add_extension(_usb_uart_pmod_io)

    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk125", loose=True), 1e9/125e6)
