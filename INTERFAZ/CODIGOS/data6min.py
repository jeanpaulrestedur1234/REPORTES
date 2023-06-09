import pandas as pd
import os

def prepare_data(df):
    df.dropna(axis=0, thresh=3, inplace=True)
    df.columns = df.iloc[0,:]
    df = df[df != df.columns].dropna(axis=0, thresh = 5).reset_index(drop=True)
    return df


def read_data():
    general_data = pd.read_excel('Data_6Minutes.xlsx', sheet_name='Datos generales').dropna(thresh=2).drop(5).reset_index(drop=True)
    section_data = pd.read_excel('Data_6Minutes.xlsx', sheet_name='Datos por tramo')
    
    # Saving sec_data in new sheet
    
    path = os.getcwd()   
    writer = pd.ExcelWriter(path + '/' + 'Data_6Minutes.xlsx', engine = 'openpyxl', mode = 'a',  if_sheet_exists = 'replace')
    prepare_data(section_data).to_excel(writer, sheet_name = 'Datos Completos')
    writer.save()
    return general_data, prepare_data(section_data)


    

    

