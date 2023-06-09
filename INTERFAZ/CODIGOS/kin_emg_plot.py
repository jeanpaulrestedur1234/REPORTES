import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os


def planes():
    return {
        'sagittal': [['RPTILT', 'LPTILT'], ['RHPFE', 'LHPFE'], ['RKFE', 'LKFE'], ['RAFE', 'LAFE']],
        'frontal': [['RPOBLI', 'LPOBLI'], ['RHPAA', 'LHPAA'], ['RKAA', 'LKAA']],
        'transverse': [['RPROT', 'LPROT'], ['RHPIE', 'LHPIE'], ['RKIE', 'LKIE'], ['RAIE', 'LAIE']],
        'sagittal_titles': ['Pelvis Inclinación', 'Cadera Flexión-Extensión', 'Rodillas Flexión-Extensión', 'Tobillos Flexión-Extensión'],
        'frontal_titles': ['Pelvis Oblicuidad', 'Cadera Abducción-Aducción', 'Rodillas Valgo-Varo'],
        'transverse_titles': ['Pelvis Rotación', 'Cadera  Rotación', 'Rodillas  Rotación', 'Tobillos Progresión Pie']
    } 
def studys():
    return { 'F':[['fcRGRAP','fcLGRAP'],['fcRGRVE','fcLGRVE'],['fcRGRML','fcLGRML']],   #F FUERZAS
        'M':[['tcRAFE','tcLAFE'],['tcRHPFE','tcLHPFE'],['tcRKFE','tcLKFE']],                 #M MOMENTOS
        'P':[['pcRKFE','pcLKFE'],['pcRAFE','pcLAFE'],['pcRHPFE','pcLHPFE']],
        'Ml':[['tcRHPAA','tcLHPAA'],['tcRKAA','tcLKAA']],
                                                        
#['pcRKIE','pcLKIE'],['pcRHPAA','pcLHPAA']

        'M_titles':['Momento Tobillo','Momento Cadera','Momento Rodilla'],
        
        'F_titles':['Fuerza Antero-Posterior','Fuerza Vertical','Fuerza Medio-Lateral'],
        'P_titles':['Potencia Rodilla','Potencia Tobillo','Potencia Cadera'],
        'Ml_titles':['Momento Cadera','Momento Rodilla']
    }
def adjus_lim(lim, step):
    while lim % step != 0:
        lim += 1 if lim > 0 else -1 
    return lim

def limits(*args) -> tuple[int, int]:
    args = list(args)
    max_v, min_v, std_v = [], [], []
    for df in range(len(args)):
        max_v += [args[df].values.max()]
        min_v += [args[df].values.min()]
        std_v += [args[df].values.std()]
    
    return int(np.max(max_v) + np.max(std_v)), int(np.min(min_v) - np.max(std_v))

def cin_cut(x_values,y_values,RT):
    x_values=np.array( x_values)
    important=list(y_values[:len(x_values[x_values<RT])])
    not_important=list([np.nan]*(len(y_values)-len(x_values[x_values<RT])))

    z=important+not_important
   
    return z




