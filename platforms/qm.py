import pathlib

from qibolab.channels import ChannelMap
from qibolab.instruments.qm import QMOPX
from qibolab.instruments.rohde_schwarz import SGS100A
from qibolab.platform import Platform
from qibolab.serialize import load_qubits, load_runcard, load_settings

NAME = "qmopx"
ADDRESS = "192.168.0.101:80"
TIME_OF_FLIGHT = 280
RUNCARD = pathlib.Path(__file__).parent / "qm.yml"


def create(runcard_path=RUNCARD):
    controller = QMOPX(NAME, ADDRESS, time_of_flight=TIME_OF_FLIGHT)
    # Instantiate local oscillators
    lo_drive = SGS100A("lo_drive", "192.168.0.35")
    lo_readout = SGS100A("lo_readout", "192.168.0.36")

    # Create channel objects
    channels = ChannelMap()
    channels |= ("readout", "feedback", "drive", "twpa")
    channels["readout"].port = controller[(("con3", 9), ("con3", 10))]
    channels["feedback"].port = controller[(("con3", 1), ("con3", 2))]
    channels["drive"].port = controller[(("con3", 3), ("con3", 4))]

    # add gain to feedback channels
    # channels["feedback"].gain = 15

    # Configure local oscillator's frequency and power
    lo_readout.frequency = 5_000_000_000
    lo_readout.power = 18
    lo_drive.frequency = 3_900_000_000
    lo_drive.power = 18

    # Assign local oscillators to channels
    channels["readout"].local_oscillator = lo_readout
    channels["feedback"].local_oscillator = lo_readout
    channels["drive"].local_oscillator = lo_drive

    # create qubit objects
    runcard = load_runcard(runcard_path)
    qubits, pairs = load_qubits(runcard)

    # assign channels to qubit
    qubit = qubits[0]
    qubit.readout = channels["readout"]
    qubit.feedback = channels["feedback"]
    qubit.drive = channels["drive"]

    instruments = {inst.name: inst for inst in [controller, lo_readout, lo_drive]}
    settings = load_settings(runcard)
    return Platform("qm", qubits, pairs, instruments, settings, resonator_type="2D")
