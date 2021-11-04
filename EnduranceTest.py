import sys
import getopt
from PyTerminal import PyTerminal
"""
This script has the purpose of being able to test the endurance of a section of the RRAM array through the use of
set/reset cycles.
"""


def main(pyterminal, addr=0, nrow=1, ncol=1, ncycles=-1):
    """
    Main method for performing endurance testing.

    :param pyterminal: input pyterminal object connected to the RRAM test board
    :type pyterminal: PyTerminal
    :param addr: starting address to test endurance on [0, last address in RRAM array] #TODO: any way to see this information with status?
    :type addr: int
    :param nrow: number of rows after starting address to endurance test [1, number of remaining rows in RRAM array]
    :param ncol: number of columns after starting address to endurance test [1, number of remaining columns in RRAM array]
    :param ncycles: number of times to perform set/reset operations, -1 for infinite otherwise [1, inf)
    """

def decode(pyterminal, args):
    opts, args = getopt.getopt(sys.argv, "s:r:c:n:", ["startAddress=", "nRows=", "nCols=", "nCycles="])