def plt_kin(kin_data,dh_data, plane, toe_off):
    if plane == 'frontal':
        w, h = 5, 7.5
    else:
        w, h = 5, 10

    clm_names = planes()[plane]
    titles = planes()[f'{plane}_titles']
    num_subplots = len(clm_names)
    x_value = kin_data.index
    rto, lto = toe_off

    fig, axs = plt.subplots(num_subplots, 1, figsize=(w, h))
    fig.subplots_adjust(hspace=0.7, wspace=0.3)

    for i in range(num_subplots):
        data2plot = kin_data[['ac' + string for string in clm_names[i]]]
  
   

        dh_data_tr = dh_data[clm_names[i][0] + '.M'] + dh_data[clm_names[i][0] + '.S']
        dh_data_dr = dh_data[clm_names[i][0] + '.M'] - dh_data[clm_names[i][0] + '.S']
        dh_data_tl = dh_data[clm_names[i][1] + '.M'] + dh_data[clm_names[i][1] + '.S']
        dh_data_dl = dh_data[clm_names[i][1] + '.M'] - dh_data[clm_names[i][1] + '.S']

        # Plotting normality
       
        # ytop, ybottom = limits(data2plot, dh_data_tr, dh_data_tl, dh_data_dr, dh_data_dl)   # Uncomment for find limits with 

        
        axs[i].fill_between(x_value, dh_data_tr, dh_data_dr, color = 'lightgrey')
        axs[i].fill_between(x_value, dh_data_tl, dh_data_dl, color = 'lightgrey')
        axs[i].plot(x_value,dh_data[clm_names[i][0] + '.M'], color = 'darkgrey')
        axs[i].plot(x_value,dh_data[clm_names[i][1] + '.M'], color = 'darkgrey')

        
        # Plotting right and left side                            _data

        axs[i].plot(x_value, data2plot[data2plot.columns[0]], color = 'forestgreen',linewidth=3)
        axs[i].plot(x_value, data2plot[data2plot.columns[1]], color = 'red',linewidth=3)
        
        # Points at the global max and min 

        axs[i].plot(data2plot[data2plot.columns[0]].idxmax(), data2plot[data2plot.columns[0]].max(), 
                    marker="o", markersize=3, c='darkblue')
        axs[i].plot(data2plot[data2plot.columns[1]].idxmax(), data2plot[data2plot.columns[1]].max(), 
                    marker="o", markersize=3, c='darkblue')
        axs[i].plot(data2plot[data2plot.columns[0]].idxmin(), data2plot[data2plot.columns[0]].min(), 
                    marker="o", markersize=3, c='darkblue')
        axs[i].plot(data2plot[data2plot.columns[1]].idxmin(), data2plot[data2plot.columns[1]].min(), 
                    marker="o", markersize=3, c='darkblue')

        axs[i].set_title(titles[i], fontweight="bold")
        axs[i].set(xlabel='Ciclo (%)', ylabel='Ángulo (deg)')
        axs[i].axvline(x = rto, ymin = 0, ymax = 1, color = 'darkgreen')
        axs[i].axvline(x = lto, ymin = 0, ymax = 1, color = 'salmon')
        axs[i].axhline(y = 0, color = 'dimgray',  linestyle = '--')
        axs[i].margins(x=0.01, y=0.1)
        axs[i].tick_params(top = True)
        ybottom, ytop = axs[i].get_ylim()
        
        step = np.diff(axs[i].get_yticks())[0]
        ytop, ybottom = adjus_lim(int(ytop), step), adjus_lim(int(ybottom), step)
        axs[i].set_ylim(ybottom, ytop)        
           
    plt.tight_layout()
    plt.savefig(os.sep.join(['images', f'{plane}.png']), dpi=200)



