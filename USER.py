import random
import time
from Lib import RRAM


def clear(pyterminal):
    """ Clear the RRAM module when it's just awakened

    Keyword arguments:
    pyterminal -- current connected COM port
    """
    # Clear up some registers
    RRAM.read(pyterminal, 'set', 'enable', '1', True)
    RRAM.read(pyterminal, 'set', 'counter', '7', True)
    RRAM.read(pyterminal, 'toggle', '', '', True)
    RRAM.read(pyterminal, 'set', 'counter', '0', True)
    RRAM.read(pyterminal, 'toggle', '', '', True)
    RRAM.read(pyterminal, 'set', 'enable', '0', True)


def read(pyterminal, level, number):
    """ A handy read function to read through one or more RRAM cells

    Keyword arguments:
    pyterminal -- current connected COM port
    level -- could be 'cell', 'row', 'col', 'module'
    number -- target number
    """
    if level == 'cell':
        addr = int(number)
        response = RRAM.read_lane(pyterminal, str(addr), '0x1', False)
        print(f'{addr:>6} : {response:>10}')
    elif level == 'row':
        for col in range(0, 256):
            addr = int(number)*256 + col
            response = RRAM.read_lane(pyterminal, str(addr), '0x1', False)
            print(f'{addr:>6} : {response:>10}')
    elif level == 'col':
        for row in range(0, 256):
            addr = row*256 + int(number)
            response = RRAM.read_lane(pyterminal, str(addr), '0x1', False)
            print(f'{addr:>6} : {response:>10}')
    elif level == 'module':
        for row in range(0, 256):
            print('row: ' + str(row))
            for col in range(0, 256):
                addr = row*256 + col
                response = RRAM.read_lane(pyterminal, str(addr), '0x1', False)
                print(f'{addr:>6} : {response:>10}')

def calibrate_VTGT_BL(pyterminal, row, col):
    """ Calibrate VTGT_BL for the decoder reference levels are between '0xFFFF'~'0x4000'

    Keyword arguments:
    pyterminal -- current connected COM port
    row -- from '0'~'255'
    col -- from '0'~'255'
    """
    print('calibrating VTGT_BL ...')

    # Reset first 9 cells
    print('Resetting ... ', end='')
    for row_offset in range(0, 9):
        addr = (int(row)+row_offset) * 256 + int(col)
        RRAM.reset(pyterminal, 'cell', str(addr), True)

    # Set second 9 cells
    print('Setting ... ')
    for row_offset in range(9, 18):
        addr = (int(row)+row_offset) * 256 + int(col)
        RRAM.set(pyterminal, 'cell', str(addr), True)

    trial = 5
    cal_low = 0
    cal_high = 1100
    vtgt_bl = 0

    while cal_high > cal_low and trial:
        vtgt_bl = int((cal_low + cal_high)/2.0)
        DAC.set_voltage_source(pyterminal, str(vtgt_bl), 'VTGT_BL')
        raw_high = RRAM.read_lane(pyterminal, str((int(row)+9)*256+int(col)), '0x1FF', False)
        print('cal_low: ' + str(cal_low) + ' ; cal_high: ' + str(cal_high) + ' ; raw_high: ' + raw_high, end='')
        if int(raw_high, 0) < int('0x4000', 0):
            trial = 5
            cal_high = vtgt_bl
        elif int(raw_high, 0) > int('0x4000', 0):
            trial = 5
            cal_low = vtgt_bl
        else:
            trial -= 1
        print(' ; trial: ' + str(trial))

    print('VTGT_BL: ' + str(vtgt_bl))
    test_bit_cim(pyterminal, row, col, True)


