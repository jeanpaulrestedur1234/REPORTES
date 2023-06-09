from cProfile import run
import os
import shutil
import time
import asyncio
import pandas as pd


from CODIGOS.sixmin_pdf import PDF_6min  
from CODIGOS.varsix_pdf import PDF_var
from CODIGOS.sixmin import six_min
from CODIGOS.var_6min import var_six

def split_name(name):
    if len(name.split()) == 3:
        return  name.split()[0], ' '.join(name.split()[1:3])
    return ' '.join(name.split()[0:2]), ' '.join(name.split()[2:4])


async def save_excel(df, path, folder, file_name):
    writer = pd.ExcelWriter(
        os.sep.join([path, folder, f'Data6_min_{file_name}.xlsx']), 
        engine='xlsxwriter'
    )
    df.to_excel(writer, sheet_name='Datos 6 Minutos',
        index_label= 'INTERVALOS DE TIEMPO (s)'
    )
    workbook  = writer.book
    worksheet = writer.sheets['Datos 6 Minutos']
    wrap_format = workbook.add_format({'text_wrap': True})
    wrap_format.set_align('rigth')
    worksheet.set_column(4,7,40, wrap_format)
    worksheet.set_column(1,3,19, wrap_format)
    worksheet.set_column(0,0,25, wrap_format)

    writer.save()
    print('¡Excel CREATED!')


def findfolder():
    path = os.getcwd()      #os.path.dirname(__file__) --> another option
    for file in os.listdir(path):
        for strings in file.split(): 
            if strings.isdigit():
                folder = file
                return path, folder


def p_data(path, folder, file_name):

    p_id = [int(s) for s in folder.split() if s.isdigit()][0]

    p_name = file_name[:-1] if file_name[-1].isdigit() else file_name
    #firstname, lastname = split_name(p_name)
    
    try:
        with open(os.sep.join([path, folder, '/NOTA.txt']), encoding='utf8') as f:
            lines = f.read()
    except UnicodeDecodeError:
        with open(os.sep.join([path, folder, '/NOTA.txt']), encoding='latin-1') as f:
            lines = f.read()
    finally:
        age = [int(s) for s in lines.split() if s.isdigit()][0]
        for index, line in enumerate(lines.split()):
            if line == 'DIAGNOSTICO:':
                index_0 = index + 1
            elif line == '6MIN': 
                index_f = index
        pathology = ' '.join(lines.split()[index_0:index_f])
    
    return p_name, age, pathology, p_id


def six_min_sensor(patient_info, path, folder, file_name):
    t0 = time.time()
    print('Six_min')
    data_6min = six_min(patient_info[1], path+ folder)

    asyncio.run(save_excel(data_6min, path, folder, file_name))
   
    pdf = PDF_6min(patient_info, 'P', 'mm', 'letter')
    pdf.pag1()
    pdf.pag2()
    pdf.pag3()

    try:
        pdf.output(os.sep.join([path, folder, f'{file_name}_6 MIN CON SENSOR.pdf']),'F')
    except PermissionError:
        print('You have an open pdf with the same name')
        return
    print(f'¡PDF1s CREATED! in {os.sep.join([path, folder])}')
    print(f'time elapsed {time.time() - t0}')
    

 
def var_sixmin(patient_info, path, folder, file_name): 
    t0 = time.time()   
    print('Varsix')
    idc, linear_tend, cv_avg = var_six(patient_info[1],path +folder)

    pdf = PDF_var(
        patient_info, idc, linear_tend, cv_avg,
        'L', 'mm', 'letter'
    )
    pdf.pag1()
    pdf.pag2()
    pdf.pag3()
    pdf.pag4()

    try:
        pdf.output(os.sep.join([path, folder, f'{file_name}_VAR_6MIN.pdf']), 'F')
    except PermissionError:
        print('You have an open pdf with the same name')
        return
    print(f'¡PDF2s CREATED! in {os.sep.join([path, folder])}')
    print(f'time elapsed {time.time() - t0}')

    
    


    



    
    
    
    
    

    