def plt_cin(kin_data,dh_data,study, toe_off):

    if study=='Ml':
        w,h=3 ,9
    else:
        w, h =  4, 15


    ylabels={'F':'Fuerza(N)','M':'Momento(N*m)','P':'Energia(W)','Ml':'Momento(N*m)' }
   
    

    clm_names = studys()[study]
    titles = studys()[f'{study}_titles']
    num_subplots = len(clm_names)
    x_value = kin_data.index
    rto, lto = toe_off

   

    fig, axs = plt.subplots(1,num_subplots, figsize=(h,w))
    fig.subplots_adjust(hspace=0.7, wspace=0.3)

    




    for i in range(num_subplots):
        data=pd.DataFrame()
        data2plot = kin_data[[ string for string in clm_names[i]]]

        data[data2plot.columns[0]]=cin_cut(x_value,data2plot[data2plot.columns[0]],rto)
        data[data2plot.columns[1]]=cin_cut(x_value,data2plot[data2plot.columns[1]],lto)
        
        
        dh_data_tr =( dh_data[clm_names[i][0][2:] + '.M'] + dh_data[clm_names[i][0][2:]  + '.S'])
        dh_data_dr =(dh_data[clm_names[i][0][2:]  + '.M'] - dh_data[clm_names[i][0][2:] + '.S'])
        dh_data_tl =(dh_data[clm_names[i][1][2:]  + '.M'] + dh_data[clm_names[i][1][2:]  + '.S'])
        dh_data_dl =(dh_data[clm_names[i][1][2:] + '.M'] - dh_data[clm_names[i][1][2:]  + '.S'])
        



        # Plotting normality
    
        # ytop, ybottom = limits(data2plot, dh_data_tr, dh_data_tl, dh_data_dr, dh_data_dl)   # Uncomment for find limits with 

        
        axs[i].fill_between(x_value, dh_data_tr, dh_data_dr, color = 'lightgrey')
        axs[i].fill_between(x_value, dh_data_tl, dh_data_dl, color = 'lightgrey')
        axs[i].plot(x_value, dh_data[clm_names[i][0][2:] + '.M'], color = 'darkgrey')
        axs[i].plot(x_value, dh_data[clm_names[i][1][2:]  + '.M'], color = 'darkgrey')
        
        # Plotting right and left side                            _data

        axs[i].plot(x_value, data[data2plot.columns[0]], color = 'forestgreen',linewidth=3)
        axs[i].plot(x_value, data[data2plot.columns[1]], color = 'red',linewidth=3)
        
        
        # Points at the global max and min 

        axs[i].plot(data[data2plot.columns[0]].idxmax(), data[data2plot.columns[0]].max(), 
                    marker="o", markersize=3, c='darkblue')
        axs[i].plot(data[data2plot.columns[1]].idxmax(), data[data2plot.columns[1]].max(), 
                    marker="o", markersize=3, c='darkblue')
        axs[i].plot(data[data2plot.columns[0]].idxmin(), data[data2plot.columns[0]].min(), 
                    marker="o", markersize=3, c='darkblue')
        axs[i].plot(data[data2plot.columns[1]].idxmin(), data[data2plot.columns[1]].min(), 
                    marker="o", markersize=3, c='darkblue')
        
        

        axs[i].set_title(titles[i], fontweight="bold")
        axs[i].set(xlabel='Ciclo (%)', ylabel=ylabels[study])
        axs[i].axvline(x = rto, ymin = 0, ymax = 1, color = 'darkgreen')
        axs[i].axvline(x = lto, ymin = 0, ymax = 1, color = 'salmon')
        axs[i].axhline(y = 0, color = 'dimgray',  linestyle = '--')
        axs[i].margins(x=0.01, y=0.1)
        axs[i].tick_params(top = True)
        ybottom, ytop = axs[i].get_ylim()
        #max(max(dh_data_tr),max(dh_data_tl),max(data2plot.columns[0]),max(data2plot.columns[1]))
        
        step = np.diff(axs[i].get_yticks())[0]
        if (ybottom> -1) &(ytop<1) :
            ybottom, ytop= -1,1
        elif (ybottom> -1.5) &(ytop<1.5) :
            ybottom, ytop= -1.5,1.5
        elif (ybottom> -2) &(ytop<2) :
            ybottom, ytop= -2,2
        else:
            ytop, ybottom = adjus_lim(int(ytop), step), adjus_lim(int(ybottom), step)
        axs[i].set_ylim(ybottom, ytop,titles[i]) 
        
               
           
    plt.tight_layout()
    plt.savefig(os.sep.join(['images/', f'{study}.png']), dpi=200)
    print(os.sep.join(['images/', f'{study}.png']))
    


def plt_emg(emg_data, t_stance, e_hs):



    rts, lts = t_stance
    itr, itl = e_hs[0]              #extracting initial heel strikes of the gait cycle 
    ftr, ftl = e_hs[1]              #extracting final heel strikes
    r_emg = emg_data.iloc[itr: ftr + 1, 0:4]
    l_emg = emg_data.iloc[itl: ftl + 1, 4:]
    r_time = np.arange(0.001, len(r_emg)) / 1000
    l_time = np.arange(0.001, len(l_emg)) / 1000
    fig, axs = plt.subplots(4, 2, figsize = (14.3, 10))
    fig.subplots_adjust(hspace = 0.7, wspace = 0.3)

    for (index, msc_l), msc_r in zip(enumerate(l_emg.columns), r_emg.columns):


        axs[index, 0].plot(r_time, r_emg[msc_r], color='forestgreen')
        axs[index, 0].set_title(msc_r, loc = "center", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'black'})
        axs[index, 0].axvline(x= rts, ymin=-0.5, ymax=1,color = 'forestgreen')
        axs[index, 1].plot(l_time, l_emg[msc_l], color='red')
        axs[index, 1].set_title(msc_l, loc = "center", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'black'})
        axs[index, 1].axvline(x= lts , ymin=-0.5, ymax=1,color = 'red')
        # print(msc_l, msc_r)



    for ax in axs.flat:
        ax.set(xlabel='Tiempo (s)', ylabel='mV')
        ax.set_yticks(np.arange(-0.5, 1, step=0.5))
        ax.set_ylim(-0.5, 0.5)
        ax.margins(x=0)

    


    plt.savefig(os.sep.join(['images/', 'emg.png']), dpi=200)


