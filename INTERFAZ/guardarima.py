import tkinter as tk
from PIL import ImageGrab
import matplotlib.pyplot as plt
import numpy as np

def save_image(event):
    # Captura la pantalla en el área de transferencia
    image = ImageGrab.grabclipboard()

    if image is None:
        print("No se encontró una imagen en el portapapeles.")
    else:
        # Guarda la imagen en un archivo
        image.save("imagen_guardada.png")
        print("La imagen se ha guardado correctamente.")

        # Carga la imagen guardada y la muestra usando matplotlib
        img = plt.imread("imagen_guardada.png")
        plt.imshow(img)
        plt.axis('off')
        plt.show()

# Crea la ventana principal
window = tk.Tk()

# Define una función para capturar el 
# 
# evento de clic derecho
def on_right_click(event):
    save_image(event)

# Asocia la función de captura de clic derecho al evento Button-3
window.bind("<Button-3>", on_right_click)

# Inicia el bucle principal de la interfaz gráfica
window.mainloop()