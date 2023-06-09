import plotly.graph_objects as go

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


def table_15s(avg, cv, col):

    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4],
    columnwidth = [1,1,1,1],
    header=dict(values= ['CV' , 'Promedio']*2, 
                fill_color='#cccccc',
                align='center',
                font=dict(color='black', size=13, family = "Helvetica"),
                line_color='black'),
        
    cells=dict(values= [cv.loc[:,col[0]], avg.loc[:,col[0]], cv.loc[:, col[1]], avg.loc[:, col[1]]], 
                align='center',
                fill_color=[['white', '#f2f2f2'] * 12],
                font=dict(color = 'black', size = 13, family = "Helvetica"),
                line_color='black'))
    ])
    fig.update_layout(
        width=300, height=550, margin={'l': 0, 'r': 0.5, 't': 25, 'b': 0},
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
                'osc_time' : ['Duración de Oscilaciòn de la zancada izquierda (%)', 'Duración de Oscilaciòn de la zancada derecha (%)']
            }

def table_title(cols):
    if cols == 'step_len':
        title = 'Longitud de Paso (m)'
    else:
        title = column_names()[cols][0].split()
        title.pop(-2)
        title = ' '.join(title)
    return title

def plt_tables(df_gen_sts, avg_15s, cv_15s, cols, ctr):
    
    title = table_title(cols)

    stts_table_fig = stats_table(df_gen_sts, column_names()[cols], ctr, title)
    tbl_15_plt = table_15s(avg_15s, cv_15s, column_names()[cols])

    stts_table_fig.write_image('images/' + cols + 'stats.png', scale=3)

    tbl_15_plt.write_image('images/' + cols + '15s.png', scale=3)