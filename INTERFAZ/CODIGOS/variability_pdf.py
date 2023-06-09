import numpy as np

from CODIGOS.variability import table_title
from fpdf import FPDF


''' PDF variability of six minutes

This class create a PDF of the variability six minutes test, that will be save
in the patient folder.
'''

class PDF_var(FPDF):
    def __init__(self, p_info, orientation, unit, format):
        super().__init__(orientation, unit, format)
        
        self.name = p_info[0][:-1]
        self.age = str(p_info[1])
        self.pathgy = p_info[2]
        self.id = str(p_info[3])




    def header(self):
        # Logo 

        self.image('Vairabillityinfo/'+'images/roosevelt.png', 10, 3, 30)

        self.set_font('Helvetica', 'B', 10)

        self.text(77, 13, "INSTITUTO ROOSEVELT - LABORATORIO DE ANÁLISIS DE MOVIMIENTO")
        self.text(80, 19, "REPORTE DE VARIABILIDAD DE PASO POR RECORRIDOS")
        self.text(27, 30, "NOMBRE:")
        self.text(205, 30, "EDAD:")
        self.text(27, 36, "DIAGNÓSTICO:")
        self.text(205, 36, "ID:")
        self.set_font('Helvetica', 'I', 9)
        self.text((205 + 30 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.name) / 2, 30, self.name)
        self.text(230, 30, self.age  + " años")
        self.text((205 + 30 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.pathgy) / 2, 36, self.pathgy) #130 - len(self.pathgy)
        self.text(228, 36, self.id)


    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)

        # Text color in gray

        self.set_text_color(128)

        # Page number

        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')   


    def pag1(self):
        self.add_page() 
        self.set_font('Helvetica', '', 10)
        self.text(115, 50, "Datos generales(Todos los tramos)")

        # Black boxes around the tables

        self.ln(49)
        self.cell(18)
        self.cell(100,53, border=True)
        self.cell(19)
        self.cell(100,53, border=True)
        self.image('Vairabillityinfo/'+'images/stride_durstats.png', 30, 60, 95, 50)
        self.image('Vairabillityinfo/'+'images/stride_lenstats.png', 150, 60, 95, 50)

        # Black boxes around the tables

        self.ln(60)
        self.cell(18)
        self.cell(100,53, border=True)
        self.cell(19)
        self.cell(100,53, border=True)
        self.image('Vairabillityinfo/'+'images/stride_velstats.png', 30, 120, 95, 50)
        self.image('Vairabillityinfo/'+'images/osc_timestats.png', 150, 120, 95, 50)

        # IDC and L_T
        
        self.set_font('Helvetica', 'B', 9)

        #self.text(43, 178, f'Índice De Distancia Caminada: {self.idc}')  # Another option is add spaces and then put the idc value
        # self.text(100, 178, self.idc)

        #self.text(175, 178, f'Tendencia Linear: {self.l_t}')
        # self.text(210, 178, self.l_t)



        
    def pag2(self):
        self.add_page()
        self.set_font('Helvetica', '', 10)
        self.text(115, 50, "Datos generales(Todos los tramos)")

        # Black boxes around the tables

        self.ln(49)
        self.cell(18)
        self.cell(100,53, border=True)
        self.cell(19)
        self.cell(100,53, border=True)
        self.image('Vairabillityinfo/'+'images/step_durstats.png', 30, 60, 95, 50)
        self.image('Vairabillityinfo/'+'images/stride_cadstats.png', 150, 60, 95, 50)

        # Black boxes around the tables

        self.ln(60)
        self.cell(78)
        self.cell(100,53, border=True)
        self.image('Vairabillityinfo/'+'images/step_lenstats.png', 90, 120, 95, 50)

        


    def pag3(self):
        self.add_page()
        x,y=[50,40]
        Y=55
        
        # Titles 
        
        self.text(15, 50, table_title("stride_dur"))
        self.text(81, 50, table_title("stride_len"))
        self.text(143, 50, table_title("stride_vel"))
        self.text(198, 50, table_title("osc_time"))
   
        self.image('Vairabillityinfo/'+'images/stride_dur15s.png', 10, Y, x, y)
        self.image('Vairabillityinfo/'+'images/stride_len15s.png', 78, Y,x, y)
        self.image('Vairabillityinfo/'+'images/stride_vel15s.png', 141,Y, x, y)
        self.image('Vairabillityinfo/'+'images/osc_time15s.png', 204, Y, x, y)
        self.ln(90)

        # The vector of cv average are in the same order of colnames in var_6min module
        # colnames -> ['stride_dur', 'stride_len', 'stride_vel', 'stride_cad', 'step_dur', 'step_len', 'osc_time']

        
        self.text(59, 120, table_title("step_dur"))
        self.text(112, 120, table_title("stride_cad"))
        self.text(183, 120, table_title("step_len"))

        self.image('Vairabillityinfo/'+'images/step_dur15s.png', 50, 125,  x, y)
        self.image('Vairabillityinfo/'+'images/stride_cad15s.png', 115, 125,  x, y)
        self.image('Vairabillityinfo/'+'images/step_len15s.png', 178,  125,  x, y)
