import PyTerminal as PT
from EnduranceTest import SAF

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
    if   parameters[1] == "SAF"               : SAF(parameters[2])
    else: PT.unknown(parameters)
