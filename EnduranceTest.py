import random
import sys
import time
from ctypes import c_int8
import numpy as np
import argparse
import resistance

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
    dead = lrs >= hrs
    #########################################
    return dead, lrs, hrs

def endurance(module, col, stop = 1000000, batch_size = 5000, form_settings=None, set_settings = [2200, 1200, 16, 10], reset_settings = [2800, 2800, 100, 10]):
    """
    perform endurance testing on specified module
    :param module: module to test
    :param stop: total number of R/W cycles to perform on module
    :param batch_size: number of S/R cycles in between reads
    :param form_settings: form settings in [AVDD_WR, AVDD_WL, cycle, times]
    :param set_settings: set settings in [AVDD_WR, AVDD_WL, cycle, times]
    :param reset_settings: reset settings in [AVDD_WR, AVDD_WL, cycle, times]
    :return: nothing, saved to npy file
    """

    RRAM.module(action='set', target=str(module), verbal=False)

    if form_settings != None:
        RRAM.conf_form(*[str(param) for param in form_settings])
        RRAM.form(level='module', number='0', verbal=False)

    #set read, set, reset parameters
    RRAM.conf_read(cycle='5', verbal=False)
    RRAM.conf_set(*[str(param) for param in set_settings])
    RRAM.conf_reset(*[str(param) for param in reset_settings])

    # configure ADC
    RRAM.conf_ADC(offset=str(10), step=str(10), comp='0x7FFF', verbal=False)

    #set weird adc settings to 0
    RRAM.adc(action='set', action_type='cal', target='0', verbal=False)
    RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    #set target bitline voltage 2-200mV
    Board.DAC.set_source(value="200", target='VTGT_BL', verbal=False)

    #holds cell responsiveness data in cycle: status form
    cell_data = {}

    results = {"module": module, "status": cell_data,
               "form_settings": form_settings}

    np.save("Data/end_m" + str(module) + "_c" + str(stop), results)

    #cycle the module

    num_cycle = 0

    start_time = time.time()

    while num_cycle < stop:
        for _ in range(batch_size):
            RRAM.set(level='col', number=str(col), verbal=False)
            RRAM.reset(level='col', number=str(col), verbal=False)
        num_cycle += batch_size
        status = np.ndarray(shape=(256, 256), dtype=dict)
        # check the cells
        num_failed=0
        for row in range(len(status)):
            address = row * 256 + col
            if status[row][col] == None:
                status[row][col] = dict()
            status[row][col]['dead'], status[row][col]['lrs'], status[row][col]['hrs'] = check(address)
            if status[row][col]['dead']:
                num_failed +=1
        cell_data[num_cycle] = status
        np.save("Data/end_m" + str(module) + "_c" + str(stop), results)
        print(f"Batch {num_cycle // batch_size} of {stop // batch_size} done.\nTotal Time: {time.time()-start_time}s.\nNumber of failed cells: {num_failed}")
    np.save("Data/end_m" + str(module) + "_c" + str(stop), results)



##########################################################

def SAF(module, form_settings=[4000, 1700, 100, 1]):
    """
    perform stuck at fault testing on specified module
    :param module: module to test
    :return: nothing, saved to npy file
    """

    RRAM.module(action='set', target=str(module), verbal=False)

    RRAM.conf_form(*[str(param) for param in form_settings])
    RRAM.form(level='module', number='0', verbal=False)

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
    status = np.ndarray(shape=(256, 256), dtype=dict)

    #start timer
    start_time = time.time()

    #cycle the module
    results = {"module": module,  "status": status,
               "form_settings": form_settings}
    np.save("Data/saf_m" + str(module) + "_c" + str(numCycles), results)

    cycle_time = time.time_ns() - start_time
    #check the cells
    for row in range(len(status)):
        for col in range(len(status[row])):
            address = row * 256 + col
            if status[row][col] == None:
                status[row][col] = dict()
            status[row][col]['saf'], status[row][col]['lrs'], status[row][col]['hrs'] = check(address)
        np.save("Data/saf_m" + str(module) + "_c" + str(numCycles), results)
        print("Read row:", row)
    read_time = time.time() - start_time
    results["read_time"] = read_time
    results["cycle_time"] = cycle_time
    np.save("Data/saf_m" + str(module) + "_c" + str(numCycles), results)

