import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utilities import *
import calendar
from datetime import datetime, timedelta
import matplotlib

def get_duration(event):
    di = event["fechaInicio"]
    df = event["fechaFin"]
    ti = event["tiempoInicio"]
    tf = event["tiempoFin"]

    dti = get_date(di[0], di[1], di[2], ti[0], ti[1])
    dtf = get_date(df[0], df[1], df[2], tf[0], tf[1])

    diff = dtf - dti

    return diff.days + diff.seconds / 60 / 60 / 24

def get_ini_sum(event):
    d = event["fechaInicio"]
    t = event["tiempoInicio"]

    d1 = get_date(d[0], d[1], d[2], 0, 0)
    d2 = get_date(d[0], d[1], d[2], t[0], t[1])

    diff = d2 - d1

    return diff.seconds / 60 / 60 / 24

def get_end(event):
    return int(event["fechaFin"][0])

def get_date(day, month, year, hour, min):
    return datetime(int(year), int(month), int(day), int(hour), int(min))
    
def get_maximum(running):
    ans = get_date(1, 1, 2000, 22, 22)

    for event in running:
        d = event["fechaFin"]
        t = event["tiempoFin"]
        ans = max(ans, get_date(d[0], d[1], d[2], t[0], t[1]))

    return ans + timedelta(1)

def get_max_num(running):
    ans = 0
    for event in running:
        ans = max(ans, event["eventNum"])
    return ans

class Utils:
    axis = 0

def createGraph():
    matplotlib.rcParams['toolbar'] = 'none'
    running = readJson("code/running_events.json")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    maxDate = get_maximum(running)
    index = 1

    x_axis, label_x = [], []
    y_axis = []

    for year in range(2077, maxDate.year + 1):
        rm = maxDate.month if year == maxDate.year else 12

        for month in range(1, rm + 1): 
            rd = maxDate.day if year == maxDate.year and month == maxDate.month else calendar.monthrange(year, month)[1]

            for day in range(1, rd + 1):
                x_axis.append(len(x_axis) + 1)
                label_x.append(f"{day}/{month}\n{year}")
    
    for count in range(1, max(8, get_max_num(running) + 2)):
        y_axis.append(count)

    if len(x_axis) < 10:
        x_axis = []
        label_x = []
        for x in range(1, 11):
            x_axis.append(x)
            label_x.append(f"{x}/{1}\n{2077}")
    
    ax.set_xticks(x_axis)
    ax.set_xticklabels(label_x)
    ax.set_yticks(y_axis)
    ax.tick_params(colors="white")

    for event in running:
        eini = event["fechaInicio"]
        ini = f"{eini[0]}/{eini[1]}\n{eini[2]}"
        x = label_x.index(ini) + get_ini_sum(event) + 1

        r = patches.Rectangle(
            (x, event["eventNum"] - 0.3), 
            get_duration(event), 
            0.6
        )
       
        r.set_facecolor(colors[event["eventID"] - 1])
        r.set_edgecolor([0.07, 0.07, 0.07, 0.85])
        ax.add_patch(r)
        index += 1

    fig.patch.set_facecolor([0.07, 0.07, 0.07, 1])
    fig.canvas.manager.set_window_title("Gráfico de Aventuras")
    ax.set_facecolor([0.12, 0.12, 0.12, 1])
    ax.spines["left"].set_color("white")
    ax.spines["bottom"].set_color("white")
    plt.xlim(0, 10)
    plt.ylim(0, 7)
    plt.xlabel("Fecha→",fontsize=20, fontweight='bold', color="white", loc='right')
    plt.ylabel("Aventuras→",fontsize=20, fontweight='bold', color="white", loc='top')

    def keypress(press):
        x = ax.get_xlim()
        y = ax.get_ylim()
        
        if press.key == 'up' and y[1] < len(y_axis):
            ax.set_ylim(y[0] + 1, y[1] + 1)
        if press.key == 'down' and y[0] > 0:
            ax.set_ylim(y[0] - 1, y[1] - 1)

        if press.key == 'right' and x[1] < len(x_axis):
            ax.set_xlim(x[0] + 1, x[1] + 1)
        if press.key == 'left' and x[0] > 0:
            ax.set_xlim(x[0] - 1, x[1] - 1)
        
        fig.canvas.draw_idle()

    
    fig.canvas.mpl_connect('key_press_event', keypress)
    