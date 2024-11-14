import argparse
import json
import os
import math
import matplotlib.pyplot as plt
import tools
from collections import defaultdict

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_metrics(data):
    return {
        'numberOfDrones': data['numberOfDrones'],
        'numberOfRechargePoints': data['numberOfRechargePoints'],
        'userLatency': sum( data['userLatency'][i] * data['isUserCovered'][i] * data['CellDist'] /300000 for i in range (len(data['userLatency'])) ) / sum(data['isUserCovered']),
        'userPathLoss': sum( (4 * math.pi * data['userPathLoss'][i] * data['CellDist'] * data['isUserCovered'][i] )/0.0107  for i in range (len(data['userPathLoss'])) ) / sum(data['isUserCovered']),
        'userBandWidth': sum( data['userBandWidth'][i] * data['isUserCovered'][i] for i in range (len(data['userBandWidth'])) ) / sum(data['isUserCovered']),
        'coverage': sum(data['isUserCovered']) / len(data['isUserCovered']),
        'averageDistanceToRP': calculate_average_distance_drones_rp(data['DronePosition'], data['ClosestRP'], data['RechargePointPosition'], data['numberOfDrones'])
    }

def calculate_average_distance_drones_rp(DronePosition, closestRP, RechargePointPosition, numberOfDrones):
    total_distance = 0
    for i, drone in enumerate(DronePosition):
        print("Calculating distance between ", drone, " and ", RechargePointPosition[closestRP[i]-1], "...", closestRP[i])
        # print(calculate_manhattan_distance(DronePosition[i][0], DronePosition[i][1], RechargePointPosition[closestRP[i]-1][0], RechargePointPosition[closestRP[i]-1][1]))
        total_distance += tools.distancia_manhattan(DronePosition[i], RechargePointPosition[closestRP[i]-1])
        print(tools.distancia_manhattan(DronePosition[i], RechargePointPosition[closestRP[i]-1]))
        # total_distance += calculate_manhattan_distance(DronePosition[i][0], DronePosition[i][1], RechargePointPosition[closestRP[i]-1][0], RechargePointPosition[closestRP[i]-1][1])
    return total_distance / numberOfDrones

def calculate_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def plot_metrics(drones_results, title, filename):
    # Configurar el tamaño de las fuentes
    plt.rcParams.update({
        'font.size': 18,          # Tamaño de la fuente general
        'axes.titlesize': 20,     # Tamaño del título del gráfico
        'axes.labelsize': 16,     # Tamaño de las etiquetas de los ejes
        'xtick.labelsize': 14,    # Tamaño de las etiquetas del eje x
        'ytick.labelsize': 14,    # Tamaño de las etiquetas del eje y
        'legend.fontsize': 16,    # Tamaño de la fuente de la leyenda
        'figure.titlesize': 18    # Tamaño del título de la figura
    })
    units = {
        'userLatency': 'Ms',
        'userPathLoss': 'dB',
        'userBandWidth': 'MBps',
        'coverage': 'Porcentaje',
        'averageDistanceToRP': 'Cells'
    }

    title = f"{title} ({units.get(title, '')})"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    for rp, metrics in drones_results.items():
        ax.plot(metrics['x'], metrics['y'], label=f'RP {rp}')
    
    ax.set_xlabel('Número de Drones')
    ax.set_ylabel(title)
    ax.set_title(title)
    ax.grid(True)
    ax.legend(title='Número de Puntos de Recarga')
    plt.tight_layout()
    os.makedirs("results/plots", exist_ok=True)
    plt.savefig(f"results/plots/{filename}")
    print(f"results saved in results/plots/{filename}")
    plt.close()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Análisis de resultados.')
    parser.add_argument('instancia', type=str, help='Directorio con archivos de resultados')
    try:
        args = parser.parse_args()
        instancia = args.instancia.replace(".", "")
    except:
        instancia = "results//instancia3"
        # directory = f"results\\instancia3"  # Actualiza esto según tu estructura de directorio
    # path = "C:\\Users\\jorge\\jgomezgi\\Universidad\\8cuatri\\tfg\\src\\minizinc\\results\\instancia3"

    path = os.path.dirname(os.path.abspath(__file__))
    # print(path)
    results_dir = path + instancia
    # print(results_dir)

    results = {
        'userLatency': defaultdict(lambda: {'x': [], 'y': []}),
        'userPathLoss': defaultdict(lambda: {'x': [], 'y': []}),
        'userBandWidth': defaultdict(lambda: {'x': [], 'y': []}),
        'coverage': defaultdict(lambda: {'x': [], 'y': []}),
        'averageDistanceToRP': defaultdict(lambda: {'x': [], 'y': []})
    }

    file_names = sorted(os.listdir(results_dir))
    for file_name in file_names:
        file_name = results_dir + "\\" + file_name
        print(file_name)
        data = load_data(file_name)
        metrics = extract_metrics(data)

        for key in results:
            rp = metrics['numberOfRechargePoints']
            results[key][rp]['x'].append(metrics['numberOfDrones'])
            results[key][rp]['y'].append(float(metrics[key]))
        
        # print(metrics)
        # input()
    # print(results)
    for metric, data in results.items():
        instancia_name = instancia.replace('//', '_').replace('\\', '_')
        file_figure_name = f"{metric}_{instancia_name}.png"
        print(file_figure_name)
        plot_metrics(data, metric, file_figure_name)