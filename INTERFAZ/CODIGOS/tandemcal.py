import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from scipy.stats import pearsonr


# Cargar la imagen

def tandem(image_path,folder):
    image = io.imread(image_path)
    dim=image.shape

    # Convertir la imagen de BGR a HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Definir el rango de color rosado
    lower_pink = np.array([140, 50, 50])
    upper_pink = np.array([180, 255, 255])
# Crear una máscara para filtrar el color rosado
    mask = cv2.inRange(hsv_image, lower_pink, upper_pink)
# Encontrar los contornos de los objetos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Extraer las coordenadas de los contornos
    coordinates = []
    for contour in contours:
         for point in contour:
                x, y = point[0]
                coordinates.append((x, y))



# Dibujar los contornos en la imagen original
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    # Mostrar la imagen con los contornos
    x_values = [coord[0] for coord in coordinates]
    y_values = [coord[1] for coord in coordinates]
   # Calcular la línea de tendencia utilizando la regresión lineal
    data_dict = {}

    for x, y in zip(x_values, y_values):
          if x in data_dict:
                data_dict[x].append(y)
          else:
                data_dict[x] = [y]



    x_values=[i for i in data_dict.keys()]
    y_values=[np.mean(data_dict[i]) for i in data_dict.keys()]
    slope, intercept = np.polyfit(x_values, y_values, 1)
    trendline = np.polyval([slope, intercept], x_values)
# Crear una figura y un eje
    fig, ax = plt.subplots(figsize=(8,2))
    # Mostrar la imagen 
    plt.imsave(''.join([folder,'/tendencia.jpg']),image)
    image_path = ''.join([folder,'/tendencia.jpg'])
    image = plt.imread(image_path)
    ax.imshow(image)
    # Calcular la pendiente de la recta


    slope=np.degrees(slope)
    

    r2=pearsonr( np.array(x_values),np.array(y_values)*dim[0])[0]




# Trazar los puntos
# Trazar la línea de tendencia
    ax.plot(x_values, trendline, 'b-', label='Línea de tendencia')

#calculan las distancias
    distances = np.abs(np.subtract(y_values, trendline))
    max_distance_index = np.argmax(distances)
# Agregar una leyenda

    plt.axis('off')

    
    ax.plot(x_values[max_distance_index], y_values[max_distance_index], 'o', color='red',label='Punto mas alejado')
    ax.legend( fontsize='small', ncol=2, loc='lower center')

    plt.savefig(''.join([folder,'/tendencia.jpg']),bbox_inches='tight',dpi=500)

    return  slope,r2
