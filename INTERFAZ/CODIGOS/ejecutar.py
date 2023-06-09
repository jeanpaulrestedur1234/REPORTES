import os 
import asyncio
import time

from CODIGOS.create_pdf import PDF   
from CODIGOS.stabilometry import stabilo
from tkinter import*
from tkinter import filedialog
from CODIGOS.kinemg_PDF import PDF_MM
from skimage import io
from CODIGOS.create_pd import PDFCOP
from CODIGOS.im_process import remBackground
from CODIGOS.im_process import COP
from CODIGOS.im_etract import extraccion
from CODIGOS.kinematics import rms
from CODIGOS.sixmin6 import six_min_sensor, var_sixmin
from CODIGOS.data import*
from CODIGOS.variability import variation
from CODIGOS.variability_pdf import PDF_var
from CODIGOS.tandemcal import*
from CODIGOS.create_tandempd import*
import tkinter as tk


"""Se copilan los codigos que ejecutan los reportes"""

def split_name(name):
    if len(name.split()) == 3:
        return  name.split()[0], ' '.join(name.split()[1:3])
    return ' '.join(name.split()[0:2]), ' '.join(name.split()[2:4])


def abrirArchivo():
        archivo=filedialog.askdirectory(title="abrir",initialdir="C:/")
        return archivo
def abrirArchivo2(folder,seleccion):
        archivo=filedialog.askopenfilename(title=seleccion,initialdir=folder)
        return archivo

def encontrar_archivos_pdf(directorio):
    rutas_pdf = []
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.endswith(".pdf"):
                ruta_absoluta = os.path.join(root, file)
                rutas_pdf.append(ruta_absoluta)
    return rutas_pdf
def p_data():    
    p_id = nfolder.split()[0]      

    # firstname, lastname = split_name(p_name)
    
    try:
        with open(nota, encoding='utf8') as f:
            lines = f.read()
    except UnicodeDecodeError:
        with open(nota, encoding='latin-1') as f:
            lines = f.read()
    finally:       
        age = [int(s) for s in lines.split() if s.isdigit()][0]
        for index, line in enumerate(lines.split()):
            
   
            if line == 'DIAGNOSTICO:':
                index_0 = index + 1
               
            elif line == '6MIN': 
                index_f = index
            elif line == 'TESTABILO:':
                index_tt = index + 1      # Initial index for time of stabilometry test
            if line == 'INDIVIDUAL:':
                index_run = index + 1
                run=''.join(lines.split()[index_run:index_run + 1])
            if line == "SENSOR:":
                index_6 = index + 1
            elif line == 'LONGITUD':
                index_footi=index+1
            elif line == 'EQUINO':
                indexfootf=index+1
            elif line == 'TOMA':
                index_eq=index+1

            
        pathology = ' '.join(lines.split()[index_0:index_f])
        t_test = lines.split()[index_tt:index_tt + 1]
        six_min = ' '.join(lines.split()[index_6:index_6 + 1])
        selected_run = ''.join(lines.split()[index_run:index_run + 1])
        foot= lines.split()[index_footi:indexfootf]
        footeq= lines.split()[indexfootf:index_eq]



    if exam=='estabilo':
        p_name =' '.join(nfolder.split()[1:]) 
    else:
         p_name = ' '.join(nfolder.split()[1:-1]) 


    if exam=='cop':
       
     
        try:
            info_pies=[float(foot[2]),float(foot[4])]
            infoeq=[float(footeq[1]),float(footeq[3])]
            equino=True
            relation=[infoeq[i]/info_pies[i] for i in range(2)]
        except:
            equino= False
            relation=[1,1]
        return p_name, age, pathology, p_id, t_test,relation
        

  


    
    if exam=='kinematics': 
            
        select=asyncio.run(save_excel(age,six_min, selected_run,folder,nfolder))
 
    else:
        select=0
    



    return p_name, age, pathology, p_id, t_test, select

def esatbilometria(comp,ant,new):

    global file_name,nfolder,nota,exam
    exam='estabilo'

    folder=abrirArchivo() 
    nfolder=os.path.split(folder)[1]
    nota=folder+'/NOTA.txt' 

    dates = (None, None)
  
    if comp:
        prev_date = ant
        cur_date = new
        dates = (prev_date, cur_date)
    
    


    patient_info = p_data()
    
    
    if not comp:
               

        stabilo(patient_info[-2][0],folder= folder)
        
    else:
        stabilo(patient_info[-2][0], folder=folder)
        stabilo(comp = comp)


    pdf = PDF(patient_info, dates, comp, 'L', 'mm', 'A4')
    pdf.pag1()
    

    try:
        if not comp:
            pdf.output(folder+f'/{patient_info[0]}_ESTABILOM.pdf')
            
        else: 
            pdf.output(folder+ f'/{patient_info[0]}_ESTABILOM_COMP.pdf')
  
    except PermissionError:
        print('You have an open pdf with the same name')

    

