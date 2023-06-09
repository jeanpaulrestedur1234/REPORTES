import plotly.graph_objects as go
import os

def plt_table(data, comp=False):
    columns = ['<b>Prueba</b>', '<b>Rango<br>(mm)<br>  ML</b>', '<b>Dezplazamiento <br>   Radial (mm) <br>' + ' '*10 + 'ML</b>', 
                '<b>Velocidad<br> (mm/s)<br>' + ' '*6 + 'AP</b>',
                '<b>Área/Segundo<br>   (mm²/s)</b>', '<b>Área de Elipse<br>' + ' '*6 + 'global</b>']
    fig = go.Figure(data=[go.Table(
        columnorder = [1, 2, 3, 4, 5, 6],
        columnwidth = [1.7, 1, 1.5, 1, 1.3, 1.3],
        header=dict(values = columns, 
                    fill_color = '#cccccc',
                    align = 'center',
                    font = dict(color='black', size=12),
                    line_color = 'black'),
            
        cells=dict(values = data,
                    align ='center',
                    height = 30, 
                    fill_color = [['white','white','#f2f2f2'] * 2],
                    font = dict(color = 'black', size = 12),
                    line_color='black'))
    ])
    fig.update_layout(width = 700, height = 290, margin = {'l': 0, 'r': 0.5, 't': 0.5, 'b': 0})
    if not comp:
        fig.write_image('images\stabilo.png', scale = 3)
    else:
        fig.write_image('images\prev_stabilo.png', scale = 3)

