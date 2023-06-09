from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self, p_info, dates, comp, orientation, unit, format):
        super().__init__(orientation, unit, format)

        self.name = p_info[0][:-1]
        self.age = str(p_info[1])
        self.pathgy = p_info[2]
        self.id = str(p_info[3])
        self.p_date = dates[0]
        self.c_date = dates[1]
        self.comparative = comp

    def header(self):
        self.image('roosevelt.png', 10, 3, 30)

        self.set_font('Times', 'B', 10)

        self.text(87, 13, "INSTITUTO ROOSEVELT - LABORATORIO DE ANÁLISIS DE MOVIMIENTO")
        self.text(106, 19, "REPORTE DE RESULTADOS PRUEBA ESTABILOMETRÍA ")
        self.text(25, 30, "NOMBRE:")
        self.text(195, 30, "EDAD:")
        self.text(25, 36, "DIAGNÓSTICO DE REMISIÓN:")
        self.text(195, 36, "ID:")

        self.set_font('Times', 'I', 9)

        self.text(
            (195 + 55 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.name) / 2,
            30,
            str(self.name))
        self.text(220, 30, self.age + " años")
        self.text(
            (195 + 55 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.pathgy) / 2,
             36, str(self.pathgy))
        self.text(218, 36, str(self.id))

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def pag1(self):
        self.add_page()
        self.set_font('Helvetica', '', 10)
        if not self.comparative:
            self.image('images/stabilo.png', 55, 50, 180, 75)
        else:
            self.text(120, 50, f'FECHA EXAMEN ACTUAL: {self.c_date}')
            self.image('images/stabilo.png', 55, 55, 180, 65)
            self.text(120, 125, f'FECHA EXAMEN ANTERIOR: {self.p_date}')
            self.image('images/prev_stabilo.png', 55, 130, 180, 65)
            