def calibrate_VTGT_BL_linear(pyterminal, row, col):
    """ Calibrate VTGT_BL for the decoder reference levels are between '0xFFFF'~'0x4000', linear version

    Keyword arguments:
    pyterminal -- current connected COM port
    row -- from '0'~'255'
    col -- from '0'~'255'
    """
    print('calibrating VTGT_BL ...')

    trial = 5
    vtgt_bl = 50

    while trial:
        DAC.set_voltage_source(pyterminal, str(vtgt_bl), 'VTGT_BL')
        raw_low = RRAM.read_lane(pyterminal, str(int(row)*256+int(col)), '0x1', False)
        raw_high = RRAM.read_lane(pyterminal, str((int(row)+9)*256+int(col)), '0x1FF', False)
        if raw_high == '0x4000':
            trial -= 1
        else:
            trial = 5
            vtgt_bl += 2

    print('VTGT_BL: ' + str(vtgt_bl))
    test_bit_cim(pyterminal, row, col, True)


def sweep_chip_VRef(pyterminal):
    """ Sweep reference voltages for the whole chip

    Keyword arguments:
    pyterminal -- current connected COM port
    """
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('| Module | Offset | Step |  VRef[0] |  VRef[1] |  VRef[2] |  VRef[3] |  VRef[4] |  VRef[5] |  VRef[6] |  VRef[7] |  VRef[8] |  VRef[9] | VRef[10] | VRef[11] | VRef[12] | VRef[13] | VRef[14] |')
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for module in range(0, 288):
        # Set to the new module and clear it
        RRAM.module(pyterminal, 'set', str(module), True)
        time.sleep(1)
        clear(pyterminal)

        # Find the (offset, step)
        trial = 3
        while trial:
            response = RRAM.calibrate_voltage_references(pyterminal, str(module), '120', '750', '5', False)
            offset = int(response.split()[0])
            step = int(response.split()[1])
            if offset != -1 and step != -1:
                break
            time.sleep(1)
            trial -= 1

        # Config the ADC and Sweep the VRef
        if trial:
            RRAM.conf_ADC(pyterminal, str(offset), str(step), '0x7FFF', True)
            RRAM.sweep_voltage_references(pyterminal, str(module), '50', '850', '2', True)

            # Find the VRef
            response = RRAM.list_voltage_references(pyterminal, str(module), False)
            vrefs = response.split('\n')[3].split('|')[2:17]
        else:
            vrefs = [''] * 15

        # Print out the result
        print(f'| {module:>6} | {offset:>6} | {step:>4} |', end='')
        for i in range(0, 15):
            print(f' {vrefs[i]:>8} |', end='')
        print('')
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


def test_write_byte(pyterminal, row, num):
    """ Test function for writing a byte at (row, col)

    Keyword arguments:
    pyterminal -- current connected COM port
    row -- from '0'~'255'
    col -- from '0'~'255'
    """
    row = int(row)
    num = int(num)
    print('-----------------------------------------------')
    print('| ( row, col) | Golden | Readout | Difference |')
    print('-----------------------------------------------')
    for col in range(0, num):
        addr = row * 256 + col
        golden = random.randint(-128, 127)
        RRAM.write_byte_iter(pyterminal, str(addr), str(golden), False)
        readout = int(RRAM.read_byte(pyterminal, str(addr), '0', '0x1', False))
        print(f'| ( {row:>3}, {col:>3}) | {golden:>6} | {readout:>7} | {golden-readout:>10} |')
    print('-----------------------------------------------')


def test_bit_cim(pyterminal, row, col):
    """ Test function for computer in memory (CIM) at bit level

    Keyword arguments:
    pyterminal -- current connected COM port
    row -- from '0'~'255'
    col -- from '0'~'255'
    """
    row = int(row)
    col = int(col)

    # Reset first 9 cells
    for row_offset in range(0, 9):
        addr = (row+row_offset) * 256 + col
        RRAM.reset(pyterminal, 'cell', str(addr), True)

    # Set second 9 cells
    for row_offset in range(9, 18):
        addr = (row+row_offset) * 256 + col
        RRAM.set(pyterminal, 'cell', str(addr), True)

    # Compute-In-Memory
    raws = [[''] * 10 for i in range(10)]
    for value in range(0, 10):
        for ones in range(max(1, value), 10):
            row_offset = 9 - ones + value
            addr = (row + row_offset) * 256 + col
            raws[value][ones] = RRAM.read_lane(pyterminal, str(addr), str(hex(2**ones - 1)), False)

    # Print it out nicely
    print('-----------------------------------------------------------------------------------------------')
    print('| Value\Ones |      1 |      2 |      3 |      4 |      5 |      6 |      7 |      8 |      9 |')
    print('-----------------------------------------------------------------------------------------------')
    for value in reversed(range(0, 10)):
        print(f'| {value:>10} |', end='')
        for ones in range(1, 10):
            print(f' {raws[value][ones]:>6} |', end='')
        print('')
    print('-----------------------------------------------------------------------------------------------')

    return raws


