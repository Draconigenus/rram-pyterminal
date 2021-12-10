import CommandMap as CM
import PyTerminal as PT


def id (verbal):
    """ Get the ID of the RRAM Modules

    Args:
        verbal (bool): Whether to print the response or not.
    Returns:
        The ID of the RRAM Modules.

    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_PID, verbal)


def status(verbal):
    """ Get the status of the RRAM modules

    Args:
        verbal (bool): Whether to print the response or not.
    Returns:
        The status of the RRAM Modules.
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_STATUS, verbal)


def lane(action, target, verbal):
    """ Set/Get the selected ADC lane

    Args:
        action (str): Could be 'set' or 'get'
        target (str): Target lane number, from '0'~'7'
        verbal (bool): Whether to print the response or not.
    Returns:
        The status of the RRAM Modules.
    """
    if   action == 'set':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_LANE + ' ' + CM.CM_RRAM_SET + ' ' + target, verbal)
    elif action == 'get': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_LANE + ' ' + CM.CM_RRAM_GET, verbal))
    else: unknown(['RRAM', 'lane', action, target])


def group(action, target, verbal):
    """ Set/Get the selected group for the Vector module

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    target -- target group number, from '0'~'35'
    verbal -- whether to print the response or not
    """
    if   action == 'set':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_GROUP + ' ' + CM.CM_RRAM_SET + ' ' + target, verbal)
    elif action == 'get': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_GROUP + ' ' + CM.CM_RRAM_GET, verbal))
    else: unknown(['RRAM', 'group', action, target])


def module(action, target, verbal):
    """ Set/Get the selected RRAM module

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    target -- target RRAM module number, from '0'~'287'
    verbal -- whether to print the response or not
    """
    if   action == 'set':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MODULE + ' ' + CM.CM_RRAM_SET + ' ' + target, verbal)
    elif action == 'get': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MODULE + ' ' + CM.CM_RRAM_GET, verbal))
    else: unknown(['RRAM', 'module', action, target])


def mask(action, target, verbal):
    """ Set/Get the RRAM module selection mask register

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    target -- target RRAM module selection mask, from '0x00000001'~'0xFFFFFFFF'
    verbal -- whether to print the response or not
    """
    if   action == 'set':        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MASK + ' ' + CM.CM_RRAM_SET + ' ' + target, verbal)
    elif action == 'get': return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MASK + ' ' + CM.CM_RRAM_GET, verbal)
    else: unknown(['RRAM', 'mask', action, target])


def address(action, target, verbal):
    """ Set/Get the RRAM module address register

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    target -- target address, from '0'~'65535'
    verbal -- whether to print the response or not
    """
    if   action == 'set':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADDRESS + ' ' + CM.CM_RRAM_SET + ' ' + target, verbal)
    elif action == 'get': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADDRESS + ' ' + CM.CM_RRAM_GET, verbal))
    else: unknown(['RRAM', 'address', action, target])


def read(action, action_type, target, verbal):
    """ Configure read related settings

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    action_type -- could be 'status', 'enable', 'cycle', 'source', 'counter', 'data'
    target -- target number, '0'~'1' for 'enable' 'source', '0'~'255' for 'cycle', and '0x1'~'0x1FF' for 'data'
    verbal -- whether to print the response or not
    """
    if action == 'set':
        if   action_type == 'enable' :        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_READ_ENABLE  + ' ' + target, verbal)
        elif action_type == 'cycle'  :        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_READ_CYCLE   + ' ' + target, verbal)
        elif action_type == 'source' :        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_READ_SOURCE  + ' ' + target, verbal)
        elif action_type == 'counter':        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_READ_COUNTER + ' ' + target, verbal)
        elif action_type == 'data'   :        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_READ_DATA    + ' ' + target, verbal)
        else: unknown(['RRAM', 'read', action, action_type, target])
    elif action == 'get':
        if   action_type == 'enable' : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_READ_ENABLE , verbal))
        elif action_type == 'status' : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_READ_STATUS , verbal))
        elif action_type == 'cycle'  : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_READ_CYCLE  , verbal))
        elif action_type == 'source' : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_READ_SOURCE , verbal))
        elif action_type == 'counter': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_READ_COUNTER, verbal))
        elif action_type == 'data'   : return     PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_READ_DATA   , verbal)
        else: unknown(['RRAM', 'read', action, action_type, target])
    elif action == 'toggle':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_READ + ' ' + CM.CM_RRAM_TOGGLE, verbal)
    else: unknown(['RRAM', 'read', action, action_type, target])


