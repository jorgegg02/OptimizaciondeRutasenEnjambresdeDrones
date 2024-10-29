def distancia_manhattan(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = abs(x2 - x1) + abs(y2 - y1)
    return distancia

def calculate_manhattan_distance(x1, y1, x2, y2):
    print("Calculating distance between ", x1, y1, " and ", x2, y2, "...")
    return abs(x1 - x2) + abs(y1 - y2)
            

def calculate_closest_rp(drones, rps):
    closest_rp = []
    print("Calculating closest RP to drones...")
    print("Drones: ", drones)
    print("RPs: ", rps)
    for drone in drones:
        # print("Calculating closest RP to drone ", drone, "...")
        min_distance = 10000
        closest_rp_index = None
        for i, rp in enumerate(rps):
            distance = distancia_manhattan(drone, rp)
            if distance < min_distance:
                min_distance = distance
                closest_rp_index = i+1
        print("Closest RP to drone ", drone, " is RP ", closest_rp_index)
        print("Distance: ", min_distance)
        closest_rp.append(closest_rp_index)
    return closest_rp

def calculate_closest_drone(DronePosition, UserClusterPosition):
    closest_drone = []
    # print("Calculating closest drone to user clusters...")
    # print("DronePosition: ", DronePosition)
    # print("UserClusterPosition: ", UserClusterPosition)
    for user_cluster in UserClusterPosition:
        # print("Calculating closest drone to user cluster ", user_cluster, "...")
        min_distance = 10000
        closest_drone_index = None
        for i, drone in enumerate(DronePosition):
            distance = distancia_manhattan(drone, user_cluster)
            if distance < min_distance:
                min_distance = distance
                closest_drone_index = i
        closest_drone.append(closest_drone_index)
    return closest_drone