def COP_EX(compara):

    global file_name, folder, nfolder, nota,exam
    exam='cop'  


    folder=abrirArchivo()
    nfolder=os.path.split(folder)[1]
    file_name = ' '.join(nfolder.split()[1:-1])

    

    nota=folder+'/NOTA.txt'
    patient_info = p_data()
    relationd=patient_info[-1][0]
    relationi=patient_info[-1][1]

    

    c_name= str(''.join([folder, f'\{file_name} SECUENCIA.pdf']))

    try:
        extraccion(c_name,15,''.join([folder,'\ic']))
        extraccion(c_name,0,''.join([folder,'\dc']))
    except:
        rutas_archivos_pdf = encontrar_archivos_pdf(folder)
        print(rutas_archivos_pdf)

        extraccion(rutas_archivos_pdf[0],15,''.join([folder,'\ic']))
        extraccion(rutas_archivos_pdf[0],0,''.join([folder,'\dc']))
        print(rutas_archivos_pdf)

    try:
        Ic=io.imread(''.join([folder,'\ic.jpg']))
        dc=io.imread(''.join([folder,'\dc.jpg']))
    except:

        dir_IZ=abrirArchivo2(folder,'SELECCIONE LA IMAGEN DEL PIE IZQUIERDO')
        dir_DER=abrirArchivo2(folder,'SELECCIONE LA IMAGEN DEL PIE IZQUIERDO')
        Ic=io.imread(dir_IZ)
        dc=io.imread(dir_DER)

    Ic=remBackground(Ic)
    io.imsave(''.join([folder,'/ic.jpg']),Ic)
    datosI =[COP(''.join([folder,'/ic.jpg']),relationi),[0,0]]

    

    
    dc=remBackground(dc)

    io.imsave(''.join([folder,'/dc.jpg']),dc)
    
    datosD =[COP(''.join([folder,'/dc.jpg']),relationd),[0,0]]

    examen=int(file_name[-1]) 
    comp=0




    if compara:
         global dirder, dirizq
         
         nombres=filedialog.askopenfilenames(title='SELECCIONE LAS IMAGENES DEL EXAMEN PREVIIO')
         dirder=[ i for i in nombres if 'dc.jpg' in i][0]
         dirizq=[ i for i in nombres if 'ic.jpg' in i][0]
    
         datosD[1]=COP(dirder,relationd)
         datosI[1] =COP(dirizq,relationi) 
         comp=1
         dirs=[dirder,dirizq]

  
         pdf = PDFCOP(patient_info,datosI,datosD,comp,folder,dirs,'L', 'mm', 'A4')
         pdf.output(''.join([folder, f'/{patient_info[0]}_TrayectoriaCOMP.pdf']))
    else: 
   
        pdf = PDFCOP(patient_info,datosI,datosD,comp,folder,[0,0],'L', 'mm', 'A4')
        pdf.output(os.sep.join([folder, f'/{patient_info[0]}_COPTrayectoria.pdf']))
        


        
def sixmin6():
    global file_name, nfolder, exam,nota
    exam='6min'

    path=abrirArchivo()


    nota=path+'/NOTA.txt'
    nfolder=os.path.split(path)[1]

  
    t0= time.time()
    file_name= ' '.join(nfolder.split()[1:-1])
    direc_info = (f'{os.path.split(path)[0]}/', nfolder, file_name)
    patient_info = p_data()


    
    
    six_min_sensor(patient_info, *direc_info)
 
   
    
    var_sixmin(patient_info, *direc_info)



def Kinematics():
    global file_name,nfolder,nota,exam,folder
    exam='kinematics'

    
    folder=abrirArchivo()
  
    
    nfolder=os.path.split(folder)[1]
    nota=folder+'/NOTA.txt'
    file_name= ' '.join(nfolder.split()[1:-1])


    p_info = p_data()



    

    ther_km,haveemg=rms(p_info[1],folder, p_info[-1])

    pdf = PDF_MM(p_info, 'L', 'mm', 'letter')
    pdf.pag1()
    pdf.pag2()
    if ther_km:
            pdf.pag3()
            pdf.pag4()
    if haveemg:
            pdf.pag5()
    pdf.output(os.sep.join([folder, f'/{p_info[0]}_ReporteMM.pdf']))



    print('KINEMATICS EJECUTADO')

def Variabilidad():
    global file_name, folder,nota,exam,nfolder



    folder = abrirArchivo()
    file_name = ' '.join(folder.split()[1:])
    nfolder=os.path.split(folder)[1]
    nota=folder+'/NOTA.txt'

    exam='variability'

    patient_info = p_data()
    variation(patient_info[1],folder)

    pdf = PDF_var(patient_info, 'L', 'mm', 'letter')
    pdf.pag1()
    pdf.pag2()
    pdf.pag3()

    
    pdf.output(folder+f'/{patient_info[0]}.pdf')

def Tandem():
    global file_name, folder,nota,exam,nfolder
    exam='Tandem'
      

    folder=abrirArchivo()
  
    print(os.path.split(folder))

    nota=folder+'/NOTA.txt'
    file_name = os.path.split(folder)[1]
    nfolder=os.path.split(folder)[1]
    patient_info = p_data()

    c_name= str(''.join([folder, f'/pies.jpg']))
    inclinacion, tendencia=tandem(c_name,folder)
    pdf = Tandempdf(patient_info[0:4],inclinacion,tendencia,folder,'L', 'mm', 'A4')  
    pdf.output(os.sep.join([folder, f'{patient_info[0]}_Tandem.pdf']))    
    
    
    
    print( 'PACIENTE',(' '.join(patient_info[0].split()[:-1])[ :-1]),'finalizado' )
    
       
       






    