def find_ranges(max_min):
    ranges_df = pd.concat([
        max_min.loc['Max'] - max_min.loc['Min'], max_min.loc['Max Ap'] - max_min.loc['Min Ap'], max_min.loc['Max Bal'] - 
        max_min.loc['Min Bal'], max_min.loc['Max Ap'] - max_min.loc['Min'], max_min.loc['Max Bal'] - max_min.loc['Min'], 
        max_min.loc['Max'] - max_min.loc['Min Ap']
    ], axis=1).transpose()
    ranges_df.index = ['Rango Global', 'Rango Ap', 'Rango Bal', 'Rango Ap global', 'Rango Bal global', 'Rango MaxG_MinAp']
    return ranges_df


def find_max_min(df, to):
    rto, lto = to
    

    length = len(df.columns)

    cycle_percents = pd.DataFrame(
        [[0] * length, [100] * length, [rto, lto] * int((length / 2))],
        columns=df.columns, index=['initial', 'final', 'toe_off']
    ) 

    toe_off_df = pd.concat([df.iloc[rto, 0::2], df.iloc[lto, 1::2]])
    max_ap_vals = pd.concat([df.iloc[0:rto, 0::2].max(), df.iloc[0:lto, 1::2].max()])
    max_ap_idx = pd.concat([df.iloc[0:rto, 0::2].idxmax(), df.iloc[0:lto, 1::2].idxmax()])
    min_ap_vals = pd.concat([df.iloc[0:rto, 0::2].min(), df.iloc[0:lto, 1::2].min()])
    min_ap_idx = pd.concat([df.iloc[0:rto, 0::2].idxmin(), df.iloc[0:lto, 1::2].idxmin()])
    max_bal_vals = pd.concat([df.iloc[rto:, 0::2].max(), df.iloc[lto:, 1::2].max()])
    max_bal_idx = pd.concat([df.iloc[rto:, 0::2].idxmax(), df.iloc[lto:, 1::2].idxmax()])
    min_bal_vals = pd.concat([df.iloc[rto:, 0::2].min(), df.iloc[lto:, 1::2].min()])
    min_bal_idx = pd.concat([df.iloc[rto:, 0::2].idxmin(), df.iloc[lto:, 1::2].idxmin()])


    
    max_ap = pd.concat([
        max_ap_vals, max_ap_idx, min_ap_vals, min_ap_idx, 
        max_bal_vals, max_bal_idx, min_bal_vals, min_bal_idx
        ], axis=1)


    

    max_min_df = pd.concat(
        [df.max(), df.idxmax(), df.min(), df.idxmin(), max_ap, toe_off_df, cycle_percents.iloc[2], 
        df.iloc[0], cycle_percents.iloc[0], df.iloc[-1], cycle_percents.iloc[1]],
        axis=1).transpose()
    

    max_min_df.index = [
        'Max', 'Max %', 'Min', 'Min %', 'Max Ap', 'Max Ap %', 'Min Ap',
        'Min Ap %', 'Max Bal', 'Max Bal %', 'Min Bal', 'Min Bal %', 'Despegue',
        'Despegue %', 'Cont. Ini', 'Cont. Ini%', 'Cont. Fin', 'Cont. Fin%'
    ] 

    

    return max_min_df, find_ranges(max_min_df)

