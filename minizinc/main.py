import subprocess
import time
import numpy as np
import json
import os
import argparse
import tools


numberOfDrones = 0
numberOfRechargePoints = 0
numberOfUsersClusters = 0
numberOfHAPSs = 0
XY = 0
HAPSPosition = []
RechargePointPosition = []
DronePosition = []
NUsers = []
UserClusterPosition = []
DroneHeight = []


def execute_minizinc(mzn_file, dzn_file,timeout):
    try:
        # Delete the previous output file if it exists
        if os.path.exists('output.txt'):
            os.remove('output.txt')

        # Execute the MiniZinc command
        print("Running MiniZinc script...")
        start_time = time.time()
        result = subprocess.run(['minizinc', mzn_file, dzn_file, '--time-limit', str(timeout)], capture_output=True, text=True)   

        print("Execution time: %s seconds" % (time.time() - start_time))
        
        # Check if the execution was successful
        if result.returncode == 0:
            # Print the output
            # print("Execution time: %s seconds" % (time.time() - start_time))
            
            
            # Write the output to a file
            with open('output.txt', 'w') as f:
                f.write(result.stdout)
                print("Output saved to file: output.txt")
        else:
            # Print the error message
            print(result.stderr)
    except FileNotFoundError:
        print("MiniZinc is not installed. Please install MiniZinc to run this script.")


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


def parse_output_data(outputfile):
    with open(outputfile, 'r') as f:
        for line in f:
            if line.startswith('HAPSPosition'):
                global HAPSPosition
                HAPSPosition = []
                HAPSs = []
                for i in range(numberOfHAPSs):
                    line = f.readline()
                    clean_line = line[2:]
                    coordinates = clean_line.split(", ")
                    HAPSs = ([int(x) for x in coordinates])
                    HAPSPosition.append(HAPSs)

            elif line.startswith('RechargePointPosition'):
                global RechargePointPosition
                RechargePointPosition = []
                recharge_points = []
                for i in range(numberOfRechargePoints):
                    line = f.readline()
                    clean_line = line[2:]
                    coordinates = clean_line.split(", ")
                    recharge_points = ([int(x) for x in coordinates])
                    RechargePointPosition.append(recharge_points)
                
            elif line.startswith('DronePosition'):
                global DronePosition
                DronePosition = []
                
                for i in range(numberOfDrones):
                    line = f.readline()
                    clean_line = line[2:]
                    coordinates = clean_line.split(", ")
                    drone = ([int(x) for x in coordinates])
                    DronePosition.append(drone)

            elif line.startswith('DroneHeight'):
                global DroneHeight
                DroneHeight = []
                clean_line = line.split("=")[1].strip().strip(";")
                DroneHeight = [int(x) for x in clean_line.strip("[").strip("]").split(",")]
            
            elif line.startswith('isUserCovered'):
                global isUserCovered
                isUserCovered = []
                clean_line = line.split("=")[1].strip().strip(";")
                isUserCovered = [int(x) for x in clean_line.strip("[").strip("]").split(",")]
            

            elif line.startswith('ClosestRP'):
                print("ClosestRP")
                print(line)
                global closestRP
                clean_line = line.split("=")[1].strip().strip(";")
                closestRP = [int(x) for x in clean_line.strip("[").strip("]").split(",")]
                print(closestRP)

            elif line.startswith('ClosestDrone'):
                global ClosestDrone
                ClosestDrone = []
                clean_line = line.split("=")[1].strip().strip(";")
                ClosestDrone = [int(x) for x in clean_line.strip("[").strip("]").split(",")]
            
            elif line.startswith('userLatency'):
                global userLatency
                userLatency = []
                clean_line = line.split("=")[1].strip().strip(";")
                userLatency = [float(x) for x in clean_line.strip("[").strip("]").split(",")]

            elif line.startswith('userPathLoss'):
                global userPathLoss
                userPathLoss = []
                clean_line = line.split("=")[1].strip().strip(";")
                userPathLoss = [float(x) for x in clean_line.strip("[").strip("]").split(",")]

            elif line.startswith('userBandWidth'):
                global userBandWidth
                userBandWidth = []
                clean_line = line.split("=")[1].strip().strip(";")
                userBandWidth = [float(x) for x in clean_line.strip("[").strip("]").split(",")]

            
            

            

