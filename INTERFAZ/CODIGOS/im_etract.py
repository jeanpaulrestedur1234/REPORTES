import PyPDF2
from PIL import Image




def extraccion(name,num_im,pie_n):
     
     file=PyPDF2.PdfFileReader(open(name,"rb"))
     page0=file.pages[0]
     xObject=page0['/Resources']['/XObject'].getObject()
     print()

     obj=str(list(xObject.keys())[num_im])
     if xObject [obj]['/Subtype'] == '/Image':
        size = (xObject [obj]['/Width'], xObject [obj]['/Height'])
        data = xObject [obj].getData()
        mode = "RGB"


        if xObject [obj]['/Filter'] == '/FlateDecode':
            img= Image.frombytes (mode, size, data)
            img.save(pie_n +".png")
        elif xObject [obj]['/Filter'] =='/DCTDecode':
            img = open (pie_n+ ".jpg", "wb")
            img.write(data)