def mac(action, action_type, target, verbal):
    """ Configure mac related settings

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    action_type -- could be 'status', 'result', 'mode', 'resolution'
    target -- target number, '0'~'1' for 'mode', '0'~'3' for 'resolution'
    verbal -- whether to print the response or not
    """
    if action == 'set':
        if   action_type == 'mode'      :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MAC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_MAC_MODE       + ' ' + target, verbal)
        elif action_type == 'resolution':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MAC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_MAC_RESOLUTION + ' ' + target, verbal)
        else: unknown(['RRAM', 'mac', action, action_type, target])
    elif action == 'get':
        if   action_type == 'status'    : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MAC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_MAC_STATUS    , verbal))
        elif action_type == 'mode'      : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MAC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_MAC_MODE      , verbal))
        elif action_type == 'resolution': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MAC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_MAC_RESOLUTION, verbal))
        elif action_type == 'result'    : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_MAC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_MAC_RESULT    , verbal))
        else: unknown(['RRAM', 'mac', action, action_type, target])
    else: unknown(['RRAM', 'mac', action, action_type, target])


def write(action, action_type, target, verbal):
    """ Configure read related settings

    Keyword arguments:
    pyterminal -- current connected COM port
    action -- could be 'set' or 'get'
    action_type -- could be 'status', 'enable', 'cycle', 'mode'
    target -- target number, '0'~'1' for 'enable' 'mode', '0'~'65535' for 'cycle'
    verbal -- whether to print the response or not
    """
    if action == 'set':
        if   action_type == 'enable':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_WRITE_ENABLE + ' ' + target, verbal)
        elif action_type == 'cycle' :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_WRITE_CYCLE  + ' ' + target, verbal)
        elif action_type == 'mode'  :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_WRITE_MODE   + ' ' + target, verbal)
        else: unknown(['RRAM', 'write', action, action_type, target])
    elif action == 'get':
        if   action_type == 'enable': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_WRITE_ENABLE, verbal))
        elif action_type == 'status': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_WRITE_STATUS, verbal))
        elif action_type == 'cycle' : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_WRITE_CYCLE , verbal))
        elif action_type == 'mode'  : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_WRITE_MODE  , verbal))
        else: unknown(['RRAM', 'write', action, action_type, target])
    elif action == 'trigger':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_WRITE + ' ' + CM.CM_RRAM_TRIGGER, verbal)
    else: unknown(['RRAM', 'write', action, action_type, target])


def adc(action, action_type, target, verbal):
    """ Configure adc related settings
    Args:
                verbal (bool): Whether to print the response or not.
        action (str): could be 'set' or 'get'
        action_type (str): could be 'raw', 'step', 'offset', 'comp', 'hbias', 'cal'
        target (str): target number, '0'~'1' for 'hbias' 'cal', '0'~'63' for 'step' 'offset', '0x0000'~'0x7FFF' for 'comp'
    """
    if action == 'set':
        if   action_type == 'step'  :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_ADC_STEP   + ' ' + target, verbal)
        elif action_type == 'offset':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_ADC_OFFSET + ' ' + target, verbal)
        elif action_type == 'comp'  :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_ADC_COMP   + ' ' + target, verbal)
        elif action_type == 'hbias' :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_ADC_HBIAS  + ' ' + target, verbal)
        elif action_type == 'cal'   :            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_ADC_CAL    + ' ' + target, verbal)
        else: unknown(['RRAM', 'adc', action, action_type, target])
    elif action == 'get':
        if   action_type == 'raw'   : return     PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ADC_RAW   , verbal)
        elif action_type == 'step'  : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ADC_STEP  , verbal))
        elif action_type == 'offset': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ADC_OFFSET, verbal))
        elif action_type == 'comp'  : return     PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ADC_COMP  , verbal)
        elif action_type == 'hbias' : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ADC_HBIAS , verbal))
        elif action_type == 'cal'   : return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ADC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ADC_CAL   , verbal))
        else:
            unknown(['RRAM', 'adc', action, action_type, target])
    else: unknown(['RRAM', 'adc', action, action_type, target])


