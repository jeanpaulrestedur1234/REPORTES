from fpdf import FPDF

''' PDF six minutes test with IMU sensor

This class create a PDF of the six minutes test with IMU sensor, that will be save
in patient folder.
'''

class PDF_6min(FPDF):

    def __init__(self, p_info, orientation, unit, format): # firstname, lastname, age, pathology, p_id
        super().__init__(orientation, unit, format)
        # self.firstname = firstname
        # self.lastname = lastname
        self.name = p_info[0][:-1]
        self.age = str(p_info[1])
        self.pathgy = p_info[2]
        self.id = str(p_info[3])

    def header(self):
        self.image('roosevelt.png', 5, 3, 30)

        # HEADER ONLY IN PAGE No 1

        if self.page_no() == 1:
            self.set_font('Times', 'B', 9)
            self.text(51, 13, 'INSTITUTO ROOSEVELT - LABORATORIO DE ANÁLISIS DE MOVIMIENTO')
            self.text(67.5, 19, 'REPORTE PRUEBA DE 6 MINUTOS CON SENSOR ')
            self.text(15, 30, 'NOMBRE:')
            self.text(155, 30, 'EDAD:')
            self.text(15, 36, 'DIAGNÓSTICO DE REMISIÓN:')
            self.text(155, 36, 'ID:')
            self.set_font('Times', 'I', 9)
            self.text((155 + 15 + self.get_string_width('DIAGNÓSTICO DE REMISIÓN:')) / 2 - self.get_string_width(self.name) / 2, 30, self.name )
            self.text(180, 30, self.age  + ' años')
            self.text((155 + 15 + self.get_string_width('DIAGNÓSTICO DE REMISIÓN:')) / 2 - self.get_string_width(self.pathgy) / 2, 36, self.pathgy)
            self.text(177, 36, self.id)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')   

    def pag1(self):
        self.add_page()
        self.ln()

        # TABLES

        self.image('images/sess_data.png', 48, 45, 120, 28)
        self.image('images/normal_values.png', 34, 73, 150, 50)

        # GRAPHS

        self.image('images/cadencia.png', 6.6, 120, 200, 73)
        self.image('images/velocidad.png', 6.6, 192,200, 73)

    def pag2(self):
        self.add_page()
        self.ln()

        #GRAPHS
        
        self.image('images/longitud_zancada.png', 6.6, 16, 200, 73)
        self.image('images/duracion_marcha.png', 6.6, 94, 200, 73)
        self.image('images/duracion_paso.png', 6.6, 172, 200, 73)
        self.image('legend.png', 102, 250, 14, 13)
        
    def pag3(self):
        self.add_page()
        self.ln()

        #GRAPHS

        self.image('images/duracion_apoyo.png', 6.6, 16, 200, 73)
        self.image('images/duracion_oscilacion.png', 6.6, 94, 200, 73)
        self.image('images/longitud_paso.png', 6.6, 172, 200, 73)
        self.image('legend.png', 102, 250, 14, 13)
