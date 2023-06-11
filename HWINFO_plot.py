import csv
import matplotlib.pyplot as plt
from datetime import datetime

"""
filenames = ["Win10 Normal OS/June 9 2023 Prime95 Torture Test Small FFTs Case Closed.CSV",
             "Win10 Normal OS/June 9 2023 Prime95 Torture Test Small FFTs No Sidepanels.CSV",
             "Win10 Normal OS/June 10 2023 Prime95 Torture Test Small FFTs No Sidepanels or front or top.CSV",
             "Win10 Normal OS/June 10 2023 Prime95 Torture Test Small FFTs No Sidepanels or front or top no blowie.CSV"]
"""
"""
filenames = ["Win11 Benchmark OS/June 10 2023 Prime95 no blower fan.CSV",
             "Win11 Benchmark OS/June 10 2023 Prime95 no sidepanels no blower fan.CSV",
             "Win11 Benchmark OS/June 10 2023 Prime95 no sidepanels no top no front no blower fan.CSV",
             "Win11 Benchmark OS/June 10 2023 Prime95 5GHz New Fan Curve No Blower.CSV",
             "Win11 Benchmark OS/June 10 2023 Prime95 New Fan Curve No Blower.CSV"]
"""
filenames = ["Laptop Win10/June 10 2023 Laptop Performance Mode Prime95.CSV",
             "Laptop Win10/June 10 2023 Laptop Standard Mode Prime95.CSV",
             "Laptop Win10/June 10 2023 Laptop Whisper Mode Prime95.CSV"]

"""
legend = ["Prime95 Case Closed",
          "Prime95 No Sidepanels",
          "Prime95 No Sidepanels, Top, or Front Panel",
          "Prime95 No Sidepanels, Top, or Front Panel, No Blower Fan"]
"""
"""
legend = ["Win11 Prime95 No Blower Fan",
          "Win11 Prime95 No Sidepanels, No Blower Fan",
          "Win11 Prime95 No Sidepanels, Top, or Front Panel, No Blower Fan",
          "Win11 Prime95 5GHz New Fan Curve No Blower Fan",
          "Win11 Prime95 New Fan Curve No Blower Fan"]
"""
legend = ["Laptop Prime95 Performance Mode",
          "Laptop Prime95 Standard Mode",
          "Laptop Prime95 Whisper Mode"]


number_of_runs = len(filenames)

max_seconds = 600 # the average still uses points after this, this will set xlim

ignore_first_n_datapoints_for_average = 20

assert (len(filenames) == len(legend)), "different number of filenames and legends"

cpu_temperatures: list[list[float]] = []
room_temperatures: list[list[float]] = []
cpu_temperature_deltas: list[list[float]] = []
cpu_powers: list[list[float]] = []
timestamps: list[list[float]] = []


def find_index(string: str, list_to_look_in: list[str]) -> int:
    """
    finds the index in the list which contains string
    """
    index = 0
    for item in list_to_look_in:
        if item.find(string) != -1:
            break
        index += 1

    return index


i = -1
for filename in filenames:
    i += 1
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader] # read the whole file

    # find column indices of variables
    cpu_temp_column = find_index("CPU Package", rows[0])
    room_temp_column = find_index("T_Sensor1", rows[0])
    cpu_power_column = find_index("CPU Package Power", rows[0])

    initial_time = datetime.strptime(rows[1][0] + ' ' + rows[1][1].split(".")[0], '%d.%m.%Y %H:%M:%S')

    # Initialize lists to store the data
    timestamps.append([])
    cpu_temperatures.append([])
    room_temperatures.append([])
    cpu_temperature_deltas.append([])
    cpu_powers.append([])

    for row in rows[1:]:
        try:
            timestamp = (datetime.strptime(row[0] + ' ' + row[1].split(".")[0], '%d.%m.%Y %H:%M:%S') - initial_time).total_seconds() # Combine date and time columns
        except ValueError:
            continue # the last couple rows are headers for some reason, so datetime doesn't know how to convert a string of characters to time

        cpu_temp = float(row[cpu_temp_column])
        cpu_power = float(row[cpu_power_column])
        room_temp = float(row[room_temp_column])

        # Append the data to the lists
        timestamps[i].append(timestamp)
        cpu_temperatures[i].append(cpu_temp)
        cpu_temperature_deltas[i].append(cpu_temp - room_temp)
        cpu_powers[i].append(cpu_power)


legend = [legend[int(i/2)] if i%2 == 0 else "Average" for i in range(len(legend)*2)]

# Plot 0: CPU package temps
plt.figure(0)
for i in range(number_of_runs):
    plt.scatter(timestamps[i], cpu_temperatures[i], s = 3)

    average_y = sum(cpu_temperatures[i][ignore_first_n_datapoints_for_average:]) / len(cpu_temperatures[i][ignore_first_n_datapoints_for_average:])
    start_end_x = (timestamps[i][0], max_seconds)
    plt.plot(start_end_x, [average_y, average_y], linewidth = 3) # average temp "trendline"

    plt.ylabel('CPU Package Temperature (°C)')
    plt.title('CPU Package Temperature Over Time')
    plt.xticks(rotation=45)
    plt.yticks(tuple(range(10, 105, 5)))
    plt.ylim((10, 105))
    plt.xlim((0, max_seconds))
    plt.tight_layout()

plt.legend(legend)


# Plot 1: CPU package to room temp deltas
plt.figure(1)
for i in range(number_of_runs):
    plt.scatter(timestamps[i], cpu_temperature_deltas[i], s = 3)

    average_y = sum(cpu_temperature_deltas[i][ignore_first_n_datapoints_for_average:]) / len(cpu_temperature_deltas[i][ignore_first_n_datapoints_for_average:])
    start_end_x = (timestamps[i][0], max_seconds)
    plt.plot(start_end_x, [average_y, average_y], linewidth = 3) # average temp "trendline"

    plt.xlabel('Time')
    plt.ylabel('CPU Package Temperature Delta from Room Temperature (°C)')
    plt.title('CPU Package-Room Delta Temperature Over Time')
    plt.xticks(rotation=45)
    plt.yticks(tuple(range(0, 90, 5)))
    plt.ylim((0, 90))
    plt.xlim((0, max_seconds))
    plt.tight_layout()

plt.legend(legend)


# Plot 2: Fan RPM?


# Plot 3: CPU Package Power
plt.figure(3)
for i in range(number_of_runs):
    plt.scatter(timestamps[i], cpu_powers[i], s = 3)

    average_y = sum(cpu_powers[i][ignore_first_n_datapoints_for_average:]) / len(cpu_powers[i][ignore_first_n_datapoints_for_average:])
    start_end_x = (timestamps[i][0], max_seconds)
    plt.plot(start_end_x, [average_y, average_y], linewidth = 3) # average temp "trendline"

    plt.xlabel('Time')
    plt.ylabel('CPU Package Power (W)')
    plt.title('CPU Package Power Over Time')
    plt.xticks(rotation=45)
    plt.yticks(tuple(range(0, 200, 5)))
    plt.ylim((0, 200))
    plt.xlim((0, max_seconds))
    plt.tight_layout()

plt.legend(legend)


plt.show()
