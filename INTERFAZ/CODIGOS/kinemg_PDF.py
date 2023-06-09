from fpdf import FPDF
import os

''' PDF max and min report, and EMG
This class create a PDF of the...
'''

class PDF_MM(FPDF):

    def __init__(self, p_info, orientation, unit, format): # firstname, lastname, age, pathology, p_id
        super().__init__(orientation, unit, format)
        self.name= p_info[0][:-1]
        print(self.name)
        self.age=p_info[1]
        self.pathgy=p_info[2]
        self.id = p_info[3]



    def header(self):
        self.image('roosevelt.png', 5, 3, 30)


        self.set_font('Helvetica', 'B', 10)
        x1 = 27
        x2 = 205
        center_name = (x1 + x2 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.name[:-1]) / 2
        center_pathgy = (x1 + x2 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.pathgy) / 2
        self.text(87, 13, 'INSTITUTO ROOSEVELT - LABORATORIO DE ANÁLISIS DE MOVIMIENTO')
        self.text(106, 19, 'REPORTE DE MÁXIMOS Y MÍNIMOS (RMS) DEL ACM')
        self.text(27, 30, 'NOMBRE:')
        self.text(205, 30, 'EDAD:')
        self.text(27, 36, 'DIAGNÓSTICO DE RESMISIÓN:')
        self.text(205, 36, 'ID:')
        self.set_font('Helvetica', 'I', 9)
        self.text(center_name, 30, self.name)
        self.text(center_pathgy, 36, self.pathgy)
        self.text(230, 30, f'{self.age} años')
        self.text(228, 36, str(self.id))


    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


    def pag1(self):
        self.add_page()
        self.image(os.sep.join([ 'images', 'sagittal.png']) , 5, 45, 70, 150)
        self.image(os.sep.join([ 'images', 'transverse.png']) , 140, 45, 70, 150)
        w, h1, h2 = 60, 25, [7, 10, 7, 13]
        x, y, x1 = 75, 47, 210
        y1 = y
        for i, h in zip(range(4), [4, 2, 5, 3]):
            self.image(os.sep.join([ 'images', f'mm_sagittal{i}.png']), x, y, w, h1)
            self.image(os.sep.join([ 'images', f'rng_sagittal{i}.png']), x, y + h1, w, h2[i])
            self.image(os.sep.join(['images', f'mm_transverse{i}.png']), x1, y1, w, h1)
            self.image(os.sep.join([ 'images', f'rng_transverse{i}.png']), x1, y1 + h1, w, h2[0])
            y += h1 + h2[i] + h 
            y1 += h1 + h2[0] + 5
        

    def pag2(self):
        self.add_page()
        self.image(os.sep.join([ 'images','frontal.png']) , 75, 55, 75, 120)
        x, y, w, h1, h2 = 155, 57, 60, 25, 8
        for i in range(3):
            self.image(os.sep.join(['images',f'mm_frontal{i}.png']), x, y, w, h1)
            self.image(os.sep.join([ 'images',f'rng_frontal{i}.png']), x, y + h1, w, h2)
            y += h1 + h2 + 7

    def pag3(self):
        self.add_page()
        
        w, h1 = 50, 15
        x, y, = 38, 100
        x1=x
        y1=170

        
        
            

        self.image(os.sep.join([ 'images', 'F.png']) , 20, 50, 210, 50)
        self.image(os.sep.join([ 'images', 'P.png']) , 20, 120, 210,50)
        for i in range(3):
             self.image(os.sep.join([ 'images', f'mm_F{i}.png']), x, y, w, h1)
             self.image(os.sep.join([ 'images', f'mm_P{i}.png']), x1, y1, w, h1)
             x=x+71
             x1=x
    
    def pag4(self):
        self.add_page()
        w, h1 = 50, 15
        x, y, = 38, 100
        x1=x
        y1=170
 

        self.image(os.sep.join([ 'images', 'M.png']) , 20, 50, 210, 50)
        self.image(os.sep.join([ 'images', 'Ml.png']) , 20, 120, 140,50)
        for i in range(3):
             self.image(os.sep.join([ 'images', f'mm_M{i}.png']), x, y, w, h1)
             if i<2:
                  self.image(os.sep.join([ 'images', f'mm_Ml{i}.png']), x1, y1, w, h1)
             x=x+70
             x1=x


    def pag5(self):
        self.add_page()
        self.image(os.sep.join([ 'images','emg.png']) , 40, 40, 200, 150)