def test_byte_cim(pyterminal, row, col, num):
    """ Test function for computer in memory (CIM) at byte level

    Keyword arguments:
    pyterminal -- current connected COM port
    row -- from '0'~'255'
    col -- from '0'~'255'
    num -- from '1'~'9'
    """
    row = int(row)
    col = int(col)
    num = int(num)
    values = [0] * num
    goldens = [0] * (2**num)
    readouts = [0] * (2**num)

    # Write the values
    for n in range(num):
        addr = (row+n) * 256 + col
        values[n] = random.randint(-128, 127)
        print(f'Writing {values[n]:>4} to ( {row+n:>3}, {col:>3})')
        RRAM.write_byte_iter(pyterminal, str(addr), str(values[n]), False)

    # Compute the goldens
    for n in range(1, 2**num):
        for i in range(num):
            if n & 2**i:
                goldens[n] += values[i]

    # CIM
    for n in range(1, 2**num):
        readouts[n] = int(RRAM.read_byte(pyterminal, str(row*256 + col), '0', hex(n), False))

    # Print the result nicely
    print('----------------------------------------')
    print('| Data | Readout | Golden | Difference |')
    print('----------------------------------------')
    for n in range(1, 2**num):
        print(f'| {hex(n):>4} | {readouts[n]:>7} | {goldens[n]:>6} | {goldens[n]-readouts[n]:>10} |')
    print('----------------------------------------')

def parse_endurance_params(pyterminal, args): #unused at the moment
    opts, args = getopt.getopt(sys.argv, "s:r:c:n:", ["startAddress=", "nRows=", "nCols=", "nCycles="])

def time_commands(pyterminal, command):
    """
    simple method to time operations. Note that this also includes the time for python code to execute

    :param pyterminal: current connected COM port
    :param command: command to run through the terminal, separate multiple commands with ","
    :return: None
    """
    #time and execute commands
    totalTime = 0
    for subCommand in command.split(","):
        subCommand = subCommand.strip()
        print("#####executing:", subCommand)
        startTime = time.time_ns()
        pyterminal.decode_command(subCommand)
        endTime = time.time_ns()
        totalTime += endTime-startTime
    print(f"total time: {totalTime}ns")

def test_endurance_master(pyterminal, addr=0, nCells=1, nCycles=-1):
    """
    controller for endurance testing, capable of ending the infinite run prematurely
    """
    stop = multiprocessing.Value('i')
    stop.value = 0
    testProcess = multiprocessing.Process(target=test_endurance, args=(None, stop, addr, nCells, nCycles), name="Test Runner")
    testProcess.start()
    while input() != ':q':
        continue
    stop = True
    testProcess.join()

