import EnduranceTest
import PyTerminal as PT
from EnduranceTest import *
import re

def example_function():
    """ Example function

    """
    print("This is an example function, feel free to add more of yours in this module")

def check_overformed(filename):
    """
    use data collected in a stuck at fault test to attempt to pull overformed cells back into function
    :param filename: module data file, should have the form saf_m<module number>_c<any number, mainly used in endurance>.npy
    :return: none
    """
    object = np.load(file=filename, allow_pickle=True).item()
    # extract cells
    status = np.ndarray(shape=(256, 256), dtype=dict)
    lrs_average = 0
    hrs_average = 0
    num_stuck = 0
    stuck_cells = []
    for row in range(len(object['status'])):
        for column in range(len(object['status'][row])):
            status[row][column] = object['status'][row][column]
            if status[row][column]['saf'] == True:
                stuck_cells.append(((row, column), status[row][column]))
                num_stuck += 1
            else:
                lrs_average += status[row][column]['lrs']
                hrs_average += status[row][column]['hrs']
    n_alive = (256 ** 2) - num_stuck
    lrs_average /= n_alive
    hrs_average /= n_alive

    stuck_lrs = 0
    stuck_hrs = 0
    # check closeness to average
    cells_to_test = []
    
    for cell in stuck_cells:
        average_adc = np.average([cell[1]['lrs'], cell[1]['hrs']])
        if np.abs(average_adc - lrs_average) < np.abs(average_adc - hrs_average):
            print(f"Address: {cell[0][0] * 256 + cell[0][1]}, Stuck in  LRS")
        else:
            print(f"Address: {cell[0][0] * 256 + cell[0][1]}, Stuck in  HRS")

    RRAM.module(action='set', target=re.findall('[0-9]+', filename)[0], verbal=False)

    # set read, set, reset parameters TODO: make set and reset voltages input
    RRAM.conf_read(cycle='5', verbal=False)
    RRAM.conf_set(AVDD_WR=str(2200), AVDD_WL=str(1200), cycle=str(16), times=str(10), verbal=False)
    RRAM.conf_reset(AVDD_WR=str(2800), AVDD_WL=str(2800), cycle=str(100), times=str(10), verbal=False)

    # set weird adc settings to 0
    RRAM.adc(action='set', action_type='cal', target='0', verbal=False)
    RRAM.adc(action='set', action_type='hbias', target='0', verbal=False)

    # set target bitline voltage 2-200mV
    Board.DAC.set_source(value="200", target='VTGT_BL', verbal=False)

    # configure ADC to have good resolution in expected range of cell voltages
    RRAM.conf_ADC(offset='5', step='8')



def decode(parameters):
    """ Decode the command

    Args:
        parameters (list): Command in List form.
    """
    parameters = list(filter(None, parameters))
    if   parameters[1] == 'example_function'  : example_function()
    if   parameters[1] == "ENDURANCE"         : EnduranceTest.decode(parameters[2:])
    else: PT.unknown(parameters)
