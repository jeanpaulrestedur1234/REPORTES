from fpdf import FPDF

class PDFCOP(FPDF):
    def __init__(self, p_info,datosI,datosD,comp,folder,dirs,orientation, unit, format):
        super().__init__(orientation, unit, format)
        # self.firstname = p_info[0]
        # self.lastname = p_info[1]
        self.name = p_info[0][:-1]
        self.age = str(p_info[1])
        self.pathgy = p_info[2]
        self.id = str(p_info[3])
        self.porcentajeI=[datosI[0][0],datosI[1][0]]
        self.desviacionI=[datosI[0][1],datosI[1][1]]
        self.porcentajeD=[datosD[0][0],datosD[1][0]]
        self.desviacionD=[datosD[0][1],datosD[1][1]]
        self.folder=folder
        self.dirder=dirs[0]
        self.dirizq=dirs[1]

        self.comp=comp
        
#firstname, lastname, age, pahtology, p_id

    def header(self):
        if self.comp==0:
              self.image(str(self.folder)+'/ic.jpg',40,80,55)
              self.image(str(self.folder)+'/dc.jpg',160,80,55)
        else:
            self.image(str(self.dirizq),30,80,55)
            self.image(str(self.dirder),180,80,55)
            self.image(str(self.folder)+'/ic.jpg',80,80,55)
            self.image(str(self.folder)+'\dc.jpg',240,80,55)


        self.image('roosevelt.png', 10, 3, 30)

        
        self.set_font('Times', 'B', 10)

        self.text(87, 13, "INSTITUTO ROOSEVELT - LABORATORIO DE ANÁLISIS DE MOVIMIENTO")
        self.text(106, 19, "REPORTE DE RESULTADOS TRAYECTORIA DEL COP ")
        self.text(25, 30, "NOMBRE:")
        self.text(195, 30, "EDAD:")
        self.text(25, 36, "DIAGNÓSTICO DE REMISIÓN:")
        self.text(195, 36, "ID:")
        self.set_font('Times', 'I', 9)


        
        



        self.text((195 + 55 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.name) / 2, 30, self.name)
        
        self.text(220, 30, self.age  + " años")
        self.text((195 + 55 + self.get_string_width('DIAGNÓSTICO:')) / 2 - self.get_string_width(self.pathgy) / 2, 36, self.pathgy) #130 - len(self.pathgy)
        self.text(218, 36, self.id)


        if self.comp==0:
             self.text(85, 100, "Porcentaje:")
             self.text(80,110, "Desviación estandar:")
             self.text(230,100, "Porcentaje:  ")
             self.text(220,110, "Desviación estandar: ")
             self.text(120, 100, ''.join([str(self.porcentajeI[0]),'','%']))
             self.text(120, 110, ''.join([str(self.desviacionI[0]),'','%']))           
             self.text(255, 100,''.join([str(self.porcentajeD[0]),'','%']) )
             self.text(255, 110, ''.join([str(self.desviacionD[0]),'','%']))
        else:
            
            self.text(60, 160, "ANTERIOR")
            self.text(60, 170,  ''.join([str(self.porcentajeI[1]),'','%']))
            self.text(100, 160, "NUEVO")
            self.text(100, 170,  ''.join([str(self.porcentajeI[0]),'','%']))

            self.text(20, 170, "Porcentaje:")
            self.text(20, 180, "Desviación estandar:")
            self.text(60, 180,  ''.join([str(self.desviacionI[1]),'','%']))
            self.text(100, 180,  ''.join([str(self.desviacionI[0]),'','%']))

            self.text(180, 170, "Porcentaje:")
            self.text(180, 180, "Desviación estandar:")


            self.text(220, 160, "ANTERIOR")
            self.text(220, 170,  ''.join([str(self.porcentajeD[1]),'','%']))
            self.text(260, 160, "NUEVO")
            self.text(260, 170,  ''.join([str(self.porcentajeD[0]),'','%']))

            self.text(180, 170, "Porcentaje:")
            self.text(180, 180, "Desviación estandar:")
            self.text(220, 180,  ''.join([str(self.desviacionD[1]),'','%']))
            self.text(260, 180,  ''.join([str(self.desviacionD[0]),'','%']))


            

        
        self.set_font('Times', 'B',12)
        self.set_text_color(0)
        self.text(60,70, "PIE IZQUIERDO")

        self.text(220,70, "PIE DERECHO")

        self.set_font('Times','I',8)
        self.set_text_color(12)



        

        



    def footer(self):
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')     








