import numpy as np
import math

def place_drones_grid(X, num_drones):
    matrix = np.zeros((X, X))
    positions = []
    
    # Calcula la cantidad de drones por fila y columna
    grid_sizex = int(round(math.sqrt(num_drones)))
    grid_sizey = int(math.ceil(math.sqrt(num_drones)))
    
    # if grid_sizex * grid_sizey < num_drones:

    #     grid_sizex = grid_sizex + (num_drones - grid_sizex*grid_sizey)

    # Determina el espacio entre drones
    step_x = math.floor(X / grid_sizex)    
    step_y = math.floor(X / grid_sizey) 
    
    # Ajusta el punto inicial para centrar los drones
    start_x = (X - step_x * (grid_sizex - 1)) // 2
    start_y = (X - step_y * (grid_sizey - 1)) // 2
    
    # Coloca los drones en la matriz
    for i in range(grid_sizex):
        remaining = num_drones - len(positions)
        if i == grid_sizex - 1 and remaining > 0:
            step_y = math.floor(X / remaining)
            start_y = (X - step_y * (remaining - 1)) // 2

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
    for row in matrix:
        print(' '.join('-' if x == 0 else '1' for x in row))

# Ejemplo de uso
X = 20  # Tamaño del lado de la matriz
#num_drones =   # Cambiar esto para probar diferentes cantidades de drones
for num_drones in range(1, 17):
    print(f"Posiciones de los drones ({num_drones} drones):")
    matrix, positions = place_drones_grid(X, num_drones)
    print("Posiciones de los drones:", positions)
    print_matrix(matrix)
    print()

