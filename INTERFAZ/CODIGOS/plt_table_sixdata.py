import plotly.graph_objects as go


def plt_table(df, n_v):

    fig = go.Figure(data = [go.Table(
        columnorder = [1,2],
        columnwidth = [1.5,1],
        header=dict(values = [df.columns.name] + df.columns.tolist(),
                    fill_color = '#668099',
                    align = ['left', 'center'],
                    font = dict(color = 'white', size = 12),
                    line_color = 'black'),
            
        cells=dict(values = [df.index[0:4],df.Valor[0:4]],
                    align = ['left','center'],
                    fill_color = 'white',
                    font = dict(color = 'black', size = 10),
                    line_color = 'black'))
    ])

    fig.update_layout(width = 450, height = 125, margin = {'l': 0, 'r': 0.5, 't': 0.2, 'b': 0})

    fig2 = go.Figure(data=[go.Table(
        columnorder = [1, 2, 3],
        columnwidth = [2, 1, 1],
        header=dict(values = [df.columns.name] + df.columns.tolist() + ['Valor normal'],
                    fill_color = '#668099',
                    align = ['left','center'],
                    font = dict(color = 'white', size=12),
                    line_color = 'black'),

        cells=dict(values= [df.index[4:], df.Valor[4:], [''] + n_v + ['','','']],
                    align=['left', 'center'],
                    font=dict(color = 'black', size = 10),
                    fill_color = 'white',            
                    line_color = 'black'))
    ])
    fig2.update_layout(width=600, height=210, margin={'l': 0, 'r': 0.5, 't': 0.2, 'b': 0})

    fig.write_image('images/sess_data.png', scale = 3)
    fig2.write_image('images/normal_values.png', scale = 3)


  



