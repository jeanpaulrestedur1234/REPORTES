from math import sqrt
from CODIGOS.kin_emg_plot import planes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import os
from CODIGOS.extractor import*



def find_cmc(p_path,runs_mdx, joint,dh):

    info=[]
    cols=[]
    desviation=np.median(dh[joint.replace('ac','') +'.S'])
    for i in range(len(runs_mdx)):
        data = extract_angles(f'{p_path}{os.sep}{runs_mdx[i]}')

        info.append(data[joint])
        cols.append(f'X{i}')
   

    df = pd.DataFrame(info).transpose()
    



    df.columns =  cols
    cmc_v = []
 #   asa=[]
  #  fig, axs = plt.subplots()
    x_vec=[]
    for i in range(len(df[df.columns[0]])):
        x_vec.append(i)

    

    #  creo el intervalo de evalucion

    rango=desviation/sqrt(2)
    h=0
 
    for run in (range(df.shape[1])):
        for i in range(h,(df.shape[1])-1):

            
            
            X, y = df[df.columns[h]], df[df.columns[i+1]]


            distancias=abs(np.array(X)-np.array(y))/sqrt(2)
            cuantas_caen=sum(distancias<rango)/len(distancias)
            cmc_v.append(cuantas_caen)

        h=h+1
    cmc_v = [round(cmc_v[_], 3) for _ in range(len(cmc_v))]

    return cmc_v



def cmc(age,p_path,runs_mdx): 

    cmc_total = []
    cmc_avg_total = []
    index = []
    planes_dict = planes()
    planes_v = planes_dict['sagittal'] + planes_dict['frontal'] + planes_dict['transverse']   
    if age <= 16:
        sheet_name = 'DH_Children'
    else:
        sheet_name = 'DH_Adults'
    dh = pd.read_excel(os.sep.join(['normatives','dh_normal.xlsx']), sheet_name = sheet_name,  header = 7, index_col = 0).dropna()
 

    joints = ['ac' + joint for joints in planes_v for joint in joints]
    columns=[]
    h=0

    for run in (range(len(runs_mdx)-1)):
        for i in range(h,len(runs_mdx)-1):
            t1=runs_mdx[h].split()[1].replace('.mdx','')
            t2=runs_mdx[i+1].split()[1].replace('.mdx','')
            columns.append(f'comparacion{t1}-{t2}')
        h=h+1




    for joint in joints:
        cmc_v = find_cmc(p_path,runs_mdx,joint,dh)
        
        cmc_total.append(cmc_v)

        index.append(joint)

    planes_titles =  planes_dict['sagittal_titles'] + planes_dict['frontal_titles'] + planes_dict['transverse_titles']
    index_2d = [[title + ' Derecha', title + ' Izquierda'] for title in planes_titles]
    index = [title for titles in index_2d for title in titles]      #flatten vector
    #columns = [f'{runs[0]}-{runs[1]}', f'distancia{runs[0]}-{runs[1]}',f'{runs[1]}-{runs[2]}',f'distancia{runs[1]}-{runs[2]}',f'{runs[0]}-{runs[2]}',f'distancia{runs[0]}-{runs[2]}']
  


    df2save =pd.DataFrame(cmc_total, columns=columns, index=index)
   
    return df2save