def pg(action, action_type, target, verbal):
    """ Configure power gating related settings

    Keyword arguments:
        action -- could be 'set' or 'get'
    action_type -- could be 'disable'
    target -- target number, '0'~'1' for 'disable'
    verbal -- whether to print the response or not
    """
    if action == 'set':
        if   action_type == 'disable':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_PG + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_PG_DISABLE + ' ' + target, verbal)
        else:
            unknown(['RRAM', 'pg', action, action_type, target])
    elif action == 'get':
        if   action_type == 'disable': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_PG + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_PG_DISABLE, verbal))
        else:
            unknown(['RRAM', 'pg', action, action_type, target])
    else: unknown(['RRAM', 'pg', action, action_type, target])


def ecc(action, action_type, target, verbal):
    """ Configure power gating related settings

    Keyword arguments:
        action -- could be 'set', 'get', 'clear', or 'check'
    action_type -- could be 'enable'
    target -- target number, '0'~'1' for 'enable'
    verbal -- whether to print the response or not
    """
    if action == 'set':
        if   action_type == 'enable':            PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ECC + ' ' + CM.CM_RRAM_SET + ' ' + CM.CM_RRAM_ECC_ENABLE + ' ' + target, verbal)
        else:
            unknown(['RRAM', 'ecc', action, action_type, target])
    elif action == 'get':
        if   action_type == 'enable': return int(PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ECC + ' ' + CM.CM_RRAM_GET + ' ' + CM.CM_RRAM_ECC_ENABLE, verbal))
        else:
            unknown(['RRAM', 'ecc', action, action_type, target])
    elif action == 'clear':
               PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ECC + ' ' + CM.CM_RRAM_CLEAR, verbal)
    elif action == 'check':
        return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_ECC + ' ' + CM.CM_RRAM_CHECK, verbal)
    else: unknown(['RRAM', 'ecc', action, action_type, target])


def switch(index, verbal):
    """ Switch to module "index" and configure related things. (ex. ADC, VTGT_BL ... etc)

    Keyword arguments:
        index -- from '0' ~ '287', the target RRAM module
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SWITCH + ' ' + index, verbal)

def conf_form(AVDD_WR, AVDD_WL, cycle, times, verbal):
    """ Configure FORM operation

    Keyword arguments:
        AVDD_WR -- AVDD_WR voltage
    AVDD_WL -- AVDD_WL voltage
    cycle -- number of clock cycles per pulse
    times -- number of pulses
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_FORM + ' ' + AVDD_WR + ' ' + AVDD_WL + ' ' + cycle + ' ' + times, verbal)


def form(level, number, verbal):
    """ FORM the cells

    Keyword arguments:
        level -- could be 'cell', 'row', 'col', 'module'
    number -- target number
    verbal -- whether to print the response or not
    """
    if level == 'cell':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_FORM + ' ' + CM.CM_RRAM_API_LEVEL_CELL + ' ' + number, verbal)
    elif level == 'row':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_FORM + ' ' + CM.CM_RRAM_API_LEVEL_ROW + ' ' + number, verbal)
    elif level == 'col':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_FORM + ' ' + CM.CM_RRAM_API_LEVEL_COL + ' ' + number, verbal)
    elif level == 'module':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_FORM + ' ' + CM.CM_RRAM_API_LEVEL_MODULE + ' ' + number, verbal)


