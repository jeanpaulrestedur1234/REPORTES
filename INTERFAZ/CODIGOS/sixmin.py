import numpy as np
import pandas as pd
import warnings

from CODIGOS.data import read_data, read_data6min
from CODIGOS.plt_table_sixdata import plt_table
from CODIGOS.plt_graphs import plot_fig
from math import floor


def sess_data(df):

    s_data = { 'Duración del análisis (min:sec)': df[df.keys()[1]][1],
                'Distancia total recorrida': str( df[df.keys()[1]][2]) + ' m',
                'Número de recorridos (tramos)':  df[df.keys()[1]][3], 
                'Número de descansos':  df[df.keys()[1]][4],
                'Simetría general promedio':  df[df.keys()[1]][5],
                'Velocidad promedio': str( df[df.keys()[1]][6]) + ' <b>m/s</b>',
                'Cadencia promedio': str( df[df.keys()[1]][7]) + ' <b>pasos/min</b>',
                'Longitud de zancada promedio': str( df[df.keys()[1]][8]) + ' <b>m</b>'
                }
    dfs_data = pd.DataFrame.from_dict(data=s_data, orient='index', columns = ['Valor'])
    dfs_data.columns.name = 'Descripción de Parámetro'

    normal_values = df.iloc[6:9,2].to_list()
    return dfs_data, df[df.keys()[1]][9:].to_numpy(), df.Talla[0], df.Peso[0], df.Gender[0], normal_values


def walk_data(age, gndr, ht, wt, d):
    '''Walk data
    
    This function returns the WDI (walking distance index), the linear tendency
    and the teoric percentage (age-dependent)
    '''
    
    factor = np.array([-5,-3,-1,5,3,1])
    if age < 18:
        ht /= 100
        if gndr == 'M':
            ind = 196.72 + (39.81 * age) - (1.36 * (age**2)) + (132.28 * ht) 

        else: 
            ind = 188.61 + (51.50 * age) - (1.86 * (age**2)) + (86.10 * ht)

    else: 
        if gndr == 'M':
            ind = (6.22 * ht) - (2.99 * wt) - (0.52 * age) - 183.06
        else:
            ind = (2.64 * ht) - (2.12 * wt) + (0.12 * age) + 330.2
 

    
    return (d[5] - d[0]) / d[0] * 100,  np.round(np.dot(factor, d) / 70, 2) , np.sum(d) / ind * 100  
    

def time_vector(df):
    #dataframe columns names are the same as in excel

    if df['Contacto inicialde de la zancada izquierda (s)'].min() < df['Contacto inicial de la zancada derecha (s)'].min():
        return df['Contacto inicialde de la zancada izquierda (s)'].dropna().to_numpy(dtype='float64')        
    return df['Contacto inicial de la zancada derecha (s)'].dropna().to_numpy(dtype='float64')


def time_markers(v_t, length):
    ''' This function return a vector with the index where 
    the values of v_time are greater than 15 and their multiplies up 
    to 24.'''

    # t_s = [np.where(v_t >= 15 * i)[0] for i in range(1, 24)]
    # t_s = [t_s[i][0] for i in range (len(t_s))]

    n = 0
    t_s = []
    for i in range(len(v_t)):
         if v_t[i] >=  n + 15  :
            t_s.append(i)
            n += 15
    t_s = np.insert(t_s, 0, -1)                          # to start at index 0 in the next function (sec_avg_data) we add -1
        
    if len(t_s) < 25: t_s = np.insert(t_s, len(t_s), length)        # to go all the way to the end of the data 


    return t_s


def sec_avg_data(df, t_s, standar = False):
    ''' Section average data 

    This function returns a dataframe with the average and standar deviation if is required (standar = True)
    of some columns from the dataframe received with the section data, in intervals of 15 seconds (time stamps(t_s))
    to the end.
    '''

    avg_df = pd.DataFrame(columns=[df.columns[6], df.columns[7], df.columns[8], df.columns[9],
                        df.columns[10], df.columns[11], df.columns[14], df.columns[15], 
                        df.columns[16], df.columns[17], df.columns[18], df.columns[19],
                        df.columns[20], df.columns[21], df.columns[28], df.columns[29]]) 

    for row in range(len(t_s) - 1):
        avg_df.loc[row,avg_df.columns] = df.loc[t_s[row] + 1:t_s[row + 1], avg_df.columns].mean()

    if standar:
        std_df = pd.DataFrame(columns=[df.columns[6], df.columns[7], df.columns[8], df.columns[9],
                        df.columns[10], df.columns[11], df.columns[14], df.columns[15], 
                        df.columns[16], df.columns[17], df.columns[18], df.columns[19],
                        df.columns[20], df.columns[21], df.columns[28], df.columns[29]]) 
        for row in range(len(t_s) - 1):
            std_df.loc[row,avg_df.columns] = df.loc[t_s[row] + 1:t_s[row + 1], avg_df.columns].std()
        return avg_df.astype('float64'), std_df.astype('float64')

    return avg_df.astype('float64')


