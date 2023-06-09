from tkinter import*
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk
import shutil
from CODIGOS.ejecutar import*
from crearexcelstabilo import*
from crearexcel_6min import*
from guardarima import*
import shutil

def estcomp():
    ant=lastexam.get()
    new=newexam.get()
    folder=abrirArchivo()
    esatbilometria(comp=True,ant=ant,new=new,path=folder)
    lastexam.destroy()
    newexam.destroy()
    lab1.destroy()
    lab2.destroy()
    NEWB.destroy()
    button = ttk.Button(text="Seleccionar", command=Condiciones)
    button.grid(row=1, column=1, padx=10, pady=10)
def cancel():
    lastexam.destroy()
    newexam.destroy()
    NEWB.destroy()
    lab1.destroy()
    lab2.destroy()
    cancelar.destroy()
    button.grid(row=1, column=1, padx=10, pady=10)
    
def cambio():
    Especificaciones.delete(1.0, tk.END)
    button2.grid_forget()
    button3.grid_forget()
    button4.grid_forget()
    button5.grid_forget()
    button6.grid_forget()
    label_var.grid_forget()
    label_var.delete(0, tk.END)


def rapido():
    if not os.path.exists('resultados'):
        os.mkdir('resultados') 
    else:
        shutil.rmtree('resultados')
        os.mkdir('resultados') 

    
    
    directorios=filedialog.askdirectory()
  
    diccionario={'EST':"ESTABILOMETRIA",'COP':'COP','6MIN':"6MIN",'RMS': "KINEMATICS",'TANDEM':"TANDEM",'VAR':"VARIABILIDAD"}

    
    
    for i in os.listdir(directorios):
        file= i
        if not('.' in file):
            exam=file.split()[-1]
            if exam=='6MIN' or exam=='6_MIN':
                exam='6MIN'
            if exam not in diccionario.keys():
                exam='EST'
            
            try:
                
                show_selection(Examen=diccionario[exam],folder=directorios+'/'+file)
              

            except:
                pass
            

    
    
def crear_():
    entrada1=label_var.get()
    datos = list(csv.reader(entrada1.strip().split('\n'), delimiter='\t'))
    information=[]
    for row in datos:
        fila=[]
        condicion=not('Exportación de ciclos de marcha a la izquierda por recorrido'in row)
        if not('Media'in row) and condicion:
            for dat in row:
                try:
                       fila.append(float(dat))
                except:
                       fila.append(dat)
            information.append(fila)
        
        
    libro_excel = load_workbook('formato6min.xlsx')
    guardar_datos(libro_excel,information,'Datos por tramo')
    folder=abrirArchivo()

    libro_excel.save(folder+'/Data_6Minutes.xlsx')
    button5.grid_forget()
    label_var.grid_forget()



def Condiciones():
    Especificaciones.delete(1.0, tk.END)
    Especificaciones.insert(tk.END, """La carpeta debe contener""" )
    Especificaciones.insert(tk.END,"\n"+"\n"+ "Nota:(edad, diagnostico...)"  )
    


    Examen= combo.get()
    if Examen== "ESTABILOMETRIA":
        button3.grid(row=6, column=0, columnspan=2, pady=10)
 
        Especificaciones.insert(tk.END,"\n" +"\n"+"el archivo excel (stabilo.xlsx)"  )
   
        
    if Examen== "ESTABILOMETRIA_COMP": 
        button3.grid(row=6, column=0, columnspan=2, pady=10)

        Especificaciones.insert(tk.END,"\n"+ "\n"+"el archivo excel (stabilo.xlsx)" )
        Especificaciones.insert(tk.END,"\n"+"\n"+"Luego de ello le pedira el excel del examen anterior" ) 
        
    

    if Examen=="COP":
 
        Especificaciones.insert(tk.END,"\n" +"\n"+"el archivo (nombre del paciente)Secuencia.pdf"  ) 
        Especificaciones.insert(tk.END,"\n"+"\n"+"Advetencia:" )   
        Especificaciones.insert(tk.END,"\n"+"si el sistema no puede encontar la imagenes en el pdf tendra que guardas las imagenes en formato jpg con los nombres ic y dc" ) 
      

      
     
    if Examen=="COP_COMP":
  
        Especificaciones.insert(tk.END, "\n"+"\n"+"el archivo (nombre del paciente)Secuencia.pdf") 
        Especificaciones.insert(tk.END, "\n"+"\n"+"Luego de ello le pedira las imagenes anteriores") 
        Especificaciones.insert(tk.END,"\n"+"\n"+"Advetencia:" )   
        Especificaciones.insert(tk.END,"\n"+"si el sistema no puede encontar la imagenes en el pdf tendra que guardas las imagenes en formato jpg con los nombres ic y dc" ) 
    
  
    if Examen=="6MIN":
        button4.grid(row=6, column=0, columnspan=2, pady=10)

        Especificaciones.insert(tk.END,"\n"+"\n"+ "el archivo excel (Data6Minutes.xlsx)"  ) 

        
    if Examen=="KINEMATICS":
    
        Especificaciones.insert(tk.END,"\n" +"\n"+"los archivos de los walking" )
        

    if Examen=="VARIABILIDAD":
        button5.grid(row=6, column=0, columnspan=2, pady=10)
        label_var.grid(row=6, column=1, columnspan=2, pady=10)
  
        Especificaciones.insert(tk.END,"\n"+"\n"+ "el archivo excel (Data6Minutes.xlsx)")
        Especificaciones.insert(tk.END,"\n"+"\n"+ "en este archivo se guarda la informacion por recorrido)" )

    if Examen=="TANDEM":
        Especificaciones.insert(tk.END,"\n"+"\n"+ "el archivo pies.jpg")
        button6.grid(row=6, column=0, columnspan=2, pady=10)
    
    
    button2.grid(row=5, column=0, columnspan=2, pady=10)
    


