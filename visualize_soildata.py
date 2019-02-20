import json
import statistics as stats
import matplotlib.pyplot as plt

with open('data.json', 'r') as f:
    data = json.load(f)

value_data = {}
voltage_data = {}

for vals in data['values']:
    if str(vals['pin']) not in value_data:
        value_data[str(vals['pin'])] = []
    value_data[str(vals['pin'])].append(vals['val'])

for vals in data['voltages']:
    if str(vals['pin']) not in voltage_data:
        voltage_data[str(vals['pin'])] = []
    voltage_data[str(vals['pin'])].append(vals['val'])

def graph_voltages():
    for key in voltage_data:
        y = voltage_data[key]
        N = len(y)
        x = range(N)
        plt.bar(x, y, color='blue')
        plt.ylim([0, 3.5])
        plt.show()

def graph_values():
    for key in value_data:
        y = value_data[key]
        N = len(y)
        x = range(N)
        plt.bar(x, y, color='blue')
        plt.ylim([45000, 65000])
        plt.show()

def voltage_statistics():
    for key in voltage_data:
        data = voltage_data[key]
        minimum = min(data)
        maximum = max(data)
        median = stats.median(data)
        stdev = stats.stdev(data)
        print('--- sensor ' + key + ' ---')
        print('min: ' + str(minimum))
        print('max: ' + str(maximum))
        print('median: ' + str(median))
        print('std: ' + str(stdev))
        print('---------------')

def value_statistics():
    for key in value_data:
        data = value_data[key]
        minimum = min(data)
        maximum = max(data)
        median = stats.median(data)
        stdev = stats.stdev(data)
        print('--- sensor ' + key + ' ---')
        print('min: ' + str(minimum))
        print('max: ' + str(maximum))
        print('median: ' + str(median))
        print('std: ' + str(stdev))
        print('---------------')

value_statistics()
#voltage_statistics()
#graph_values()
#graph_voltages()