def MR(module, numSamples):
    """
    check resistance variations of a module that was already SAF tested.
    :param module: module number to compute resistances for
    :param numSamples: number of resistance samples in the module to collect
    :return: nothong, saved to npy file
    """

    module = int(module)
    numSamples = int(numSamples)

    #set module
    RRAM.module(action='set', target=str(module), verbal=False)

    # set read, set, reset parameters TODO: make set and reset voltages input
    RRAM.conf_read(cycle='5', verbal=False)
    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(1200), cycle=str(16), times=str(10), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2800), AVDD_WL=str(2800), cycle=str(100), times=str(10), verbal=False)

    # set weird adc settings to 0
    RRAM.adc(action='set', action_type='cal', target='0', verbal=False)
    RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    # set target bitline voltage 2-200mV
    Board.DAC.set_source(value="200", target='VTGT_BL', verbal=False)

    #generate a lot of voltage references
    references = resistance.references(module, VTGT=200)

    resistances = {}

    results = {"module": module, "numSamples": numSamples, "resistances": resistances}

    np.save("Data/delta_res_m" + str(module) + "_s" + str(numSamples), results)

    blockSize = int(256*256/numSamples)

    print("Address\t(Row, Col)\t|\tLRS\t|\tHRS\t|\tDelta")

    for sample in range(0, numSamples):
        addr = np.random.randint(low=sample * blockSize, high=min((sample + 1) * blockSize, 256 * 256), dtype=int)
        row = addr // 256
        col = addr % 256
        #set
        RRAM.set(level="cell", number=str(addr), verbal=False)
        LRS = np.round(resistance.resistance(addr, references, VTGT=200), decimals=0)
        #reset
        RRAM.reset(level="cell", number=str(addr), verbal=True)
        HRS = np.round(resistance.resistance(addr, references, VTGT=200), decimals=0)
        resistances[addr] = {"LRS": LRS, "HRS": HRS, "Delta": HRS-LRS}

        if sample % 100 == 0:
            np.save("Data/delta_res_m" + str(module) + "_s" + str(numSamples), results)

        print(str(addr) + "\t" + f"({row}, {col})" + "\t|\t" + str(LRS) + "\t|\t" + str(HRS) + "\t|\t" + str(HRS - LRS))

    np.save("Data/delta_res_m" + str(module) + "_s" + str(numSamples), results)

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

def decode(argList):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The method/test you desire to run")
    parser.add_argument("module", type=int, help="Module to run test on")
    parser.add_argument("col",    type=int, help="Column to run test on")
    parser.add_argument("-f", "--conf_form", type=int, nargs=4, help="Arguments to pass to conf_form", default=None)
    parser.add_argument("-n", "--num_cycles", type=int, help="#S/R cycles total", default=1000000)
    parser.add_argument("-b", "--batch_size", type=int, help="#S/R cycles between checking cell health", default=5000)
    parser.add_argument('-s', '--conf_set', type=int, nargs=4, help="Arguments to pass to conf_set", default=[2200, 1200, 16, 10])
    parser.add_argument('-r', '--conf_reset', type=int, nargs=4, help="Arguments to pass to conf_reset", default=[2800, 2800, 100, 10])
    args = parser.parse_args(argList)
    if args.command == "SAF":
        if args.conf_form:
            SAF(args.module, args.conf_form)
        else:
            SAF(args.module)
    elif args.command == "ENDURANCE":
        endurance(args.module, args.col, args.num_cycles, args.batch_size, args.conf_form, args.conf_set, args.conf_reset)





