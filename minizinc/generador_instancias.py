import json
import argparse
import os

def json_to_dzn(data, dzn_file_path):
    

    # Convertir datos a formato .dzn
    dzn_data = (
    f"numberOfDrones = {data['numberOfDrones']}; % Number of drones\n"
    f"numberOfRechargePoints = {data['numberOfRechargePoints']}; % Number of recharge points\n"
    f"numberOfUsersClusters = {data['numberOfUsersClusters']}; % Number of user clusters\n"
    f"numberOfHAPSs = {data.get('numberOfHAPSs', '')};\n"
    f"M1 = {data['M1']}; % Large enough value\n"
    f"XY = {data['XY']};\n"
    f"CellDist = {data.get('CellDist', '')};\n\n"
    f"% Data\n"
    f"RHAPS = {data.get('RHAPS', '')};\n"
    f"Ri = [{', '.join([str(data['Ri'][0]) for _ in range(data['numberOfDrones'])])}]; % Coverage radius of drones\n"
    f"Bi = [{', '.join([str(data['Bi'][0]) for _ in range(data['numberOfDrones'])])}]; % Battery capacity of drones\n"
    f"Ci = [{', '.join([str(data['Ci'][0]) for _ in range(data['numberOfDrones'])])}]; % Consumption per unit distance of drones\n"
    f"NUsers = {data['NUsers']}; % Number of users in clusters\n"
    f"UserClusterPosition = [| " + "\n       | ".join([f"{pos[0]}, {pos[1]}" for pos in data['UserClusterPosition']]) + " |]; % Position of user clusters\n"
)

    # Guardar datos en archivo .dzn
    path_ejecucion = os.path.dirname(os.path.abspath(__file__))
    print(f"Path ejecucion: {path_ejecucion}")

    dzn_file_path = path_ejecucion + "\\" + dzn_file_path
    print(f"Saving data to {dzn_file_path}")
    try:
        with open(dzn_file_path, 'x') as dzn_file:
            dzn_file.write(dzn_data)
    except FileExistsError:
        print(f"File {dzn_file_path} already exists. Overwriting...")
    except FileNotFoundError:
        print(f"Directory {dzn_file_path} does not exist. Creating directory...")
        os.makedirs(os.path.dirname(dzn_file_path), exist_ok=True)
        with open(dzn_file_path, 'x') as dzn_file:
            dzn_file.write(dzn_data)
   

def dzn_name(data, dzn_file_path, instancia_path):
    ndrones = data['numberOfDrones']
    nRp = data['numberOfRechargePoints']
    nHAPS = data['numberOfHAPSs']
    instancia = instancia_path.split('\\')[-1].split('.')[0]
    dzn_file_path = f"{dzn_file_path}\\instancia_{instancia}_drones_{ndrones}_Rp_{nRp}_HAPS_{nHAPS}.dzn"
    return dzn_file_path

def generate_dzn_instances(json_dir):
    dzn_dir = json_dir.replace("json", "").replace(".", "")

    #eliminamos las instancias anteriores en la carpeta
    # print("dir: ", dzn_dir)
    # print("json_dir: ", json_dir)
    if not os.path.exists(dzn_dir):
        os.makedirs(dzn_dir)
    
    for file in os.listdir(dzn_dir):
        os.remove(f"{dzn_dir}/{file}")
        
    with open(json_dir, 'r') as json_file:
        data = json.load(json_file)

    area = data["XY"]**2
    print("Area:, ", area)
    densidad = sum (data["NUsers"]) / area
    print(densidad)


    #generacion de instancias con diferentes numero de drones y diferentes numero de puntos de recarga
    avg_radius = sum(data["Ri"]) / len(data["Ri"])
    print("avg_radius: ", avg_radius)

    avg_battery = sum(data["Bi"]) / len(data["Bi"])
    avg_consumption = sum(data["Ci"]) / len(data["Ci"])
    
    nDrones = round(area / (3.14 * avg_radius**2))
    print("n Drones:")
    print(nDrones)
    
    nRP = round(area / ( avg_battery/avg_consumption)/2)
    print("n RPs:")
    print(nRP)

    
    for drones in range(2,16):
        data["numberOfDrones"] = drones
        for recharge_points in range(1,3):
            data["numberOfRechargePoints"] = recharge_points
            dzn_file_path = dzn_name(data, dzn_dir, json_dir)
            json_to_dzn(data, dzn_file_path)

    print("Instancias generadas con exito")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON to DZN format.')
    parser.add_argument('json_file', type=str, help='Path to the input JSON file')

    
    args = parser.parse_args()

    print(args.json_file)

    generate_dzn_instances(args.json_file)
