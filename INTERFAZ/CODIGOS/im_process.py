import numpy as np
from skimage import io, measure
import matplotlib.pyplot as plt
def obtener_puntos_negros(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = np.dot(imagen[..., :3], [0.2989, 0.5870, 0.1140])
    # Obtener las coordenadas de los puntos negros
    puntos_negros = np.argwhere(imagen_gris<44)
    return puntos_negros
def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray
def remBackground(I):

    I_back = np.array(I)
    gray=rgb2gray(I_back)
    I_back [gray>240,:]=255



    I_back[:,np.size(I_back,1)- 5:np.size(I_back,1),:] = 255;
    I_back[:,0:5,:] = 255;
    I_back[np.size(I_back,0)- 5:np.size(I_back,0),:,:] = 255;
    I_back[0:6,:,:] = 255;
    I_back[0:30,0:30,:] = 255;

    return I_back





def COP(toe, relation=1):   # se usa i.png o d.png
  print(toe) 

  longI = 0
  longRI = 0


 
  i=io.imread(toe, as_gray=True)



  contornos = measure.find_contours(i, 0.9)  # Ajusta el valor de umbral según sea necesario
  contorno=np.concatenate(contornos,axis=0) # agrupa los datos
  fig, ax = plt.subplots()






 
  anchoI=max(contorno[:, 1])-min(contorno[:, 1])

  largoI=max(contorno[:, 0])-min(contorno[:, 0])
  print(largoI)
  contorno2=obtener_puntos_negros(io.imread(toe))

  

  
  x=max(contorno2[:, 1])-min(contorno2[:, 1])

  y=max(contorno2[:, 0])-min(contorno2[:, 0])
  
 #ax.plot(contorno[:, 1], contorno[:, 0], 'o')
  largoCOPI =  y
  Iporce_cop = largoCOPI /largoI*100
      

#Desviacion estandar

  COPstdI = np.std(contorno2[:, 1])
  print(np.round(Iporce_cop*relation ,2),np.round(COPstdI ,2))
  return  np.round(Iporce_cop*relation ,2),np.round(COPstdI ,2)

#variables
#Longitud de los pies, cuando la persona no apoya todo el pie
#Si estas variables estan en 0 es porque no son necesarias

#variables
#Longitud de los pies, cuando la persona no apoya todo el pie
#Si estas variables estan en 0 es porque no son necesarias