def avg_data_bs(df):
    '''Average data between both sides

    This function returns a data frame with the average between left and rigth
    side. 
    '''

    bs_avg_data = pd.DataFrame(columns=['CADENCIA', 'VELOCIDAD', 'LONGITUD ZANCADA', 'DURACION DE LA ZANCADA',
                    'DURACION DEL PASO', 'DURACION DE APOYO', 'DURACION DE OSCILACION','LONGITUD DE PASO'])
    for col in range(0,len(df.columns),2):
        bs_avg_data.iloc[:, floor(col/2)] = df.iloc[:, col :col + 2].mean(axis=1)

    return bs_avg_data


def data_out(both_sides, avg_sides):
    '''
    This function return the data that will be save 
    in .xlsx format in the selected folder. 
    ''' 
    intervals = [str(i) + '-' + str(i + 15) for i in range(0, 360, 15)]
    
    data2save = pd.DataFrame(columns=['CADENCIA', 'VELOCIDAD', 'LONGITUD ZANCADA', 'DURACION CICLO DE MARCHA IZQUIERDO',
                    'DURACION CICLO DE MARCHA DERECHO', 'DURACION DE PASO IZQUIERDO', 'DURACION DE PASO DERECHO'], index=intervals)

    datos=min([len(avg_sides),len(data2save)])   
    data2save.iloc[0:datos,0:3] = avg_sides.iloc[0:datos,0:3]
    data2save.iloc[0:datos,3:5] = both_sides.iloc[0:datos,6:8]
    data2save.iloc[0:datos,5:7] = both_sides.iloc[0:datos,8:10] 
    data2save.columns.name = 'INTERVALOS DE TIEMPO'
    return data2save


def plt(time, btwside_avg_data, avg_data):

    plot_fig( 'Tiempo(s)', 'Cadencia (pasos/min)', 'cadencia', time, btwside_avg_data['CADENCIA'])
    plot_fig( 'Tiempo(s)', 'Velocidad (m/s)', 'velocidad', time, btwside_avg_data['VELOCIDAD'])
    plot_fig( 'Tiempo(s)', 'Longitud Zancada (m)', 'longitud_zancada', time, btwside_avg_data['LONGITUD ZANCADA'])
    plot_fig( 'Tiempo(s)', 'Duración ciclo de marcha (s)', 'duracion_marcha', time,
            avg_data['Duración de la zancada izquierda (s)'], avg_data['Duración de la zancada derecha (s)'] , 
            plot2sides=True)
    plot_fig( 'Tiempo(s)', 'Duración de paso (s)', 'duracion_paso', time,
            avg_data['Duración del paso izquierdo (s)'], avg_data['Duración del paso derecha (s)'] , 
            plot2sides=True)
    plot_fig( 'Tiempo(s)', 'Duración fase de apoyo (%)', 'duracion_apoyo', time,
            avg_data['Duración de Apoyo de la zancada izquierda (%)'], avg_data['Duración de Apoyo de la zancada derecha (%)'] , 
            plot2sides=True)
    plot_fig( 'Tiempo(s)', 'Duración fase de oscilación (%)', 'duracion_oscilacion', time,
            avg_data['Duración de Oscilaciòn de la zancada izquierda (%)'], avg_data['Duración de Oscilaciòn de la zancada derecha (%)'] , 
            plot2sides=True)
    plot_fig( 'Tiempo(s)', 'Longitud de paso (m)', 'longitud_paso', time,
            avg_data['Left Step Length (m)'], avg_data['Right Step Length (m)'], 
            plot2sides=True)


def six_min(age,folder):
    gen_data,sec_data = read_data6min(folder=folder)
    
    session_data, distance, height, weight, gender, normal_values  = sess_data(gen_data)
    
    idc, linear_tend, teoric_per = walk_data(age, gender, height, weight, distance)
    
    if teoric_per < 0:
        warnings.warn("Porcentaje teorico negativo, revisar peso y talla")
        
    # concatenate walk data and session data into one dataframe

    w_data = pd.DataFrame([round(idc,2), linear_tend, str(round(teoric_per,2)) + '%'], 
            index=['Indice de distancia caminada', 'Tendencia linear', 'Porcentaje Teórico'], 
            columns=['Valor'])  

    session_data = pd.concat([session_data, w_data])
    session_data.columns.name = 'Descripción de Parámetro'

    #extract time vector and find time stamps each 15 seconds. 

    v_time = time_vector(sec_data)
    t_stamps = time_markers(v_time, len(sec_data))

    #find the mean each 15 seconds. 

    avg_data = sec_avg_data(sec_data, np.rint(t_stamps))
    btwside_avg_data = avg_data_bs(avg_data)
    data2save = data_out(avg_data, btwside_avg_data)

    #preparing time vector for plotting

    t_stamps[-1] -= t_stamps[-1] - len(v_time) + 1
    t_stamps = np.delete(t_stamps,0)

    time = v_time[t_stamps]

    # Plotting

    plt_table(session_data, normal_values)
    plt(time, btwside_avg_data, avg_data)

    return data2save#, avg_data, time
    
