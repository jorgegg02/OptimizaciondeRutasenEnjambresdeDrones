import numpy as np
import math
import json
import argparse
import os
import tools


def parse_minizinc_data(data_string):

    with open(data_string, 'r') as f:
        for line in f:
            if line.startswith('numberOfDrones'):
                global numberOfDrones
                numberOfDrones = int(line.split()[2].replace(";", ""))
            elif line.startswith('numberOfRechargePoints'):
                global numberOfRechargePoints
                numberOfRechargePoints = int(line.split()[2].replace(";", ""))
            elif line.startswith('numberOfUsersClusters'):
                global numberOfUsersClusters
                numberOfUsersClusters = int(line.split()[2].replace(";", ""))
            elif line.startswith('numberOfHAPSs'):
                global numberOfHAPSs
                numberOfHAPSs = int(line.split()[2].replace(";", ""))
                
                
            elif line.startswith('XY'):
                global XY
                XY = int(line.split()[2].replace(";", ""))

            elif line.startswith('CellDist'):
                global CellDist
                CellDist = int(line.split()[2].replace(";", ""))

            elif line.startswith('RHAPS'):
                global RHAPS
                RHAPS = int(line.split()[2].replace(";", ""))
                

            elif line.startswith('Ri'):
                global Ri
                Ri = []
                clean_line = line.split("=")[1].strip().split(";")[0].strip("[").strip("]").strip()  
                # Convert string to list of integers
                Ri = [int(x) for x in clean_line.strip().split(",")]
                
 
            elif line.startswith('NUsers'):
                global NUsers
                NUsers = []
                clean_line = line.split("=")[1].strip().split(";")[0].strip("[").strip("]").strip()  
                # Convert string to list of integers
                NUsers = [int(x) for x in clean_line.strip().split(",")]

            elif line.startswith('UserClusterPosition'):
                global UserClusterPosition
                UserClusterPosition = []
                user_clusters = []
                
                # Remove special characters and leading/trailing spaces
                clean_line = line.split("=")[1]
                
                clean_line = clean_line[3:8]
               
                clean_line = clean_line.strip()
                
                coordinates = clean_line.split(",")
                # print(coordinates)
                user_clusters = ([int(x.strip()) for x in coordinates])
                UserClusterPosition.append(user_clusters)

                for i in range(numberOfUsersClusters-2):
                    line = f.readline()
                    user_clusters = []
                    # print(line)
                    # Remove special characters and leading/trailing spaces
                    clean_line = line.strip().strip("|")
                    # print(clean_line)
                    if not clean_line:  # Skip empty lines
                        continue

                    # Split by comma and space separator
                    coordinates = clean_line.split(", ")
                    # print(coordinates)
                    # Convert strings to integers
                    user_clusters = ([int(x) for x in coordinates])
                    UserClusterPosition.append(user_clusters)
                line = f.readline()

                clean_line = line.split(";")[0]
                clean_line = clean_line.strip("]").strip("|").strip()
                # print(clean_line)
                coordinates = clean_line.split(", ")
                coordinates[0] = coordinates[0][1:]
                # print(coordinates)
                user_clusters = ([int(x) for x in coordinates])
                UserClusterPosition.append(user_clusters)


