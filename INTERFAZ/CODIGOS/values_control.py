from traceback import print_tb


def control_values(param, age):

    if param in ('step_dur' , 'step_len' , 'stride_cad'): return 'No hay datos'
    if param == 'stride_dur':
        if age >= 3 and age <= 5: 
            control = '2.9%-6.6%'
        elif age >= 6 and age <= 9:
            control = '1.7%-3.5%'
        elif age >= 10 and age <= 14:
            control = '1.1%-2.2%'
        elif age >= 15 and age <= 36:
            control = '0.8%-3.1%'   
        elif age >= 37 and age <= 65:
            control = '2.01%-2.8%'
        elif age >= 66 and age <=80:
            control = '0.8%-6.1%'
        elif age >= 81 and age <=90:
            control = '2.8%-10.80%'  
        else:
            control = 'No hay datos'
    elif param == 'stride_len':
        if age >= 4 and age <= 18: 
            control = '1.2%-9.2%'
        elif age >= 19 and age <= 34:
            control = '0.5%-5.1%'     
        elif age >= 35 and age <=80: 
            control = '0.5%-5.2%'
        elif age >= 80 and age <=90:
            control = '4.07%-5.35%'
        else:
            control = 'No hay datos'
    elif param == 'stride_vel':
        if age >= 1 and age <= 3: 
            control = '6.4%-26.6%'
        elif age >= 4 and age <= 7:
            control = '4.5%-20%'
        elif age >= 8 and age <= 11:
            control = '2.5%-14%'
        elif age >= 12 and age <= 16:
            control = '2.8%-11.8%'
        elif age >= 17 and age <= 68:
            control = '3.7%-4.5%'
        elif age >= 69 and age <= 75:
            control = '6.4%-10%'
        else:
            control = 'No hay datos'
    else:
        if age >= 4 and age <= 10:
            control = '3%-8%'
        elif age >= 19 and age <= 23: 
            control = '2.53%'
        elif age >= 24 and age <= 54:
            control = '4.38%-4.9%'     
        elif age >= 55 and age <= 79:
            control = '4.08%-7.38%'
        elif age >= 80 and age <= 90: 
            control = '5.0%-18.20%'
        else:
            control = 'No hay datos'
    return control 
