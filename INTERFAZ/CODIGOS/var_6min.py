import pandas as pd 

from CODIGOS.data import read_data6min
from CODIGOS.values_control import control_values
from CODIGOS.plt_table_var import(
    plt_tables,
    column_names
) 
from CODIGOS.sixmin import (
    time_vector,
    time_markers,
    sec_avg_data,
    walk_data,
    sess_data
)


def stats_gen(df):
    '''General statistics
    
    This function returns the mean, std and coefficient of variation as a dataframe. 
    '''
    return pd.concat([df.mean(axis=0), df.std(axis=0), df.std(axis=0) / df.mean(axis=0) * 100], axis=1).transpose()


def var_six(age, folder):

    gen_data, sec_data = read_data6min(folder=folder)
    _, distance, height, weight, gender, _  = sess_data(gen_data)
    idc, ln_tend, _ = walk_data(age, gender, height, weight, distance)

    avg_data_15s, std_data_15s = sec_avg_data(sec_data, time_markers(time_vector(sec_data), len(sec_data)), standar=True)
    
    cv_df_15s = (std_data_15s / avg_data_15s * 100).astype('float64')

    df_stats = stats_gen(sec_data).set_index(pd.Index(['Promedio', 'Desviación Estandar', 'C.V.(%)']))

    colnames = ['stride_dur', 'stride_len', 'stride_vel', 'stride_cad', 'step_dur', 'step_len', 'osc_time']
    
    avg_cv = []
    for col in colnames:
        control = control_values(col, age)
        avg_cv.append(cv_df_15s.loc[:,column_names()[col]].mean(axis=0).round(3).to_list())
        plt_tables(df_stats.round(3), avg_data_15s.round(3), cv_df_15s.round(3), col, control)

    return idc, ln_tend, avg_cv 
