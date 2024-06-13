import os
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Definir el directorio donde están los archivos JSON
json_dir = './results'

# Imprimir archivos en la carpeta
print('Files in the directory:')
for file in os.listdir(json_dir):
    print(file)
# Inicializar listas para almacenar los datos
latencies = []
path_losses = []
bandwidths = []
coverages = []

# Leer todos los archivos JSON en la carpeta
for json_file in glob.glob(os.path.join(json_dir, '*.json')):
    print(f'Reading file: {json_file}')
    with open(json_file, 'r') as f:
        data = json.load(f)
        latencies.extend(data['userLatency'])
        path_losses.extend(data['userPathLoss'])
        bandwidths.extend(data['userBandWidth'])
        coverages.extend(data['isUserCovered'])

# Convertir los datos a DataFrame para facilitar el análisis
df = pd.DataFrame({
    'Latency': latencies,
    'PathLoss': path_losses,
    'Bandwidth': bandwidths,
    'Coverage': coverages
})

#imprimir suma de coverage
print(f'Total coverage: {df["Coverage"].sum()}')

# Calcular estadísticas
stats = df.describe().transpose()

# Agregar mediana
stats['median'] = df.median()

# Mostrar estadísticas
print(stats)

# Graficar la evolución de cada valor
plt.figure(figsize=(14, 10))

# Latency
plt.subplot(2, 2, 1)
plt.plot(df['Latency'])
plt.title('User Latency Evolution')
plt.xlabel('Sample')
plt.ylabel('Latency')

# Path Loss
plt.subplot(2, 2, 2)
plt.plot(df['PathLoss'])
plt.title('User Path Loss Evolution')
plt.xlabel('Sample')
plt.ylabel('Path Loss')

# Bandwidth
plt.subplot(2, 2, 3)
plt.plot(df['Bandwidth'])
plt.title('User Bandwidth Evolution')
plt.xlabel('Sample')
plt.ylabel('Bandwidth')

# Coverage
plt.subplot(2, 2, 4)
plt.plot(df['Coverage'])
plt.title('User Coverage Evolution')
plt.xlabel('Sample')
plt.ylabel('Coverage')

plt.tight_layout()
plt.show()

# Guardar estadísticas en un archivo CSV
stats.to_csv('./results/statistics.csv')

# Guardar gráficos en un archivo
plt.savefig('./results/evolution_plots.png')