def conf_set(AVDD_WR, AVDD_WL, cycle, times, verbal):
    """ Configure SET operation

    Keyword arguments:
        AVDD_WR -- AVDD_WR voltage
    AVDD_WL -- AVDD_WL voltage
    cycle -- number of clock cycles per pulse
    times -- number of pulses
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_SET + ' ' + AVDD_WR + ' ' + AVDD_WL + ' ' + cycle + ' ' + times, verbal)


def set(level, number, verbal):
    """ SET the cells

    Keyword arguments:
        level -- could be 'cell', 'row', 'col', 'module'
    number -- target number
    verbal -- whether to print the response or not
    """
    if level == 'cell':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET + ' ' + CM.CM_RRAM_API_LEVEL_CELL + ' ' + number, verbal)
    elif level == 'row':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET + ' ' + CM.CM_RRAM_API_LEVEL_ROW + ' ' + number, verbal)
    elif level == 'col':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET + ' ' + CM.CM_RRAM_API_LEVEL_COL + ' ' + number, verbal)
    elif level == 'module':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET + ' ' + CM.CM_RRAM_API_LEVEL_MODULE + ' ' + number, verbal)


def conf_reset(AVDD_WR, AVDD_WL, cycle, times, verbal):
    """ Configure RESET operation

    Keyword arguments:
        AVDD_WR -- AVDD_WR voltage
    AVDD_WL -- AVDD_WL voltage
    cycle -- number of clock cycles per pulse
    times -- number of pulses
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_RESET + ' ' + AVDD_WR + ' ' + AVDD_WL + ' ' + cycle + ' ' + times, verbal)


def reset(level, number, verbal):
    """ RESET the cells

    Keyword arguments:
        level -- could be 'cell', 'row', 'col', 'module'
    number -- target number
    verbal -- whether to print the response or not
    """
    if level == 'cell':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_RESET + ' ' + CM.CM_RRAM_API_LEVEL_CELL + ' ' + number, verbal)
    elif level == 'row':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_RESET + ' ' + CM.CM_RRAM_API_LEVEL_ROW + ' ' + number, verbal)
    elif level == 'col':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_RESET + ' ' + CM.CM_RRAM_API_LEVEL_COL + ' ' + number, verbal)
    elif level == 'module':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_RESET + ' ' + CM.CM_RRAM_API_LEVEL_MODULE + ' ' + number, verbal)


def set_reset(level, number, times, verbal):
    """ SET and RESET the cells

    Keyword arguments:
        level -- could be 'cell', 'row', 'col', 'module'
    number -- target number
    times -- how many loops per set&reset
    verbal -- whether to print the response or not
    """
    if level == 'cell':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET_RESET + ' ' + CM.CM_RRAM_API_LEVEL_CELL + ' ' + number + ' ' + times, verbal)
    elif level == 'row':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET_RESET + ' ' + CM.CM_RRAM_API_LEVEL_ROW + ' ' + number + ' ' + times, verbal)
    elif level == 'col':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET_RESET + ' ' + CM.CM_RRAM_API_LEVEL_COL + ' ' + number + ' ' + times, verbal)
    elif level == 'module':
        PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SET_RESET + ' ' + CM.CM_RRAM_API_LEVEL_MODULE + ' ' + number + ' ' + times, verbal)


def write_byte(address, value, verbal):
    """ Write 'value' to 'address'

    Keyword arguments:
        address -- address to be written to
    value -- value to be written to
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_WRITE_BYTE + ' ' + address + ' ' + value, verbal)


def write_byte_iter(address, value, verbal):
    """ Write 'value' to 'address' iteratively, this function is more robust than 'write_byte' but takes longer

    Keyword arguments:
        address -- address to be written to
    value -- value to be written to
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_WRITE_BYTE_ITER + ' ' + address + ' ' + value, verbal)


