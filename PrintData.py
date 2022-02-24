#loads numpy file and attempts to print its data in a readable manner
import pprint
import sys

import matplotlib.pyplot
import numpy as np


def main(filename):
    object = np.load(file=filename, allow_pickle=True).item()
    #extract cells
    status = np.ndarray(shape=(256,256), dtype=bool)
    num_stuck = 0
    for row in range(len(object['status'])):
        for column in range(len(object['status'][row])):
            status[row][column]= object['status'][row][column]['saf']
            if status[row][column] == True:
                num_stuck += 1
    print(num_stuck)
    stuck_percent = round((float(num_stuck) / (256 ** 2)) * 100, ndigits=4)
    status_display = matplotlib.pyplot.pcolormesh(status)
    matplotlib.pyplot.title("%stuck=" + str(stuck_percent))
    matplotlib.pyplot.savefig("Plots/" + filename.split(sep="/")[-1][:-4] + ".png")

if __name__ == "__main__":
    main(sys.argv[1])