def show_selection(Examen='select',folder='ninguno'):
    if not os.path.exists('images'):
        os.mkdir('images') 
    else:
        shutil.rmtree('images')
        os.mkdir('images') 

    
    if Examen=='select':
        Examen=combo.get()
    else:
        pass
    

    
    """Se elige el examen a realizar """
    # Obtener la opción seleccionada.
    if folder=='ninguno':
        if Examen!="ESTABILOMETRIA_COMP":
                folder=abrirArchivo() 
        try:
            shutil.rmtree('resultados')
        except:
            pass
    else:
        pass



    if Examen== "ESTABILOMETRIA": 
    
        esatbilometria(comp=False,ant=None,new=None,path=folder)
    
        
    if Examen== "ESTABILOMETRIA_COMP": 
        global lastexam, newexam,NEWB,lab1,lab2,cancelar,button
        button.grid_forget()
        lastexam=tk.Entry()
        lastexam.grid(row=3, column=2, padx=10, pady=10)
        lab1=tk.Label(text='Fecha del anterior examen')
        lab1.grid(row=3, column=1, padx=10, pady=10)
        newexam=tk.Entry()
        newexam.grid(row=4, column=2, padx=10, pady=10)
        lab2=tk.Label(text='Fecha del nuevo examen')
        lab2.grid(row=4, column=1, padx=10, pady=10)
        NEWB=tk.Button(text="INICIAR EXAMEN COMPARATIVO",command=estcomp)
        NEWB.grid(row=5, column=0, columnspan=2, pady=10)
        cancelar=tk.Button(text="cancelar",command=cancel)
        cancelar.grid(row=5, column=1, columnspan=2, pady=10)
       

        

       
    if Examen=="COP":
        COP_EX(compara=False,path=folder)
      
    if Examen=="COP_COMP":
        COP_EX(compara=True,path=folder)
      
    if Examen=="6MIN":
        sixmin6(path=folder)

        
    if Examen=="KINEMATICS":
        Kinematics(path=folder)
    if Examen=="VARIABILIDAD":
        Variabilidad(path=folder)
    if Examen=="TANDEM":
        Tandem(path=folder)

    button2.grid_forget()
    button3.grid_forget()
    button4.grid_forget()
    button5.grid_forget()
    button6.grid_forget()
    label_var.grid_forget()


    
       
        

""" CREO LA INTERFRAZ """
main_window = Tk()

title_label = tk.Label(main_window, text="GENERADOR DE REPORTES",bg="light blue")
title_label.grid(row=0, column=0, columnspan=2, pady=10)
main_window.columnconfigure(0, weight=1)
main_window.columnconfigure(1, weight=1)
main_window.configure(bg="light blue")

combo = ttk.Combobox(
    state="readonly",
    values=["ESTABILOMETRIA", "ESTABILOMETRIA_COMP","COP","COP_COMP", "6MIN", "KINEMATICS","TANDEM","VARIABILIDAD"]
)
titulo = tk.Label(main_window, text="Generador de Reportes", font=("Arial", 16),bg="light blue")

combo.grid(row=1, column=0, padx=10, pady=10)
button = ttk.Button(text="Seleccionar", command=Condiciones)
Especificaciones=tk.Text(main_window, height=14, width=50,bg="light blue")
Especificaciones.grid(row=2, column=0, columnspan=2, pady=4)
button2 = ttk.Button(text="INICIAR", command=show_selection)

button.grid(row=1, column=1, padx=10, pady=10)
combo.bind("<<ComboboxSelected>>", lambda event: cambio())
button3 = ttk.Button(text="Crear excel", command=guardar_stabilo)
button4 = ttk.Button(text="Crear excel", command=crear_ventana6min)
button5 = ttk.Button(text="Crear excel", command=crear_)
button6 = ttk.Button(text="Cargar imagen", command=guardarimagen)
label_var = tk.Entry(main_window)
boton = tk.Button( text="", command=rapido, bg="light blue", bd=0)
boton.place(x=0,y=0)
main_window.mainloop()
