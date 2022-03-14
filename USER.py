import EnduranceTest
import PyTerminal as PT
from EnduranceTest import *
from READ import READ

def example_function():
    """ Example function

    """
    print("This is an example function, feel free to add more of yours in this module")


def decode(parameters):
    """ Decode the command

    Args:
        parameters (list): Command in List form.
    """
    parameters = list(filter(None, parameters))
    if   parameters[1] == 'example_function'  : example_function()
    if   parameters[1] == "ENDURANCE"         : EnduranceTest.decode(parameters[2:])
    if   parameters[1] == 'READ'              : READ (parameters[2], parameters[3], parameters[4] )
    else: PT.unknown(parameters)
