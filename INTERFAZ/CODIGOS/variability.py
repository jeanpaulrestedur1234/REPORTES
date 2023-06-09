from CODIGOS.data import read_data6min
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from CODIGOS.values_control import control_values


def stats_gen(df):
    '''General statistics
    
    This function returns the mean, std and coefficient of variation as a dataframe. 

    '''


    k=df.mean(axis=0)

 
  
    return pd.concat([df.mean(axis=0), df.std(axis=0), df.std(axis=0) / df.mean(axis=0) * 100], axis=1).transpose()

def stats_table(df, col, control, titl):
    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4],
    columnwidth = [1,1,1,1],
    header=dict(values= ['', '<b>Izquierdo</b>', '<b>Derecho</b>', '<b>Control</b>'], 
                fill_color='white',
                align='center',
                font=dict(color='black', size=13, family = "Helvetica"),
                line_color='white'),
        
    cells=dict(values = ['<b>' + df.index + '</b>', df.loc[:,col[0]], df.loc[:, col[1]], ['', '', '<b>' + control + '</b>']],
                align = 'center',
                fill_color = 'white',
                font = dict(color = 'black', size = 13, family = "Helvetica"),
                line_color = 'white'))
    ])
    fig.update_layout(width=450, height=170, margin={'l': 0, 'r': 0.5, 't': 25, 'b': 0}, 
                    title=dict(text=titl, x=.5, font_size=13, font_color='black', font_family = "Helvetica")
                    )

    return fig


def table_15s(table):

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4],
    columnwidth = [1,1,1,1],
    header=dict(values= ['CV' , 'Promedio']*2, 
                fill_color='#cccccc',
                align='center',
                font=dict(color='black', size=13, family = "Helvetica"),
                line_color='black'),
        
    cells=dict(values= table, 
                align='center',
                fill_color=[['white', '#f2f2f2'] * 12],
                font=dict(color = 'black', size = 13, family = "Helvetica"),
                line_color='black'))
    ])

    fig.update_layout(
        width=300, height=220, margin={'l': 0, 'r': 0.5, 't': 25, 'b': 0},
        title=dict(text='<b>Izquierda</b>' + ' '*22 + '<b>Derecha</b>', x=.5, font_size=13, font_color='black', font_family = "Helvetica")
    )
    return fig   

def column_names():
    return  {'stride_dur' : ['Duración de la zancada izquierda (s)', 'Duración de la zancada derecha (s)'],
                'stride_len' : ['Longitud de la zancada izquierda (m)', 'Longitud de la zancada derecha (m)'],
                'stride_vel' : ['Velocidad de la zancada izquierda (m/s)', 'Velocidad de la zancada derecha (m/s)'],
                'stride_cad' : ['Cadencia de la zancada izquierda (pasos/min)', 'Cadencia de la zancada derecha (pasos/min)'],
                'step_dur' : ['Duración del paso izquierdo (s)', 'Duración del paso derecha (s)'],
                'step_len' : ['Left Step Length (m)', 'Right Step Length (m)'],
                'osc_time' : ['Duración de Oscilaciòn de la zancada izquierda (%)', 'Duración de Oscilaciòn de la zancada derecha (%)']}



def table_title(cols):
    if cols == 'step_len':
        title = 'Longitud de Paso (m)'
    else:
        title = column_names()[cols][0].split()
        title.pop(-2)
        title = ' '.join(title)
    return title


def variation(age,folder):
    general, datos=read_data6min(folder)
    colnames=column_names()
    df_stats = stats_gen(datos).set_index(pd.Index(['Promedio', 'Desviación Estandar', 'C.V.(%)']))   

    for col in colnames.keys():
        tabla=[]
        info=datos[colnames[col]]
        info['Recorrido']=datos['Recorrido']      

        control = control_values(col, age)


        for recorrido in np.unique(info['Recorrido']):
              
              
              
   
              d_tabla=info[info['Recorrido']==recorrido]
        
              
              mL=np.mean(d_tabla[colnames[col][0]])
              mR=np.mean(d_tabla[colnames[col][1]])
              sL=np.std(d_tabla[colnames[col][0]])
              sR=np.std(d_tabla[colnames[col][1]])
              tabla.append([round(sL/mL*100,2),round(mL ,2),round(sR/mR*100,2),round(mR,2) ])

        

        
        fig=table_15s(np.transpose(tabla))
        fig.write_image('Vairabillityinfo/'+'images/'+col+'15s.png' , scale=5)
        title = table_title(col)
        fig2= stats_table(df_stats.round(3), column_names()[col], control, title)
        fig2.write_image('Vairabillityinfo/'+'images/' + col +'stats.png' , scale=5)
        
    
        
