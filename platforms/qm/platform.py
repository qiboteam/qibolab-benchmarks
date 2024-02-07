import pathlib

from qibolab.channels import ChannelMap
from qibolab.instruments.qm import OPXplus, QMController
from qibolab.instruments.rohde_schwarz import SGS100A
from qibolab.platform import Platform
from qibolab.serialize import (
    load_instrument_settings,
    load_qubits,
    load_runcard,
    load_settings,
)

ADDRESS = "192.168.0.101:80"
TIME_OF_FLIGHT = 280
FOLDER = pathlib.Path(__file__).parent


def create():
    opx = OPXplus("con3")
    controller = QMController("qm", ADDRESS, opxs=[opx], time_of_flight=TIME_OF_FLIGHT)
    # Instantiate local oscillators
    lo_drive = SGS100A("lo_drive", "192.168.0.35")
    lo_readout = SGS100A("lo_readout", "192.168.0.36")

    # Create channel objects
    channels = ChannelMap()
    channels |= ("readout", "feedback", "drive", "twpa")
    channels["readout"].port = controller.ports((("con3", 9), ("con3", 10)))
    channels["feedback"].port = controller.ports(
        (("con3", 1), ("con3", 2)), output=False
    )
    channels["drive"].port = controller.ports((("con3", 3), ("con3", 4)))

    # Assign local oscillators to channels
    channels["readout"].local_oscillator = lo_readout
    channels["feedback"].local_oscillator = lo_readout
    channels["drive"].local_oscillator = lo_drive

    # create qubit objects
    runcard = load_runcard(FOLDER)
    qubits, couplers, pairs = load_qubits(runcard)

    # assign channels to qubit
    qubit = qubits[0]
    qubit.readout = channels["readout"]
    qubit.feedback = channels["feedback"]
    qubit.drive = channels["drive"]

    instruments = {inst.name: inst for inst in [controller, opx, lo_readout, lo_drive]}
    settings = load_settings(runcard)
    instruments = load_instrument_settings(runcard, instruments)
    return Platform("qm", qubits, pairs, instruments, settings, resonator_type="2D")
