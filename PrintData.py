#loads numpy file and attempts to print its data in a readable manner
import pprint
import sys

import matplotlib.pyplot
import numpy as np


def main(filename):
    status, stuck_percent = getSAFstatus(filename)
    matplotlib.pyplot.pcolormesh(status)
    matplotlib.pyplot.title("%stuck=" + str(stuck_percent))
    matplotlib.pyplot.savefig("Plots/" + filename.split(sep="/")[-1][:-4] + ".png")
    matplotlib.pyplot.close()

def arrayWithAccentedFaults(filename, size, round):
    status, stuck_percent = getSAFstatus(filename)

    enlarged_status = np.full(shape=(256,256), dtype=bool, fill_value=False)

    for x in range(len(status)):
        for y in range(len(status[x])):
            if status[x][y] == True:
                for i in range(x - size//2, x + size//2 + 1):
                    for j in range(y - size//2, y + size//2 + 1):
                        if (round == False or np.linalg.norm(np.array([i, j]) - np.array([x, y])) <= size // 2):
                            enlarged_status[min(max(0, i), len(status) - 1)][min(max(0, j), len(status[x]) - 1)] = True
    matplotlib.pyplot.imshow(enlarged_status, cmap="binary", aspect=1, origin='lower')
    matplotlib.pyplot.xticks(np.arange(0, 257, 64))
    matplotlib.pyplot.yticks((np.arange(0, 257, 64)))
    # matplotlib.pyplot.pcolormesh(enlarged_status, cmap='binary')
    # matplotlib.pyplot.title("%stuck=" + str(stuck_percent))
    matplotlib.pyplot.savefig("Plots/" + filename.split(sep="/")[-1][:-4] + f"_res{size}" + ".png", dpi=2000)
    matplotlib.pyplot.close()

def evaluateLRS(filename):
    object = np.load(file=filename, allow_pickle=True).item()
    # extract cells
    LRS = []
    for addr, data in object["resistances"].items():
        LRS.append(data["LRS"])
    print(f"mean: {np.mean(LRS)}, std: {np.std(LRS)}")

def SAFvsvoltage():
    modules = [16, 26, 67, 69, 24, 35, 12, 20]
    voltages = [3000, 3100, 3150, 3200, 3250, 3300, 3500, 4000]
    data = []
    for i in range(len(modules)):
        status, stuck_percent = getSAFstatus(filename=f"Data/saf_m{modules[i]}_c1.npy")
        data.append(stuck_percent)
    matplotlib.pyplot.plot(voltages, data, marker='o')
    matplotlib.pyplot.yscale("log")
    matplotlib.pyplot.savefig("Plots/SAFvsVoltage.png")
    matplotlib.pyplot.close()

def SAFvsVdivided():
    modules = [16, 26, 67, 69,  24, 35, 12, 20]
    voltages = [3000, 3100, 3150, 3200, 3250, 3300, 3500, 4000]
    lrs_stuck = []
    hrs_stuck = []
    total_stuck = []
    for i in range(len(modules)):
        status, total, lrs, hrs = getSAFstatusdivided(filename=f"Data/saf_m{modules[i]}_c1.npy")
        total_stuck.append(total)
        lrs_stuck.append(lrs)
        hrs_stuck.append(hrs)
        print(total, lrs + hrs)

    width = 0.35
    # matplotlib.pyplot.plot(voltages, total_stuck, color='blue')
    matplotlib.pyplot.bar([str(voltage) + "mV" for voltage in voltages], lrs_stuck, width, color='green')
    matplotlib.pyplot.bar([str(voltage) + "mV" for voltage in voltages], hrs_stuck,width, color='orange')
    matplotlib.pyplot.yscale("log")
    matplotlib.pyplot.savefig("Plots/SAFvsVoltageDivided.png")
    matplotlib.pyplot.close()

def SAFvsVcategorized():
    modules = [16, 26, 67, 69, 24, 35, 12, 20]
    voltages = [3000, 3100, 3150, 3200, 3250, 3300, 3500, 4000]
    total_stuck = []
    for i in range(len(modules)):
        status, stuck_percent = getSAFstatus(filename=f"Data/saf_m{modules[i]}_c1.npy")
        total_stuck.append(stuck_percent)
        print(stuck_percent)

    width = 0.35
    # matplotlib.pyplot.plot(voltages, total_stuck, color='blue')
    barlist = matplotlib.pyplot.bar([str(voltage) + "mV" for voltage in voltages], total_stuck, width, color='green')
    for i in range(voltages.index(3250)):
        barlist[i].set_color('orange')
    matplotlib.pyplot.yscale("log")
    matplotlib.pyplot.ylim(10 ** -3, 10 ** 2)
    matplotlib.pyplot.savefig("Plots/SAFvsVoltageCategorized.png", dpi = 2000)
    matplotlib.pyplot.close()

def SAFvspulse():
    modules = [47, 36, 37, 24, 63, 52]
    pulse_widths = [5, 50, 75, 100, 200, 400]
    data = []
    for i in range(len(modules)):
        status, stuck_percent = getSAFstatus(filename=f"Data/saf_m{modules[i]}_c1.npy")
        data.append(stuck_percent)
    plot = matplotlib.pyplot.plot(pulse_widths, data, marker='o')
    matplotlib.pyplot.yscale("log")
    matplotlib.pyplot.savefig("Plots/SAFvsPulse.png")
    matplotlib.pyplot.close()

def SAFvsPdivided():
    modules = [47, 36, 37, 24, 63, 52]
    pulse_widths = [5, 50, 75, 100, 200, 400]
    lrs_stuck = []
    hrs_stuck = []
    total_stuck = []
    for i in range(len(modules)):
        status, total, lrs, hrs = getSAFstatusdivided(filename=f"Data/saf_m{modules[i]}_c1.npy")
        total_stuck.append(total)
        lrs_stuck.append(lrs)
        hrs_stuck.append(hrs)

    width = 0.35
    # matplotlib.pyplot.plot(pulse_widths, total_stuck, marker='o', color='blue')
    matplotlib.pyplot.bar([str(pulse_width) for pulse_width in pulse_widths], lrs_stuck, width, color='green')
    matplotlib.pyplot.bar([str(pulse_width) for pulse_width in pulse_widths], hrs_stuck, width, color='orange')
    matplotlib.pyplot.yscale("log")
    matplotlib.pyplot.savefig("Plots/SAFvsPulseDivided.png")
    matplotlib.pyplot.close()


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
    stuck_percent = (float(num_stuck) / (256 ** 2)) * 100
    return status, stuck_percent

def getSAFstatusdivided(filename):
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
                stuck_cells.append(status[row][column])
                num_stuck += 1
            else:
                lrs_average += status[row][column]['lrs']
                hrs_average += status[row][column]['hrs']
    n_alive = (256 ** 2) - num_stuck
    lrs_average /= n_alive
    hrs_average /= n_alive

    stuck_lrs = 0
    stuck_hrs = 0
    #check closeness to average
    for cell in stuck_cells:
        average_adc = np.average([cell['lrs'],cell['hrs']])
        if np.abs(average_adc - lrs_average) < np.abs(average_adc - hrs_average):
            stuck_lrs += 1
        else:
            stuck_hrs += 1

    stuck_percent = (float(num_stuck) / (256 ** 2)) * 100
    lrs_stuck_percent = (float(stuck_lrs) / (256 ** 2)) * 100
    hrs_stuck_percent = (float(stuck_hrs) / (256 ** 2)) * 100
    return status, stuck_percent, lrs_stuck_percent, hrs_stuck_percent

def listStuckCells(filename):
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
    #check closeness to average
    for cell in stuck_cells:
        average_adc = np.average([cell[1]['lrs'],cell[1]['hrs']])
        if np.abs(average_adc - lrs_average) < np.abs(average_adc - hrs_average):
            print(f"Address: {cell[0][0] * 256 + cell[0][1]}, Stuck in  LRS")
        else:
            print(f"Address: {cell[0][0] * 256 + cell[0][1]}, Stuck in  HRS")

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
    matplotlib.pyplot.close()



if __name__ == "__main__":
    main(sys.argv[1])