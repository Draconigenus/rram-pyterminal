import random
import sys
import time
from ctypes import c_int8
import numpy as np

import Board.DAC
from Lib import RRAM
"""
This script has the purpose of being able to test the endurance of a section of the RRAM array through the use of
set/reset cycles.
"""

def check(addr):
    """
    Determines if the cell at addr is still responsive
    :param addr: address of the cell
    :return: true if the cell is responsive, lrs value (resistance/ADC comps), hrs (resistance/ADC comps)
    """
    #########################################
    RRAM.set(level='cell', number=str(addr), verbal=False)
    # lrs = resistance(addr, refs, VTGT)
    lrs = int( RRAM.read_lane(address=str(addr), data='0x001', verbal=False), 16)
    #########################################
    RRAM.reset(level='cell', number=str(addr), verbal=False)
    # hrs = resistance(addr, refs, VTGT)
    hrs = int( RRAM.read_lane(address=str(addr), data='0x001', verbal=False), 16)
    #########################################
    saf = lrs >= hrs
    #########################################
    return saf, lrs, hrs

def endurance(module, addr):
    """
    runs endurance testing on a specified range of cells and save to endurance.npy
    :param module: module for target cells
    :param addr: column for target cells
    :return: nothing
    """

    if module == '': module = 0
    else:            module = int(module)

    if addr == '': addr = 200
    else:          addr = int(addr)

    RRAM.module(action='set', target=str(module), verbal=False)
    RRAM.conf_read(cycle='5', verbal=False)
    cal = RRAM.adc(action='set', action_type='cal', target='0', verbal=False)
    hbias = RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(1200), cycle=str(16), times=str(10), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2800), AVDD_WL=str(2800), cycle=str(100), times=str(10), verbal=False)

    VTGT = 200
    Board.DAC.set_source(value=str(VTGT), target='VTGT_BL', verbal=False)
    # refs = references(module=module, col=addr, VTGT=VTGT)

    RRAM.conf_ADC(offset='5', step='8')

    total = int(1e3)
    #cycles between reads
    batch_size = int(1e2)
    batch_num = total // batch_size
    status = np.zeros(shape=(batch_num, 256, 3))

    start = time.time()
    for batch in range(batch_num):
        for _ in range(batch_size):
            RRAM.set(level='col', number=str(addr), verbal=False)
            RRAM.reset(level='col', number=str(addr), verbal=False)

        for row in range(256):
            address = row * 256 + addr
            status[batch][row] = check(addr=address)
            print (status[batch][row])

        duration = time.time() - start
        rate = (batch * batch_size + batch_size) / duration
        stuck = np.sum(status[batch] > 0)
        print ('switch / sec: %f | stuck devices: %d/%d' % (rate, stuck, 256))

        results = {'batch': batch, 'status': status}
        np.save('endurance', results)

##########################################################

def SAF(module):
    """
    perform stuck at fault testing on specified module
    :param module: module to test
    :return:
    """
    module = int(module)

    RRAM.module(action='set', target=str(module), verbal=False)

    #set read, set, reset parameters TODO: make set and reset voltages input
    RRAM.conf_read(cycle='5', verbal=False)
    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(1200), cycle=str(16), times=str(10), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2800), AVDD_WL=str(2800), cycle=str(100), times=str(10), verbal=False)

    #set weird adc settings to 0
    RRAM.adc(action='set', action_type='cal', target='0', verbal=False)
    RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    #set target bitline voltage 2-200mV
    Board.DAC.set_source(value="200", target='VTGT_BL', verbal=False)

    #configure ADC to have good resolution in expected range of cell voltages
    RRAM.conf_ADC(offset='5', step='8')

    #set the number of set/reset cycles
    numCycles = 1

    #set number of set/reset cycles between reads
    batchSize = 1

    #array representation of status/health of cells in module
    status = np.zeros(Shape=(256, 256))

    #start timer
    start_time = time.time()

    #cycle the module
    RRAM.set_reset(level='module', number='0', times='1', verbal=False)

    cycle_time = time.time_ns() - start_time
    #check the cells
    for row in status:
        for col in status[row]:
            address = row * 256 + col
            if status[row][col] == 0:
                status[row][col] = {}
            status['saf'], status['lrs'], status['hrs'] = check(address)
    read_time = time.time() - start_time
    results = {"module": module, "cycle time": cycle_time, "read time": read_time, "status": status}
    np.save("saf_m" + module + "_c" + numCycles, results)




def main(addr=0, nrow=1, ncol=1, ncycles=-1):
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

def decode(args):
    # opts, args = getopt.getopt(sys.argv, "t:a:s:r:c:n:", ["test=","area=","startAddress=", "nRows=", "nCols=", "nCycles="])
    if args[0] == "SAF": SAF(args[1])