def data2table(plane, i, mm, rng):
    data_rng = np.concatenate((['Rango'], np.round([rng.loc['Rango Global'][0], rng.loc['Rango Global'][1]], 2))) 
    height = [180, 60]
    if plane != 'sagittal' or i == 0:
        data_mm = [
                [mm.index.tolist()[idx] for idx in [0,2,12,14,16]],
                [mm.loc['Max'][0], mm.loc['Min'][0], mm.loc['Despegue'][0], mm.loc['Cont. Ini'][0], mm.loc['Cont. Fin'][0]],
                [mm.loc['Max %'][0], mm.loc['Min %'][0], mm.loc['Despegue %'][0], mm.loc['Cont. Ini%'][0], mm.loc['Cont. Fin%'][0]],
                [mm.loc['Max'][1], mm.loc['Min'][1], mm.loc['Despegue'][1], mm.loc['Cont. Ini'][1], mm.loc['Cont. Fin'][1]],
                [mm.loc['Max %'][1], mm.loc['Min %'][1], mm.loc['Despegue %'][1], mm.loc['Cont. Ini%'][1], mm.loc['Cont. Fin%'][1]]
            ]   
    elif i == 2: 
        data_mm = [
                [mm.index.tolist()[idx] for idx in [4, 8, 2, 12, 14, 16]],
                [mm.loc['Max Ap'][0], mm.loc['Max Bal'][0], mm.loc['Min'][0], mm.loc['Despegue'][0], mm.loc['Cont. Ini'][0], mm.loc['Cont. Fin'][0]],
                [mm.loc['Max Ap %'][0], mm.loc['Max Bal %'][0], mm.loc['Min %'][0], mm.loc['Despegue %'][0], mm.loc['Cont. Ini%'][0], mm.loc['Cont. Fin%'][0]],
                [mm.loc['Max Ap'][1], mm.loc['Max Bal'][1], mm.loc['Min'][1], mm.loc['Despegue'][1], mm.loc['Cont. Ini'][1], mm.loc['Cont. Fin'][1]],
                [mm.loc['Max Ap %'][1], mm.loc['Max Bal %'][1], mm.loc['Min %'][1], mm.loc['Despegue %'][1], mm.loc['Cont. Ini%'][1], mm.loc['Cont. Fin%'][1]]
            ]   
        data_rng = [
            ['Rango AP', 'Rango Bal'],
            np.round([rng.loc['Rango Ap global'][0], rng.loc['Rango Bal global'][0]], 2),
            np.round([rng.loc['Rango Ap global'][1], rng.loc['Rango Bal global'][1]], 2)
            ]
        height = [210, 90]
    elif i == 4:
        data_mm = [
                [mm.index.tolist()[idx] for idx in [6, 8, 12, 14, 16]],
                [mm.loc['Min Ap'][0], mm.loc['Max Bal'][0], mm.loc['Despegue'][0], mm.loc['Cont. Ini'][0], mm.loc['Cont. Fin'][0]],
                [mm.loc['Min Ap %'][0], mm.loc['Max Bal %'][0], mm.loc['Despegue %'][0], mm.loc['Cont. Ini%'][0], mm.loc['Cont. Fin%'][0]],
                [mm.loc['Min Ap'][1], mm.loc['Max Bal'][1], mm.loc['Despegue'][1], mm.loc['Cont. Ini'][1], mm.loc['Cont. Fin'][1]],
                [mm.loc['Min Ap %'][1], mm.loc['Max Bal %'][1], mm.loc['Despegue %'][1], mm.loc['Cont. Ini%'][1], mm.loc['Cont. Fin%'][1]]
            ]   
        data_rng = np.concatenate((['Rango'], np.round([rng.loc['Rango MaxG_MinAp'][0], rng.loc['Rango MaxG_MinAp'][1]], 2))) 
    elif i == 6:
        data_mm = [
                [mm.index.tolist()[idx] for idx in [4, 6, 8, 10, 12, 14]],
                [mm.loc['Max Ap'][0], mm.loc['Min Ap'][0], mm.loc['Max Bal'][0], mm.loc['Min Bal'][0], mm.loc['Despegue'][0], mm.loc['Cont. Ini'][0]],
                [mm.loc['Max Ap %'][0], mm.loc['Min Ap %'][0], mm.loc['Max Bal %'][0], mm.loc['Min Bal %'][1], mm.loc['Despegue %'][0], mm.loc['Cont. Ini%'][0]],
                [mm.loc['Max Ap'][1], mm.loc['Min Ap'][1], mm.loc['Max Bal'][1], mm.loc['Max Bal'][1], mm.loc['Despegue'][1], mm.loc['Cont. Ini'][1]],
                [mm.loc['Max Ap %'][1], mm.loc['Min Ap %'][1], mm.loc['Max Bal %'][1], mm.loc['Max Bal %'][1], mm.loc['Despegue %'][1], mm.loc['Cont. Ini%'][1]]
            ]
        data_rng =  [    
            ['Rango', 'Rango AP', 'Rango Bal'],
            np.round([rng.loc['Rango Global'][0], rng.loc['Rango Ap'][0], rng.loc['Rango Bal'][0]], 2),
            np.round([rng.loc['Rango Global'][1], rng.loc['Rango Ap'][1], rng.loc['Rango Bal'][1]], 2)
            ]
        height = [210, 120]
        
    return data_mm, data_rng, height
    
