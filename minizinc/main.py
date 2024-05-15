import subprocess
import time
import numpy as np

numberOfDrones = 0
numberOfRechargePoints = 0
numberOfUsersClusters = 0
numberOfHASPs = 0
XY = 0
HASPPosition = []
RechargePointPosition = []
DronePosition = []
NUsers = []
UserClusterPosition = []
DroneHeight = []


def execute_minizinc(mzn_file, dzn_file,timeout):
    try:
        # Execute the MiniZinc command

        print("Running MiniZinc script...")
        start_time = time.time()
        result = subprocess.run(['minizinc', mzn_file, dzn_file, '--time-limit', str(timeout)], capture_output=True, text=True)        
        # Check if the execution was successful
        if result.returncode == 0:
            # Print the output
            print("Execution time: %s seconds" % (time.time() - start_time))
            # Write the output to a file
            with open('output.txt', 'w') as f:
                f.write(result.stdout)
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
            elif line.startswith('numberOfHASPs'):
                global numberOfHASPs
                numberOfHASPs = int(line.split()[2].replace(";", ""))
            elif line.startswith('XY'):
                global XY
                XY = int(line.split()[2].replace(";", ""))

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
            if line.startswith('HASPPosition'):
                global HASPPosition
                HASPPosition = []
                hasps = []
                for i in range(numberOfHASPs):
                    line = f.readline()
                    clean_line = line[2:]
                    coordinates = clean_line.split(", ")
                    hasps = ([int(x) for x in coordinates])
                    HASPPosition.append(hasps)

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
            
            elif line.startswith('ClosestRP'):
                print("ClosestRP")
                print(line)
                global closestRP
                clean_line = line.split("=")[1].strip().strip(";")
                closestRP = [int(x) for x in clean_line.strip("[").strip("]").split(",")]
                print(closestRP)
            
            elif line.startswith('userQoS'):
                print("userQoS")
                print(line)
                global userQoS
                clean_line = line.split("=")[1].strip().strip(";")
                userQoS = [float(x) for x in clean_line.strip("[").strip("]").split(",")]
                print(sum(userQoS))

            

def print_matrix():
    print("  ", end=" ")
    for x in range(1,XY+1):
        print(f"{x:02}", end=" ")
    print()
    for x in range(1,XY+1):
        print(f"{x:02}", end=" ")
        for y in range(1,XY+1):
            
            if [x, y] in UserClusterPosition and [x, y] in RechargePointPosition and [x, y] in HASPPosition and [x, y] in DronePosition:
                print(" A", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in RechargePointPosition and [x, y] in HASPPosition:
                print(" B", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in RechargePointPosition:
                print(" C", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in HASPPosition:
                print(" D", end=" ")
            elif [x, y] in UserClusterPosition and [x, y] in DronePosition:
                print(" E", end=" ")
            elif [x, y] in RechargePointPosition and [x, y] in DronePosition:
                print(" F", end=" ")
            elif [x, y] in HASPPosition and [x, y] in DronePosition:
                print(" G", end=" ")
            
            elif [x, y] in UserClusterPosition:
                print(" U", end=" ")
            elif [x, y] in HASPPosition:
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
    for i in range(numberOfDrones):    
        total_distance += calculate_manhattan_distance(DronePosition[i][0], DronePosition[i][1], RechargePointPosition[closestRP[i]-1][0], RechargePointPosition[closestRP[i]-1][1])
    return total_distance
    


print("Starting the script...")

# Specify the MiniZinc file and data file
mzn_file = 'intento4_version_QoS.mzn'
dzn_file = 'instancia3_hasps.dzn'
maxtime = 100000

# Execute the MiniZinc file
output = execute_minizinc(mzn_file, dzn_file,maxtime)

print("Parsing the data...")


# Parse the data
parse_minizinc_data(dzn_file)
parse_output_data('output.txt')



print("XY: ", XY)
print("numberOfDrones: ", numberOfDrones)
print("numberOfRechargePoints: ", numberOfRechargePoints)
print("numberOfUsersClusters: ", numberOfUsersClusters)
print("numberOfHASPs: ", numberOfHASPs)
print("NUsers: ", NUsers)
print("UserClusterPosition: ", UserClusterPosition)

# Parse the output
print("HASPPosition: ", HASPPosition)
print("RechargePointPosition: ", RechargePointPosition)
print("DronePosition: ", DronePosition)
print("DroneHeight: ", DroneHeight)
print("ClosestRP: ", closestRP)

print("Matrix: ")
print_matrix()
print("Total distance drones to closest RP: ", calculate_total_distance_drones_rp())





# structured_output = parse_minizinc_output("output.txt")
# print(structured_output)
# # coverage_stats = analyze_coverage(structured_output)
# # print(coverage_stats)


#  matriz, suma distancias, porcentaje area cobertura, 
# ratio latencia altura 
