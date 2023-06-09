import numpy as np

from CODIGOS.data import read_data
from CODIGOS.plot_table import plt_table

def max_displ(df):
    return abs(df['Bari Body X'].max() - df['Bari Body X'].min())


def avg_radial_displ(df):
    """Average distance from the COP to the centroid"""

    RadiX = abs(df['Bari Body X'].mean() - df['Bari Body X'])
    return sum(RadiX) / len(RadiX)


def distance(df,type = None):
    x = df['Bari Body X'].to_numpy('float64')[1:] - df['Bari Body X'].to_numpy('float64')[:-1] 
    y = df['Bari Body Y'].to_numpy('float64')[1:] - df['Bari Body Y'].to_numpy('float64')[:-1]
    if type == "COP":
        return sum(np.hypot(x,y))
    return sum(abs(y))


def area_s(df,time):
    """Area per second

    Sum of triangles area (centroid / current point  / next point) / 30sec
    
    """

    trian = np.array([[[df['Bari Body X'].mean(), df['Bari Body Y'].mean(), 1.0],
                [df['Bari Body X'][i], df['Bari Body Y'][i], 1.0],
                [df['Bari Body X'][i + 1], df['Bari Body Y'][i + 1], 1.0]
            ] for i in range(1, len(df))])
    return sum(abs(np.linalg.det(trian)) / 2) / time
    

def ellipse_area(df):
    return df['Bari Body X'].std(axis = 0),df['Bari Body Y'].std(axis = 0)


def stabilo(time_test = 30, comp=False,folder=str):
 
    OA1, OA2, OC1, OC2, GLO = read_data(comp,folder= folder) 

    if OC1.empty | OC2.empty:
        close_eyes = False 
    else: 
        close_eyes = True



    ec_time = int(time_test)         # test times (eyes closed, eyes open)
    eo_time = int(time_test)   

    # Open eyes variables

    rangeML_avg_eo = (max_displ(OA1) + max_displ(OA2)) / 2
    desRadiML_avg_eo = (avg_radial_displ(OA1) + avg_radial_displ(OA2)) / 2
    velAP_eo1 = distance(OA1) / eo_time
    velAP_eo2 = distance(OA2) / eo_time
    velAP_avg_eo = (velAP_eo1 + velAP_eo2) / 2
    As_avg_eo = (area_s(OA1,eo_time) + area_s(OA2,eo_time)) / 2
    

    # dis_eo = (distance(OA1,"COP") + distance(OA2,"COP")) / 2
    # Std_ML_eo1, Std_AP_eo1 = ellipse_area(OA1)
    # Std_ML_eo2, Std_AP_eo2 = ellipse_area(OA2)

    # Std_ML_eo_avg = (Std_ML_eo1 + Std_ML_eo2) / 2
    # Std_AP_eo_avg = (Std_AP_eo1 + Std_AP_eo2) / 2


    # CLose eyes?
 
    if close_eyes: 
        
        rangeML_avg_ec = (max_displ(OC1) + max_displ(OC2)) / 2   
        desRadiML_avg_ec = (avg_radial_displ(OC1) + avg_radial_displ(OC2)) / 2

        # dis_ec = (distance(OC1,"COP") + distance(OC2,"COP")) / 2
        
        velAP_ec1 = distance(OC1) / eo_time
        velAP_ec2 = distance(OC2) / eo_time    
        velAP_avg_ec = (velAP_ec1 + velAP_ec2) / 2
        As_avg_ec = (area_s(OC1,eo_time) + area_s(OC2,eo_time)) / 2
        # Std_ML_ec1, Std_AP_ec1 = ellipse_area(OC1)
        # Std_ML_ec2, Std_AP_ec2 = ellipse_area(OC1)

        # Std_ML_ec_avg = (Std_ML_ec1 + Std_ML_ec2) / 2
        # Std_AP_ec_avg = (Std_AP_ec1 + Std_AP_ec2) / 2

        data = [[max_displ(OA1), avg_radial_displ(OA1), velAP_eo1, area_s(OA1, eo_time), GLO['Global'][0]],
            [max_displ(OA2), avg_radial_displ(OA2), velAP_eo2, area_s(OA2, eo_time), GLO['Global'][1]],
            [rangeML_avg_eo, desRadiML_avg_eo, velAP_avg_eo, As_avg_eo, GLO['Global'][2]],
            [max_displ(OC1), avg_radial_displ(OC1), velAP_ec1, area_s(OC1, ec_time), GLO['Global'][3]],
            [max_displ(OC2), avg_radial_displ(OC2), velAP_ec2, area_s(OC2, ec_time), GLO['Global'][4]],
            [rangeML_avg_ec, desRadiML_avg_ec, velAP_avg_ec, As_avg_ec, GLO['Global'][5]]
        ]
        rows = ['Ojos abiertos 1', 'Ojos abiertos 2', 'Ojos abiertos Promedio',
                'Ojos cerrados 1', 'Ojos cerrados 2', 'Ojos cerrados Promedio']
    else:  
        data = [[max_displ(OA1), avg_radial_displ(OA1), velAP_eo1, area_s(OA1, eo_time), GLO['Global'][0]],
            [max_displ(OA2), avg_radial_displ(OA2), velAP_eo2, area_s(OA2, eo_time), GLO['Global'][1]],
            [rangeML_avg_eo, desRadiML_avg_eo, velAP_avg_eo, As_avg_eo, GLO['Global'][2]],
        ]  
        rows = ['Ojos abiertos 1', 'Ojos abiertos 2', 'Ojos abiertos Promedio']
    # print(data.transpose())
    data = np.around(np.array(data).T,2)
    

    data = np.vstack([rows, data])
    plt_table(data, comp)

    
    