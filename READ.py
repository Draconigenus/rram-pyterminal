
import random
import time
from ctypes import c_int8
import numpy as np
import sys

import Board.DAC
from Lib import RRAM

'''
def READ(module, addr, form):
    VTGT = 200
    offset = 10
    step = 20
    addr = int(addr)
    FORM = 1

    RRAM.module(action='set', target=str(module), verbal=False)
    if FORM:
        RRAM.conf_form(AVDD_WR=str(3200), AVDD_WL=str(1700), cycle=str(100), times=str(1))
        RRAM.form(level='col', number=str(addr))

    cal   = RRAM.adc(action='set', action_type='cal',   target='0', verbal=False)
    hbias = RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)
    
    RRAM.conf_ADC(offset=str(offset), step=str(step), comp='0x7FFF', verbal=False)
    RRAM.sweep_VRef(low='0', high='900', step='1', verbal=False)
    RRAM.list_VRef(verbal=True)

    Board.DAC.set_source(value=str(VTGT), target='VTGT_BL', verbal=False)

    RRAM.conf_read(cycle='5', verbal=False)
    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(1300), cycle=str(100), times=str(20), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2800), AVDD_WL=str(2800), cycle=str(100), times=str(20), verbal=False)

    for row in range(8, 16):
        RRAM.read_lane(address=str(row * 256 + addr), data='0x000', verbal=True)

    RRAM.set(level='col', number=str(addr), verbal=False)
    for row in range(8, 16):
        RRAM.read_lane(address=str(row * 256 + addr), data='0x001', verbal=True)

    RRAM.reset(level='col', number=str(addr), verbal=False)
    for row in range(8, 16):
        RRAM.read_lane(address=str(row * 256 + addr), data='0x001', verbal=True)
'''

def READ(module, addr, form):
    VTGT = 200
    addr = int(addr)
    FORM = 1

    RRAM.module(action='set', target=str(module), verbal=False)
    if FORM:
        RRAM.conf_form(AVDD_WR=str(3200), AVDD_WL=str(1700), cycle=str(100), times=str(1))
        RRAM.form(level='col', number=str(addr))

    cal   = RRAM.adc(action='set', action_type='cal',   target='0', verbal=False)
    hbias = RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    Board.DAC.set_source(value=str(VTGT), target='VTGT_BL', verbal=False)

    RRAM.conf_read(cycle='5', verbal=False)
    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(1300), cycle=str(2), times=str(1), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2400), AVDD_WL=str(2400), cycle=str(32), times=str(4), verbal=False)

    def count_ones(N, bits=16):
        ones = 0
        for bit in range(bits):
            ones += (N >> bit) & 1
        return ones

    SET   = {}
    RESET = {}

    RRAM.reset(level='col', number=str(addr), verbal=False)
    RRAM.set(level='col', number=str(addr), verbal=False)
    for offset in [5, 8, 11, 14, 17]:
        for step in [8, 11, 14, 17, 20]:
            RRAM.conf_ADC(offset=str(offset), step=str(step), comp='0x7FFF', verbal=False)
            SET[(offset, step)] = 0
            for row in range(8, 16):
                rd = int( RRAM.read_lane(address=str(row * 256 + addr), data='0x001', verbal=False), 16 )
                print (hex(rd))
                SET[(offset, step)] += count_ones(rd) / 8

    RRAM.reset(level='col', number=str(addr), verbal=False)
    for offset in [5, 8, 11, 14, 17]:
        for step in [8, 11, 14, 17, 20]:
            RRAM.conf_ADC(offset=str(offset), step=str(step), comp='0x7FFF', verbal=False)
            RESET[(offset, step)] = 0            
            for row in range(8, 16):
                rd = int( RRAM.read_lane(address=str(row * 256 + addr), data='0x001', verbal=False), 16 )
                print (hex(rd))
                RESET[(offset, step)] += count_ones(rd) / 8

    best = (0, None, None)
    for (offset, step) in SET.keys():
        diff = RESET[(offset, step)] - SET[(offset, step)]
        if best[0] < diff: best = (diff, offset, step)

    print ('diff', best[0], 'offset', best[1], 'step', best[2])