def print_matrix_user():
    print("  ", end=" ")
    for x in range(1,XY+1):
        print(f"{x:02}", end=" ")
    print()
    for x in range(1,XY+1):
        print(f"{x:02}", end=" ")
        for y in range(1,XY+1):
            
            if [x, y] in UserClusterPosition and [x, y] in RechargePointPosition and [x, y] in HAPSPosition and [x, y] in DronePosition:
                print(" A", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in RechargePointPosition and [x, y] in HAPSPosition:
                print(" B", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in RechargePointPosition:
                print(" C", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in HAPSPosition:
                print(" D", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in DronePosition:
                print(" E", end=" ")
            elif [x, y] in RechargePointPosition and [x, y] in DronePosition:
                print(" F", end=" ")
            elif [x, y] in HAPSPosition and [x, y] in DronePosition:
                print(" G", end=" ")

            elif [x, y] in HAPSPosition and [x, y] in RechargePointPosition:
                print(" M", end=" ")
            
            elif [x, y] in UserClusterPosition:
                print(" U", end=" ")
            elif [x, y] in HAPSPosition:
                print(" H", end=" ")
            elif [x, y] in RechargePointPosition:
                print(" R", end=" ")
            elif [x, y] in DronePosition:
                print(" D", end=" ")
            else:
                print(" -", end=" ")

        print()



def place_drones_grid(XY, num_drones):
    
    matrix = np.zeros((XY, XY))
    positions = []
    
    # Calcula la cantidad de drones por fila y columna
    grid_sizex = int(round(math.sqrt(num_drones)))
    grid_sizey = int(math.ceil(math.sqrt(num_drones)))
    
    # if grid_sizex * grid_sizey < num_drones:

    #     grid_sizex = grid_sizex + (num_drones - grid_sizex*grid_sizey)

    # Determina el espacio entre drones
    step_x = math.floor(XY / grid_sizex)    
    step_y = math.floor(XY / grid_sizey) 
    
    # Ajusta el punto inicial para centrar los drones
    start_x = (XY - step_x * (grid_sizex - 1)) // 2
    start_y = (XY - step_y * (grid_sizey - 1)) // 2
    
    # Coloca los drones en la matriz
    for i in range(grid_sizex):
        remaining = num_drones - len(positions)
        if i == grid_sizex - 1 and remaining > 0:
            step_y = math.floor(XY / remaining)
            start_y = (XY - step_y * (remaining - 1)) // 2

            for j in range(remaining):
                x_pos = start_x + i * step_x
                y_pos = start_y + j * step_y
                positions.append((x_pos, y_pos))
                matrix[x_pos, y_pos] = 1

            break
        for j in range(grid_sizey):
            if len(positions) < num_drones:
                x_pos = start_x + i * step_x
                y_pos = start_y + j * step_y
                positions.append((x_pos, y_pos))
                matrix[x_pos, y_pos] = 1
            
    
    return matrix, positions


def print_matrix(matrix):
    print("  ", end=" ")
    for x in range(1, XY+1):
        print(f"{x:02}", end=" ")
    print()
    for x in range(1, XY+1):
        print(f"{x:02}", end=" ")
        for y in range(1, XY+1):
            if matrix[x-1][y-1] == 0:
                print("- ", end=" ")
            else:
                print("1 ", end=" ")
        print()

def calcular_salida_algoritmos_alternativos( dzn_file):
    
    path_ejecucion = os.path.dirname(os.path.abspath(__file__))
    print(f"Path ejecucion: {path_ejecucion}")

    dzn_file_path = path_ejecucion  +  dzn_file
    print("Parsing data from file: ", dzn_file_path)
    parse_minizinc_data(dzn_file_path)
    global DronePosition, HAPSPosition, RechargePointPosition
    drone_matrix, DronePosition = place_drones_grid(XY, numberOfDrones)
    DronePosition = [list(pos) for pos in DronePosition]
    # print(positions)
    # print_matrix(drone_matrix)
    HAPS_matrix, HAPSPosition = place_drones_grid(XY, numberOfHAPSs)
    HAPSPosition = [list(pos) for pos in HAPSPosition]
    rechagePoint_matrix, RechargePointPosition = place_drones_grid(XY, numberOfRechargePoints)
    RechargePointPosition = [list(pos) for pos in RechargePointPosition]
    
    # print_matrix(drone_matrix)
    # print(DronePosition)
    # print (UserClusterPosition)
    # print_matrix(rechagePoint_matrix)

    DroneHeight = [1 for _ in range(numberOfDrones)]

    userDroneCoverage = [[1 if tools.distancia_manhattan(DronePosition[i], UserClusterPosition[j]) <= Ri[i] else 0  for j in range(numberOfUsersClusters)  ]for i in range(numberOfDrones)]
    isUserCovered = [1 if sum(userDroneCoverage[j][i]  for j in range(numberOfDrones)) > 0 else 0   for i in range(numberOfUsersClusters)]
    
    closestRP = tools.calculate_closest_rp(DronePosition, RechargePointPosition)
    ClosestDrone = tools.calculate_closest_drone(DronePosition, UserClusterPosition)
    userLatency = [ tools.distancia_manhattan(DronePosition[ClosestDrone[j]],UserClusterPosition[j]) + DroneHeight[ClosestDrone[j]] if isUserCovered[j] > 0 else 9999 for j in range(numberOfUsersClusters)]
    userPathLoss = [ (tools.distancia_manhattan(UserClusterPosition[j],DronePosition[ClosestDrone[j]]) + DroneHeight[ClosestDrone[j]]) if isUserCovered[j] > 0 else 9999 for j in range(numberOfUsersClusters)]
    userBandWidth = [ 1000 * isUserCovered[j] / sum(userDroneCoverage[ClosestDrone[j]][i] for i in range(numberOfUsersClusters)) if sum(userDroneCoverage[ClosestDrone[j]][i]for i in range(numberOfUsersClusters)) != 0 else 0     for j in range(numberOfUsersClusters)]

    # print(DronePosition)  

    # print_matrix_user()

    # for i in range(numberOfDrones):
    #     #imprimir numero de usuarios conectados a cada dron
    #     print(f"Drone {i} conectado a {sum(userDroneCoverage[i])} usuarios")

    data = {
        "numberOfDrones": numberOfDrones,
        "numberOfRechargePoints": numberOfRechargePoints,
        "numberOfUsersClusters": numberOfUsersClusters,
        "numberOfHAPSs": numberOfHAPSs,
        "XY": XY,
        "CellDist": CellDist,
        "HAPSPosition": HAPSPosition,
        "RechargePointPosition": RechargePointPosition,
        "DronePosition": DronePosition,
        "NUsers": NUsers,
        "UserClusterPosition": UserClusterPosition,
        "DroneHeight": DroneHeight,
        "isUserCovered": isUserCovered,
        "ClosestRP": closestRP,
        "ClosestDrone": ClosestDrone,
        "userLatency": userLatency,
        "userPathLoss": userPathLoss,
        "userBandWidth": userBandWidth
    }

    # Save the data to a JSON file
    print("dzn_file: ", dzn_file)
    dzn_name = dzn_file.split("\\")[-1].split(".")[0]
    print("dzn_name: ", dzn_name)
    instancia = dzn_name.split('_')[0]
    print("instancia: ", instancia)

    file_name = f'results/results_centralidad/{instancia}/result_{dzn_name}.json'
    print("Saving the data to file: ", file_name)

    os.makedirs(os.path.dirname(file_name), exist_ok=True)  # Create the directory if it doesn't exist
    with open(file_name, 'w') as f:
        json.dump(data, f)
    
    print("Data saved to file: " + file_name)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' directory with dzn files file path')
    parser.add_argument('dzn_directory', type=str, help='Path to the directory with dzn files')

    args = parser.parse_args()

    print(args.dzn_directory)

    for file in os.listdir(args.dzn_directory):
        if file.endswith('.dzn'):
            print(file)
            
            calcular_salida_algoritmos_alternativos(args.dzn_directory.replace(".", "")+ "\\" + file)
    