def plt_tables(kin_data, plane, toe_off): 
    clmn_names = np.array(planes()[plane]).flatten()
    clmn_names = ['ac' + string for string in clmn_names]
    
    

    # Find the ranges dataframe
    
    mm_df, rng_df = find_max_min(kin_data[clmn_names], toe_off)
  

    for i in np.arange(0, len(mm_df.columns), 2):
        joints = [mm_df.columns[i], mm_df.columns[i+1]]
        mm_joint, rang_joint = mm_df[joints], rng_df[joints]   

        data_mm, data_rng, h = data2table(plane, i, mm_joint, rang_joint)
        
        fig_mm = go.Figure(data=[go.Table(
            columnorder = [1, 2, 3, 4, 5],
            columnwidth = [1.5, 1],
            header=dict(values = ['', 'Der °', 'Der %', 'Izq °', 'Izq %'], 
                        fill_color = 'lightgrey',
                        align = 'center',
                        font = dict(color='black', size=12),
                        line_color = 'black'),

            cells=dict(values = data_mm,
                        align = 'center',
                        height = 30, 
                        fill_color = ['#d9d9d9', ['white', '#f2f2f2'] * 3],
                        font = dict(color = 'black', size = 12),
                        line_color = 'black'))
        ])
        fig_mm.update_layout(width = 330, height = h[0], margin = {'l': 0, 'r': 0.5, 't': 0.5, 'b': 0})

        fig_rng = go.Figure(data=[go.Table(
            columnorder = [1, 2, 3],
            columnwidth = [0.75, 1],
            header=dict(values = ['','Derecho', 'Izquierdo'], 
                        fill_color = '#d9d9d9',
                        align = 'center',
                        font = dict(color='black', size=12),
                        line_color = 'black'),

            cells=dict(values = data_rng,
                        align ='center',
                        height = 30, 
                        fill_color = ['#d9d9d9', ['white','#f2f2f2'] * 3],
                        font = dict(color = 'black', size = 12),
                        line_color = 'black'))
        ])
        fig_rng.update_layout(width = 330, height = h[1], margin = {'l': 0, 'r': 0.5, 't': 0, 'b': 0})
        fig_mm.write_image(os.sep.join(['images', f'mm_{plane}{int(i / 2)}.png']), scale = 3)
        fig_rng.write_image(os.sep.join(['images', f'rng_{plane}{int(i / 2)}.png']), scale = 3)



def plt_tables_CIN(kin_data, study, toe_off): 
    clmn_names = np.array(studys()[study]).flatten()
    clmn_names = [ string for string in clmn_names]
    


    df=kin_data[clmn_names]

    
    mm_df=pd.concat([df.max(), df.idxmax(), df.min(), df.idxmin()],axis=1).transpose()

    
    columnas=mm_df.keys()
    h = [100, 120]
    units={'F':'N','M':'','P':'W','Ml':''}


    

    for i in np.arange(0, len(mm_df.columns), 2):

        
              


        data_mm = [['Max','Min'],[mm_df[columnas[i]][0],mm_df[columnas[i]][2]],[mm_df[columnas[i]][1],mm_df[columnas[i]][3]],
                    [mm_df[columnas[i+1]][0],mm_df[columnas[i+1]][2]],
                    [mm_df[columnas[i+1]][1],mm_df[columnas[i+1]][3]]]                                         
        
        fig_mm = go.Figure(data=[go.Table(
            columnorder = [1, 2, 3, 4, 5],
            columnwidth = [0.7, 1],
            header=dict(values = ['', f'Der {units[study]}', 'Der %', f'Izq {units[study]}', 'Izq %'], 
                        fill_color = 'lightgrey',
                        align = 'center',
                        font = dict(color='black', size=12),
                        line_color = 'black'),

            cells=dict(values = data_mm,
                        align = 'center',
                        height = 30, 
                        fill_color = ['#d9d9d9', ['white', '#f2f2f2'] * 3],
                        font = dict(color = 'black', size = 12),
                        line_color = 'black'))
        ])
        fig_mm.update_layout(width = 330, height = h[0], margin = {'l': 0, 'r': 0.5, 't': 0.5, 'b': 0})

        
 
        fig_mm.write_image(os.sep.join(['images', f'mm_{study}{int(i / 2)}.png']), scale = 3)
 