def conf_read(cycle, verbal):
    """ Configure READ operation

    Keyword arguments:
        cycle -- number of clock cycles per pulse
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_READ + ' ' + cycle, verbal)


def read_lane(address, data, verbal):
    """ Read the 'address' cell with 'data' fed to the WLs

    Keyword arguments:
        address -- address to be read from
    value -- value to be fed to the WLs
    verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_READ_LANE + ' ' + address + ' ' + data, verbal)


def read_byte(address, counter, data, verbal):
    """ Read the whole byte from 'address' with 'data' fed to the WLs and 'counter' for the MAC unit

    Keyword arguments:
        address -- address to be read from
    counter -- so the MAC unit knows which bit the 'data' is currently at
    value -- value to be fed to the WLs
    verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_READ_BYTE + ' ' + address + ' ' + counter + ' ' + data, verbal)


def conf_ADC(offset, step, comp, verbal):
    """ Configure ADC settings

    Keyword arguments:
        offset -- from '0'~'63', '0' for minimum offset and '63' for maximum offset
    step -- from '0'~'63', '0' for minimum step and '63' for maximum step
    comp -- comparator enables, from '0x0001'~'0x7FFF', each bit controls a comparator
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_ADC + ' ' + offset + ' ' + step + ' ' + comp, verbal)


def conf_MAC(mode, resolution, verbal):
    """ Configure MAC settings

    Keyword arguments:
        mode -- from '0'~'1', '0' for unsigned and '1' for 'signed'
    resolution -- from '0'~'3', '0' for 1 bit, '1' for 2 bits, '2' for 4 bits, and '3' for 8 bits
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_MAC + ' ' + mode + ' ' + resolution, verbal)


def calibrate_voltage_references(low, high, tolerance, verbal):
    """ Calibrate the internally generated reference voltages so the range would be approx. ('low', 'high') for the current module

    Keyword arguments:
        low -- lower bound of the reference voltages
    high -- upper bound of the reference voltages
    tolerance -- means ideally the first extreme reference voltage should be within 'tolerance' from either 'low' or 'high'
    verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CAL_VREF + ' ' + low + ' ' + high + ' ' + tolerance, verbal)


def sweep_voltage_references(low, high, step, verbal):
    """ Sweep the ADC_CAL and look for all 15 internally generated reference voltages for the current module

    Keyword arguments:
        low -- starting voltage for ADC_CAL
    high -- ending voltage for ADC_CAL
    step -- step for ADC_CAL
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SWEEP_VREF + ' ' + low + ' ' + high + ' ' + step, verbal)


def list_voltage_references(verbal):
    """ List 15 internally generated reference voltages of the current module, sweep_voltage_references needs to be done in advance

    Keyword arguments:
        verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_LIST_VREF, verbal)


def calibrate_vtgt_bl(verbal):
    """ Calibrate VTGT_BL for the current module

    Keyword arguments:
        verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CAL_VTGT_BL, verbal)


def conf_vtgt_bl(vtgt_bl, verbal):
    """ Save the VTGT_BL for the current module

    Keyword arguments:
        verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CONF_VTGT_BL + ' ' + vtgt_bl, verbal)


