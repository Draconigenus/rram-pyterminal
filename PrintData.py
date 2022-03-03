#loads numpy file and attempts to print its data in a readable manner
import pprint
import sys

import matplotlib.pyplot
import numpy as np


def main(filename):
    status, stuck_percent = getSAFstatus(filename)
    status_display = matplotlib.pyplot.pcolormesh(status)
    matplotlib.pyplot.title("%stuck=" + str(stuck_percent))
    matplotlib.pyplot.savefig("Plots/" + filename.split(sep="/")[-1][:-4] + ".png")

def evaluateLRS(filename):
    object = np.load(file=filename, allow_pickle=True).item()
    # extract cells
    LRS = []
    for addr, data in object["resistances"].items():
        LRS.append(data["LRS"])
    print(f"mean: {np.mean(LRS)}, std: {np.std(LRS)}")


def evaluateResistance(filename):
    object = np.load(file=filename, allow_pickle=True).item()
    #extract cells
    deltas = []
    for addr, data in object["resistances"].items():
        deltas.append(data["Delta"])

    mean = np.mean(deltas)
    stdev = np.std(deltas)

    trimmed = []
    for delta in deltas:
        if abs((delta - mean)) < stdev * 2:
            trimmed.append(delta)
    print("Number of samples after trimming: " + str(len(trimmed)))
    print(f"mean: {np.mean(trimmed)}, std: {np.std(trimmed)}")


def getSAFstatus(filename):
    object = np.load(file=filename, allow_pickle=True).item()
    # extract cells
    status = np.ndarray(shape=(256, 256), dtype=bool)
    num_stuck = 0
    for row in range(len(object['status'])):
        for column in range(len(object['status'][row])):
            status[row][column] = object['status'][row][column]['saf']
            if status[row][column] == True:
                num_stuck += 1
    stuck_percent = round((float(num_stuck) / (256 ** 2)) * 100, ndigits=4)
    return status, stuck_percent

def combinePlots():
    files = ["Data/saf_m16_c1.npy",
             "Data/saf_m26_c1.npy",
             "Data/saf_m24_c1.npy",
             "Data/saf_m35_c1.npy",
             "Data/saf_m12_c1.npy",
             "Data/saf_m20_c1.npy"]
    voltages = [3000,
                3100,
                3250,
                3300,
                3500,
                4000]

    plt = matplotlib.pyplot.figure(figsize=[15,15])
    for i in range(len(files)):
        status, stuck_percent = getSAFstatus(files[i])
        subplt = plt.add_subplot(3, 2, i + 1)
        subplt.pcolormesh(status)
        subplt.set_title(f"Form Write Voltage: {voltages[i]}mV    Stuck Cells: {stuck_percent}%")
        subplt.autoscale(enable=True)
    plt.suptitle("Stuck at Fault % Across Formation Write Voltages")
    plt.tight_layout()
    plt.savefig("Plots/FormingVoltages.png")



if __name__ == "__main__":
    main(sys.argv[1])