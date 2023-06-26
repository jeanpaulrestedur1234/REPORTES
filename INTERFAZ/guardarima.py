import tkinter as tk
from PIL import ImageGrab
import matplotlib.pyplot as plt
import numpy as np
from CODIGOS.ejecutar import abrirArchivo
def save_image(event):
    # Captura la pantalla en el área de transferencia
    image = ImageGrab.grabclipboard()

    if image is None:
        print("No se encontró una imagen en el portapapeles.")
    else:
        
        # Carga la imagen guardada y la muestra usando matplotlib
        
        plt.imshow(image)
        plt.axis('off')
        plt.show()
        folder=abrirArchivo()
        image.save(folder+"/pies.jpg")
        # Guarda la imagen en un archivo
        window.destroy()

# Crea la ventana principal
def guardarimagen():
    global window
    # Crea la ventana principal
    window = tk.Tk()

    # Define una función para capturar el evento de clic derecho
    def on_right_click(event):
        save_image(event)

    # Asocia la función de captura de clic derecho al evento Button-3
    window.bind("<Button-3>", on_right_click)

    # Inicia el bucle principal de la interfaz gráfica
    window.mainloop()