def print_matrix():
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
                print(" J", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in DronePosition:
                print(" E", end=" ")
            elif [x, y] in RechargePointPosition and [x, y] in DronePosition:
                print(" F", end=" ")
            elif [x, y] in HAPSPosition and [x, y] in DronePosition:
                print(" G", end=" ")
            
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


def calculate_manhattan_distance(x1, y1, x2, y2):
    print("Calculating distance between ", x1, y1, " and ", x2, y2, "...")
    return abs(x1 - x2) + abs(y1 - y2)

def calculate_total_distance_drones_rp():
    total_distance = 0
    # i = 0

    # print(DronePosition[i][0], DronePosition[i][1])
    # print(RechargePointPosition[closestRP[i]][0])
    # print(RechargePointPosition[closestRP[i]][1])
    print("DronePosition: ", DronePosition)
    print("number of dornes: ", numberOfDrones)
    for i, drone in enumerate(DronePosition):
        print("DronePosition i: ",i,  DronePosition[i])
        print("Drone Height: ", DroneHeight[i])
        total_distance += tools.distancia_manhattan(DronePosition[i], RechargePointPosition[closestRP[i]-1])
    return total_distance
    


def execute_optimization(mzn_file, dzn_file, instancia):

    
    maxtime = 200000

    # Execute the MiniZinc file
    execute_minizinc(mzn_file, dzn_file,maxtime)

    print("Parsing the data...")


    # Parse the data
    parse_minizinc_data(dzn_file)
    output_path = 'C:\\Users\\jorge\\jgomezgi\\Universidad\\8cuatri\\tfg\\src\\minizinc\\output.txt'

    output_path = 'output.txt'
    if os.path.exists(output_path):
        parse_output_data(output_path)
    else:
        print("---------------------")
        print("Error: The output file does not exist.")
        print("---------------------")
        return



    print("XY: ", XY)
    print("numberOfDrones: ", numberOfDrones)
    print("numberOfRechargePoints: ", numberOfRechargePoints)
    print("numberOfUsersClusters: ", numberOfUsersClusters)
    print("numberOfHAPSs: ", numberOfHAPSs)
    print("NUsers: ", NUsers)
    print("UserClusterPosition: ", UserClusterPosition)

    # Parse the output
    print("HAPSPosition: ", HAPSPosition)
    print("RechargePointPosition: ", RechargePointPosition)
    print("DronePosition: ", DronePosition)
    print("DroneHeight: ", DroneHeight)
    print("ClosestRP: ", closestRP)

    print("Matrix: ")
    print_matrix()
    print("Total distance drones to closest RP: ", calculate_total_distance_drones_rp())

    # Create a dictionary to store the data
    data = {
        "numberOfDrones": numberOfDrones,
        "numberOfRechargePoints": numberOfRechargePoints,
        "numberOfUsersClusters": numberOfUsersClusters,
        "numberOfHAPSs": numberOfHAPSs,
        "XY": XY,
        "CellDist":CellDist,
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
    dzn_name = dzn_file.split("\\")[-1].split(".")[0]
    file_name = f'results/{instancia}/result_{dzn_name}.json'
    print("Saving the data to file: ", file_name)

    os.makedirs(os.path.dirname(file_name), exist_ok=True)  # Create the directory if it doesn't exist
    with open(file_name, 'w') as f:
        json.dump(data, f)
    




print("Starting the script...")
mzn_file = 'modelos\\intento4_version_QoS_2.mzn'

# Get the directory path from the command line argument
parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str)

try:
    args = parser.parse_args()
    directory = args.directory
except:
    print("Error: Please provide the directory path as an argument.")

directory = directory.rstrip("\\")
instancia = directory.split("\\")[-1]
print("Directory: ", directory.split("\\"))
print("Instancia: ", instancia)
# print("Directory: ", directory)
# Iterate over all files in the directory
total_files = len([filename for filename in os.listdir(directory) if filename.endswith(".dzn")])
processed_files = 0

for filename in os.listdir(directory):
    if filename.endswith(".dzn"):
        # Construct the full file path
        dzn_file = os.path.join(directory, filename)
        # Execute the optimization for the current file
        print(f"Processing file: {dzn_file}")
        execute_optimization(mzn_file, dzn_file, instancia)
        processed_files += 1
        completion_percentage = (processed_files / total_files) * 100
        print(f"Progress: {completion_percentage:.2f}%")

