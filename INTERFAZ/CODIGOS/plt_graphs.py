import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_fig(x_label, y_label, filename, v_time, data1, data2=None, plot2sides = False):
    


 #   print(data1)

    diff=(np.array(data1[1:])-np.array(data1[:len(data1)-1]))/15
       

   # plt.plot(v_time[1:],diff)
    #plt.ylim(-2,2)
    #plt.show()
    
    
    plt.figure(figsize=(12,5), dpi= 200)
    
    
    if not plot2sides:   
        D=pd.DataFrame({'time':v_time,'values':data1})
        tendencia=round((D['time'].corr(D['values'])),2)
        plt.plot(v_time, data1, marker='o')
        plt.ylim(data1.min() - data1.std(), data1.max() + data1.std())
        plt.text(2, data1.max()- data1.std()/2, f'Tendencia L:{tendencia}', fontsize=10,
                 
                 
                 bbox={'facecolor':'white', 'pad':10, 'alpha':0.25})
    else:
        D=pd.DataFrame({'time':v_time,'values':data1,'values2':data2})
        tend1=round((D['time'].corr(D['values'])),2)
        tend2=round((D['time'].corr(D['values2'])),2)
        ymin = (data1.min() - data1.std()) if data1.min() < data2.min() else (data2.min() - data2.std())
        ymax = (data1.max() + data1.std()) if data1.max() > data2.max() else (data2.max() + data2.std())
        plt.plot(v_time, data1, marker='o', color='red')
        plt.plot(v_time, data2, marker='o', color='forestgreen')
        plt.ylim(ymin, ymax)
        
        plt.text(2,(ymax-ymin)/100*94+ymin, f'Tendencia L:{tend1}', fontsize=10, color='red',
                 bbox={'facecolor':'white', 'pad':10, 'alpha':0.25})
        plt.text(2,(ymax-ymin)/100*2+ymin, f'Tendencia L:{tend2}', fontsize=10, color='forestgreen',
                 bbox={'facecolor':'white', 'pad':10, 'alpha':0.25})
    
   

    plt.vlines(x = [60,120,180,240,300,360], ymin=plt.axis()[2], ymax=plt.axis()[3],  color='black', linestyle='dotted')

 
    

    plt.grid()
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(np.arange(0, 365, 15))
    plt.title(y_label, fontname='Times New Roman', size=14, fontweight='bold')
    plt.savefig(f'images/{filename}.png')
    plt.close()
    
