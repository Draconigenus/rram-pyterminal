
import random
import time
from ctypes import c_int8
import numpy as np
import sys

import Board.DAC
import DAC
from Lib import RRAM

def resistance(addr, refs, VTGT):

    #################################################

    def _localize(ones, zeros):
        if len(ones) == 0: 
            print ('No 1s')
            return np.min(zeros)
        if len(zeros) == 0: 
            print ('No 0s')
            return np.max(ones)
        max_one = np.max(ones)
        min_zero = np.min(zeros)
        if max_one <= min_zero: 
            return (max_one + min_zero) / 2
        else: 
            ones = ones[np.where(ones > min_zero)]
            zeros = zeros[np.where(zeros < max_one)]
            # return np.median(ones.tolist() + zeros.tolist())
            return np.mean(ones.tolist() + zeros.tolist())

    def _resistance(VTGT, Rsense, VBL):
        Rcell = VTGT / ((VBL - VTGT) / Rsense)
        return Rcell

    def _compare(numEnabled):
        #################################################
        '''
        rds = []
        for _ in range(10):
            rd = int( RRAM.read_lane(address=str(addr), data='0x001', verbal=False), 16)
            rds.append(rd)
        rd = np.min(rd)
        '''
        #################################################
        if numEnabled == 0:
            data = "0x000"
        else:
            data = "0x001"
        DAC.set_source(value=str(200), target="VTGT_BL", verbal=False)
        rd = int( RRAM.read_lane(address=str(addr), data=data, verbal=False), 16)
        #################################################
        comp = np.zeros(15)
        for bit in range(15):
            mask = 1 << bit
            comp[bit] = (rd & mask) == mask
        #################################################
        return np.array(comp)

    ##############################################

    ones = []
    zeros = []
    for (offset, step) in refs.keys():
        #################################################
        RRAM.conf_ADC(offset=str(offset), step=str(step), comp='0x7FFF', verbal=False)
        #################################################
        ref = refs[(offset, step)]
        #################################################
        comps = _compare(0)
        for i, _ in enumerate(ref):
            if comps[i]: zeros.append( ref[i] )
            else:        ones.append( ref[i] )
        #################################################
    VBL_0 = _localize(np.array(ones), np.array(zeros))

    #####################################################

    ones = []; zeros = []
    for (offset, step) in refs.keys():
        #################################################
        RRAM.conf_ADC(offset=str(offset), step=str(step), comp='0x7FFF', verbal=False)
        #################################################
        ref = refs[(offset, step)]
        #################################################
        comps = _compare(1)
        for i, _ in enumerate(ref):
            if comps[i]: zeros.append( ref[i] )
            else:        ones.append( ref[i] )
        #################################################
    VBL = _localize(np.array(ones), np.array(zeros))
    # Rcell = _resistance(VTGT=VBL_0, Rsense=3000, VBL=VBL)
    Rcell = _resistance(VTGT=VTGT, Rsense=3000, VBL=VBL)
    #################################################
    return Rcell

##############################################################################################

def references(module, VTGT):
    #########################
    if module == '': module = 0
    else:            module = int(module)
    #########################
    if VTGT == '': VTGT = 200
    else:          VTGT = int(VTGT)
    #########################
    def parse_ints(string):
        numbers = []
        for word in string.split():
            if word.isdigit():
                numbers.append(int(word))
        return numbers
    #########################
    Board.DAC.set_source(value=str(VTGT), target='VTGT_BL', verbal=False)
    
    ret = {}
    for offset in [3, 4, 5, 6, 7]:
        for step in [1, 2, 3, 4, 5, 6, 7, 8]:
            RRAM.conf_ADC(offset=str(offset), step=str(step), comp='0x7FFF', verbal=False)
            RRAM.sweep_VRef(low='0', high='900', step='4', verbal=False)

            refs = RRAM.list_VRef(verbal=False)
            refs = parse_ints(refs)
            refs = np.array(refs[15:])

            ret[(offset, step)] = refs
            #print (refs)

    Board.DAC.set_source(value=str(VTGT), target='VTGT_BL', verbal=False)
    #########################
    return ret

##############################################################################################

def measure_resistance(module, addr):

    ###############################################

    if module == '': module = 0
    else:            module = int(module)

    if addr == '': addr = 200
    else:          addr = int(addr)

    print ("module: %d address: %d" % (module, addr))

    ###############################################

    RRAM.module(action='set', target=str(module), verbal=False)

    RRAM.conf_read(cycle='5', verbal=False)

    cal   = RRAM.adc(action='set', action_type='cal',   target='0', verbal=False)
    hbias = RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    # _ = RRAM.calibrate_VTGT_BL(verbal=False) # returns full string thats printed.
    # VTGT = Board.DAC.get_source('VTGT_BL', verbal=False)
    # print (VTGT)
    
    VTGT = 200
    Board.DAC.set_source(value=str(VTGT), target='VTGT_BL', verbal=False)
    
    refs = references(module=module, col=addr, VTGT=VTGT)

    ###############################################

    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(2200), cycle=str(16), times=str(2), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2800), AVDD_WL=str(2800), cycle=str(100), times=str(2), verbal=False)

    for _ in range(10):
        RRAM.set(level='col', number=str(addr), verbal=False)
        RRAM.reset(level='col', number=str(addr), verbal=False)

    ###############################################
    results = {}
    V_LO = 2000
    V_HI = 2800
    for step_size in [50, 25, 10]:
        step_num = (V_HI - V_LO) // step_size + 1
        for step in range(step_num):
            #########################
            V_WR = V_LO + step * step_size
            #########################
            RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(2200), cycle=str(16), times=str(2), verbal=False)
            RRAM.conf_reset(AVDD_WR=str(V_WR), AVDD_WL=str(V_WR), cycle=str(100), times=str(2), verbal=False)
            #########################
            if step == 0: RRAM.set(level='col', number=str(addr), verbal=False)
            else:         RRAM.reset(level='col', number=str(addr), verbal=False)
            #########################
            row_offset = 8
            for row in range(32):
                address = (row + row_offset) * 256 + addr
                R = resistance(addr=address, refs=refs, VTGT=VTGT)
                #########################
                key = (step_size, step, row)
                if key in results.keys(): print ('ERROR')
                results[key] = R
                #########################
                print (V_WR, step, row, '|', '%x' % (address), R, flush=True)
                sys.stdout.flush()
        # save each outer loop
        np.save('results.npy', results)

##############################################################################################




