import argparse
import json
import os
import matplotlib.pyplot as plt

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_metrics(data):
    return {
        'numberOfDrones': data['numberOfDrones'],
        'numberOfRechargePoints': data['numberOfRechargePoints'],
        'numberOfHASPs': data['numberOfHASPs'],
        'userLatency': sum(data['userLatency']) / len(data['userLatency']),  # Promedio de latencia
        'userPathLoss': sum(data['userPathLoss']) / len(data['userPathLoss']),  # Promedio de path loss
        'userBandWidth': sum(data['userBandWidth']) / len(data['userBandWidth']),  # Promedio de ancho de banda
        'coverage': sum(data['isUserCovered']) / len(data['isUserCovered'])  # Porcentaje de usuarios cubiertos
    }

def plot_metrics_grouped(metrics_list, titles, xlabel):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs = axs.flatten()
    
    for idx, metrics in enumerate(metrics_list):
        axs[idx].plot(metrics['x'], metrics['y'], marker='o')
        axs[idx].set_xlabel(xlabel)
        axs[idx].set_ylabel(titles[idx])
        axs[idx].set_title(titles[idx])
        axs[idx].grid(True)
    
    plt.tight_layout()
    plt.show()

def main(instancia):
    directory = f"C:\\Users\\jorge\\jgomezgi\\Universidad\\8cuatri\\tfg\\src\\minizinc\\results\\{instancia}"
    files = [f for f in os.listdir(directory) if f.endswith('.json')]

    drones_results = {'latency': {'x': [], 'y': []}, 'pathloss': {'x': [], 'y': []}, 'bandwidth': {'x': [], 'y': []}, 'coverage': {'x': [], 'y': []}}
    rp_results = {'latency': {'x': [], 'y': []}, 'pathloss': {'x': [], 'y': []}, 'bandwidth': {'x': [], 'y': []}, 'coverage': {'x': [], 'y': []}}
    hasp_results = {'latency': {'x': [], 'y': []}, 'pathloss': {'x': [], 'y': []}, 'bandwidth': {'x': [], 'y': []}, 'coverage': {'x': [], 'y': []}}

    for file_name in files:
        data = load_data(os.path.join(directory, file_name))
        metrics = extract_metrics(data)

        drones_results['latency']['x'].append(metrics['numberOfDrones'])
        drones_results['latency']['y'].append(metrics['userLatency'])
        drones_results['pathloss']['x'].append(metrics['numberOfDrones'])
        drones_results['pathloss']['y'].append(metrics['userPathLoss'])
        drones_results['bandwidth']['x'].append(metrics['numberOfDrones'])
        drones_results['bandwidth']['y'].append(metrics['userBandWidth'])
        drones_results['coverage']['x'].append(metrics['numberOfDrones'])
        drones_results['coverage']['y'].append(metrics['coverage'])

        rp_results['latency']['x'].append(metrics['numberOfRechargePoints'])
        rp_results['latency']['y'].append(metrics['userLatency'])
        rp_results['pathloss']['x'].append(metrics['numberOfRechargePoints'])
        rp_results['pathloss']['y'].append(metrics['userPathLoss'])
        rp_results['bandwidth']['x'].append(metrics['numberOfRechargePoints'])
        rp_results['bandwidth']['y'].append(metrics['userBandWidth'])
        rp_results['coverage']['x'].append(metrics['numberOfRechargePoints'])
        rp_results['coverage']['y'].append(metrics['coverage'])

        hasp_results['latency']['x'].append(metrics['numberOfHASPs'])
        hasp_results['latency']['y'].append(metrics['userLatency'])
        hasp_results['pathloss']['x'].append(metrics['numberOfHASPs'])
        hasp_results['pathloss']['y'].append(metrics['userPathLoss'])
        hasp_results['bandwidth']['x'].append(metrics['numberOfHASPs'])
        hasp_results['bandwidth']['y'].append(metrics['userBandWidth'])
        hasp_results['coverage']['x'].append(metrics['numberOfHASPs'])
        hasp_results['coverage']['y'].append(metrics['coverage'])

    # Ordenar resultados por número de drones, RP y HASPs para una visualización más clara
    for key in drones_results.keys():
        drones_results[key]['x'], drones_results[key]['y'] = zip(*sorted(zip(drones_results[key]['x'], drones_results[key]['y'])))
        rp_results[key]['x'], rp_results[key]['y'] = zip(*sorted(zip(rp_results[key]['x'], rp_results[key]['y'])))
        hasp_results[key]['x'], hasp_results[key]['y'] = zip(*sorted(zip(hasp_results[key]['x'], hasp_results[key]['y'])))

    # Crear listas de métricas para plotear en subplots
    metrics_list_drones = [drones_results['latency'], drones_results['pathloss'], drones_results['bandwidth'], drones_results['coverage']]
    titles_drones = ['Latencia', 'Pérdida de Señal', 'Ancho de Banda', 'Cobertura']
    
    metrics_list_rp = [rp_results['latency'], rp_results['pathloss'], rp_results['bandwidth'], rp_results['coverage']]
    titles_rp = ['Latencia', 'Pérdida de Señal', 'Ancho de Banda', 'Cobertura']
    
    metrics_list_hasp = [hasp_results['latency'], hasp_results['pathloss'], hasp_results['bandwidth'], hasp_results['coverage']]
    titles_hasp = ['Latencia', 'Pérdida de Señal', 'Ancho de Banda', 'Cobertura']

    plot_metrics_grouped(metrics_list_drones, titles_drones, 'Número de Drones')
    plot_metrics_grouped(metrics_list_rp, titles_rp, 'Número de Puntos de Recarga')
    plot_metrics_grouped(metrics_list_hasp, titles_hasp, 'Número de HASPs')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert JSON to DZN format.')
    parser.add_argument('instancia', type=str, help='Path to the input JSON file')

    
    args = parser.parse_args()

    print(args.json_file)

    main(args.instancia)
