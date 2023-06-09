import numpy as np

from CODIGOS.data import*
from CODIGOS.kin_emg_plot import*
def dh_study(s: str, study:str, path=str):
     if study=='Ml':
         study='M'

     if s =='DH_Children':
        sheet_name = f'DH{study}_Children'
     else:
        sheet_name = f'DH{study}_Adults'
     dh_data = pd.read_excel(os.sep.join(['normatives','dh_normal.xlsx']), sheet_name = sheet_name,  header = 7, index_col = 0).dropna()

     return dh_data

def fix_order(e_hs):
    if (e_hs[0]>e_hs[1]).any():
        idxs = np.where(e_hs[0]>e_hs[1])[0]
        for idx in idxs:
            temp = e_hs[0][idx]
            e_hs[0][idx] = e_hs[1][idx]
            e_hs[1][idx] = temp
    return list(e_hs)


def rms(age, path, run):
    times, scalars, events, kinec_data, emg_data, dh_normal, forces, powers, momentos, thereare_kinetics, s = read_dataRMS(age, path, run)

    scalars.iloc[:, :-2] *= 100
    events = events * 1000 + 7

    t_stance = times.loc[0, ['tseqRSTANCE', 'tseqLSTANCE']].tolist()
    e_hs = fix_order(events[['eRHS', 'eLHS']].values.astype(int))  # this results in [[initial_right, initial_left][final_right, final_left]]
    toe_off = np.round(scalars.loc[0, ['sRSTANCE', 'sLSTANCE']].tolist()).astype(int)

    try:
        plt_emg(emg_data, t_stance, e_hs)
        haveemg=True
    except:
        haveemg=False
        
    for plane in ['sagittal', 'frontal', 'transverse']:
        plt_tables(kinec_data, plane, toe_off)
        plt_kin(kinec_data, dh_normal, plane, toe_off)



    if thereare_kinetics:
        plt_cin(forces, dh_study(s, 'F', path), 'F', toe_off)
        plt_tables_CIN(forces, 'F', toe_off)

        plt_cin(powers, dh_study(s, 'P', path), 'P', toe_off)
        plt_tables_CIN(powers, 'P', toe_off)

        plt_cin(momentos, dh_study(s, 'M', path), 'M', toe_off)
        plt_tables_CIN(momentos, 'M', toe_off)

        plt_cin(momentos, dh_study(s, 'Ml', path), 'Ml', toe_off)
        plt_tables_CIN(momentos, 'Ml', toe_off)

    return thereare_kinetics,haveemg