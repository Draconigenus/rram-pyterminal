import PyTerminal as PT
from resistance import measure_resistance
from endurance import endurance

def example_function():
    """ Example function

    """
    print("This is an example function, feel free to add more of yours in this module")


def decode(parameters):
    """ Decode the command

    Args:
        parameters (list): Command in List form.
    """
    if   parameters[1] == 'example_function'  : example_function()
    elif parameters[1] == 'resistance'        : measure_resistance (parameters[2], parameters[3])
    elif parameters[1] == 'endurance'         : endurance (parameters[2], parameters[3])
    else: PT.unknown(parameters)