def list_vtgt_bl(verbal):
    """ List saved VTGT_BL of the current module

    Keyword arguments:
        verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_LIST_VTGT_BL, verbal)

def sweep_decoder_references(ones, verbal):
    """ Calibrate decoder reference levels

    Keyword arguments:
        ones -- could be omit or '0'~'9', omit means do the calibration for all '1'~'9'
    verbal -- whether to print the response or not
    """
    PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_SWEEP_DREF + ' ' + ones, verbal)


def list_decoder_references(verbal):
    """ List decoder reference levels of the current module

    Keyword arguments:
        verbal -- whether to print the response or not
    """
    return PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_LIST_DREF, verbal)


def check(level, number, verbal):
    """ Check the health of RRAM cells, this function essentially SET the cell and read the value, then RESET the cell
        and read the value.
        If the cell is healthy, the ADC raw value after SET should be smaller than the value after RESET

    Keyword arguments:
        level -- could be 'cell', 'row', 'col', 'module'
    number -- target number
    verbal -- whether to print the response or not
    """
    if level == 'cell':
        address = int(number)
        response = PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CHECK_CELL + ' ' + str(address), False)
        print(f'{address:>6} : {response:>10}')
    elif level == 'row':
        for col in range(0, 256):
            address = int(number)*256 + col
            response = PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CHECK_CELL + ' ' + str(address), False)
            print(f'{address:>6} : {response:>10}')
    elif level == 'col':
        for row in range(0, 256):
            address = row*256 + int(number)
            response = PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CHECK_CELL + ' ' + str(address), False)
            print(f'{address:>6} : {response:>10}')
    elif level == 'module':
        for row in range(0, 256):
            for col in range(0, 256):
                address = row*256 + col
                response = PT.send_command(CM.CM_RRAM + ' ' + CM.CM_RRAM_API_CHECK_CELL + ' ' + str(address), False)
                print(f'{address:>6} : {response:>10}')


def unknown(parameters):
    """ Print out the unknown command

    Keyword arguments:
    parameters -- the split version of the command
    """
    print('Unknown Command: ' + ' '.join(parameters) + '(From PyTerminal)')


def decode(parameters):
    """ Decode the split version of the command

    Keyword arguments:
        parameters -- split version of the command
    """
    # Driver functions
    if   parameters[1] == 'id'               : id                          (                                                            True)
    elif parameters[1] == 'status'           : status                      (                                                            True)
    elif parameters[1] == 'lane'             : lane                        (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'group'            : group                       (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'module'           : module                      (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'mask'             : mask                        (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'address'          : address                     (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'read'             : read                        (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'mac'              : mac                         (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'write'            : write                       (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'adc'              : adc                         (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'pg'               : pg                          (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'ecc'              : ecc                         (parameters[2], parameters[3], parameters[4],                True)
    # API functions
    elif parameters[1] == 'switch'           : switch                      (parameters[2],                                              True)
    elif parameters[1] == 'conf_form'        : conf_form                   (parameters[2], parameters[3], parameters[4], parameters[5], True)
    elif parameters[1] == 'form'             : form                        (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'conf_set'         : conf_set                    (parameters[2], parameters[3], parameters[4], parameters[5], True)
    elif parameters[1] == 'set'              : set                         (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'set_reset'        : set_reset                   (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'conf_reset'       : conf_reset                  (parameters[2], parameters[3], parameters[4], parameters[5], True)
    elif parameters[1] == 'reset'            : reset                       (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'write_byte'       : write_byte                  (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'write_byte_iter'  : write_byte_iter             (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'conf_read'        : conf_read                   (parameters[2],                                              True)
    elif parameters[1] == 'read_lane'        : read_lane                   (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'read_byte'        : read_byte                   (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'conf_ADC'         : conf_ADC                    (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'conf_MAC'         : conf_MAC                    (parameters[2], parameters[3],                               True)
    elif parameters[1] == 'calibrate_VRef'   : calibrate_voltage_references(parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'sweep_VRef'       : sweep_voltage_references    (parameters[2], parameters[3], parameters[4],                True)
    elif parameters[1] == 'list_VRef'        : list_voltage_references     (                                                            True)
    elif parameters[1] == 'calibrate_VTGT_BL': calibrate_vtgt_bl           (                                                            True)
    elif parameters[1] == 'conf_VTGT_BL'     : conf_vtgt_bl                (parameters[2],                                              True)
    elif parameters[1] == 'list_VTGT_BL'     : list_vtgt_bl                (                                                            True)
    elif parameters[1] == 'sweep_DRef'       : sweep_decoder_references    (parameters[2],                                              True)
    elif parameters[1] == 'list_DRef'        : list_decoder_references     (                                                            True)
    elif parameters[1] == 'check'            : check                       (parameters[2], parameters[3],                               True)
    else: unknown(parameters)
