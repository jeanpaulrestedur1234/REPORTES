from fpdf import FPDF

class Tandempdf(FPDF):
    def __init__(self, p_info,inclinacion,tendencia, folder ,orientation, unit, format):
        super().__init__(orientation, unit, format)
        # self.firstname = p_info[0]
        # self.lastname = p_info[1]
        self.name =p_info[0][:-1]
        self.age = str(p_info[1])
        self.pathgy = p_info[2]
        self.id = str(p_info[3])
        self.inclinacion=str(abs(round(inclinacion,2)))
        self.tendencia=str(abs(round(tendencia,2)))

        self.folder=folder

#firstname, lastname, age, pahtology, p_id

    def header(self):
   
       
       
        self.image(str(self.folder)+'/tendencia.jpg',30,50,250)

       

        self.image('roosevelt.png', 10, 3, 30)
        self.set_font('Times', 'B', 10)
        self.text(97, 13, "INSTITUTO ROOSEVELT - LABORATORIO DE ANÁLISIS DE MOVIMIENTO")
        self.text(126, 19, "REPORTE DE RESULTADOS TANDEM ")
        self.text(35, 30, "NOMBRE:")
        self.text(205, 30, "EDAD:")
        self.text(35, 36, "DIAGNÓSTICO DE REMISIÓN:")
        self.text(205, 36, "ID:")
        self.set_font('Times', 'I', 9)
        self.text((205 + 55 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.name) / 2, 30, self.name)   
        self.text(230, 30, self.age  + " años")
        self.text((205 + 55 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.pathgy) / 2, 36, self.pathgy) #130 - len(self.pathgy)
        self.text(228, 36, self.id)





            

        
        self.set_font('Times', 'B',12)
        self.set_text_color(0)
        self.text(150,50, "TANDEM")
        self.set_font('Times', 'B',12)
        self.set_text_color(0)
        self.text(135,150, ' '.join(['Grado de inclinación',self.inclinacion,'°']))
        self.text(130,160, ' '.join(['Coeficiente de correlacion',self.tendencia]))
 

    def footer(self):
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')     