def test_endurance(pyterminal, addr=0, nCells=1, nCycles=-1, readStep=1):
    """
    Test endurance of n cells starting at address
    :param pyterminal: current connected COM port
    :param addr: starting address
    :param nCells: number of cells to test after starting address
    :param nCycles: maximum number of cycles to run if no cell fails, or -1 to continue till failure
    :param readStep: number of set/reset cycles in between reading the cells
    :return:
    """

    cycle_list = []
    currentCycle = 0
    fail = False
    nCycles = int(nCycles)
    readStep = int(readStep)
    try:
        while currentCycle != nCycles and not fail:
            currentCycle += 1
            if currentCycle % readStep == 0:
                address_dict = {}
                #set
                for address in range(int(addr), int(addr) + int(nCells)):
                    address = str(address)
                    address_dict[address] = {}
                    start_time = time.time_ns()
                    RRAM.set(pyterminal, 'cell', address, False)
                    end_time = time.time_ns()
                    address_dict[address]['time'] = end_time - start_time

                #read set result

                for address in range(int(addr), int(addr) + int(nCells)):
                    address = str(address)
                    start_time = time.time_ns()
                    address_dict[address]['set_value'] = RRAM.read_lane(pyterminal, address, '0x1', False)
                    end_time = time.time_ns()
                    address_dict[address]['time'] += end_time - start_time

                # reset
                for address in range(int(addr), int(addr) + int(nCells)):
                    address = str(address)
                    start_time = time.time_ns()
                    RRAM.reset(pyterminal, 'cell', address, False)
                    end_time = time.time_ns()
                    address_dict[address]['time'] += end_time - start_time

                # read reset result
                for address in range(int(addr), int(addr) + int(nCells)):
                    address = str(address)
                    start_time = time.time_ns()
                    address_dict[address]['reset_value'] = RRAM.read_lane(pyterminal, address, '0x1', False)
                    end_time = time.time_ns()
                    if int(address_dict[address]['reset_value'], 16) <= int(address_dict[address]['set_value'], 16):
                        fail = True
                    address_dict[address]['time'] += end_time - start_time


                cycle_list.append(address_dict)

                # Print the result nicely
                print("Cycle:", currentCycle)
                print('---------------------------------------------')
                print('| Address | Set Value | Reset Value | Cycle Time (ns) |')
                print('---------------------------------------------')
                for address, data in address_dict.items():
                    print(f'| {address:>7} | {data["set_value"]:>9} | {data["reset_value"]:>11} | {data["time"]:>15} |')
            else:
                #set
                for address in range(int(addr), int(addr) + int(nCells)):
                    address = str(address)
                    RRAM.set(pyterminal, 'cell', address, False)
                #reset
                for address in range(int(addr), int(addr) + int(nCells)):
                    address = str(address)
                    RRAM.reset(pyterminal, 'cell', address, False)
    except KeyboardInterrupt:
        pass

    total_time = 0
    for address_dict in cycle_list:
        subTotal = 0
        for address in address_dict.keys():
            subTotal += address_dict[address]['time']
        total_time += subTotal * readStep
    print(f"total time: {total_time}ns")

def unknown(parameters):
    """ Print out the unknown command

    Keyword arguments:
    parameters -- the split version of the command
    """
    print('Unknown Command: ' + ' '.join(parameters) + '(From PyTerminal)')


def decode(pyterminal, parameters):
    """ Decode the split version of the command

    Keyword arguments:
    pyterminal -- current connected COM port
    parameters -- split version of the command
    """
    if   parameters[1] == 'clear'            : clear                    (pyterminal)
    elif parameters[1] == 'read'             : read                     (pyterminal, parameters[2], parameters[3])
    elif parameters[1] == 'calibrate_VTGT_BL': calibrate_VTGT_BL        (pyterminal, parameters[2], parameters[3])
    elif parameters[1] == 'sweep_chip_VRef'  : sweep_chip_VRef          (pyterminal)
    elif parameters[1] == 'test_write_byte'  : test_write_byte          (pyterminal, parameters[2], parameters[3])
    elif parameters[1] == 'test_bit_cim'     : test_bit_cim             (pyterminal, parameters[2], parameters[3])
    elif parameters[1] == 'test_byte_cim'    : test_byte_cim            (pyterminal, parameters[2], parameters[3], parameters[4])
    elif parameters[1] == 'test_endurance'   : test_endurance           (pyterminal, parameters[2], parameters[3], parameters[4], parameters[5])
    elif parameters[1] == "time_commands"    : time_commands            (pyterminal, " ".join(parameters[2:]))
    else: unknown(parameters)
