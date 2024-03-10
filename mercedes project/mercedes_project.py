#Import Libraries
#----------------------
from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter
from tkinter import ttk

global meeting_code,session_code,session_ITEMS,session_MAPPING,session,btn1,plot_widget,sector1Btn,ITEMS,MAPPING

#Create Window
#----------------------
window = tkinter.Tk()

#Define Meeting names and their meeting code
#----------------------
url = "https://api.openf1.org/v1/meetings"
response = urlopen(url)
data111 = json.loads(response.read().decode('utf-8'))
ITEMS = []
MAPPING = {}

for data11 in data111:
    ITEMS.append(data11["meeting_official_name"])
    MAPPING[data11["meeting_official_name"]] = data11["meeting_key"]


meeting_code = 0
session_ITEMS=[]
session_MAPPING = {}

# function to get session code ready for the graphs 
def onSessionSelect(event):
    global session_code, section1_44,section1_63,section2_44,section2_63,section3_44,section3_63,laptime_44,laptime_63,sector1Btn
    session_code = session_MAPPING[session.get()]
    btn1.place(x=20,y=70)
    sector1Btn.place(x=140,y=70)
    sector2Btn.place(x=290,y=70)
    sector3Btn.place(x=440,y=70)
    url = "https://api.openf1.org/v1/laps?session_key=%d" % session_code
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

    section1_63, section2_63, section3_63, laptime_63 = [], [], [], []

    section1_44, section2_44, section3_44, laptime_44 = [], [], [], []

    for datapoint in data:
        if(datapoint["driver_number"]==63):
            if (datapoint["is_pit_out_lap"] != True and datapoint["duration_sector_3"] is not None): 
                section1_63.append(datapoint["duration_sector_1"])
                section2_63.append(datapoint["duration_sector_2"])
                section3_63.append(datapoint["duration_sector_3"])
                laptime_63.append(datapoint["lap_duration"])
        elif(datapoint["driver_number"] == 44):
            if (datapoint["is_pit_out_lap"] != True and datapoint["duration_sector_3"] is not None): 
                section1_44.append(datapoint["duration_sector_1"])
                section2_44.append(datapoint["duration_sector_2"])
                section3_44.append(datapoint["duration_sector_3"])
                laptime_44.append(datapoint["lap_duration"])


# function that converts the time into minutes 
def format_yticks(y, _):
    minutes = int(y // 60)
    seconds = int(y % 60)
    return f"{minutes}:{seconds:02d}"

#function to get the circuit code from the country name
def onSelect(event):
    global sesison_ITEMS, session_MAPPING
    meeting_code = MAPPING[meeting.get()]
    url = "https://api.openf1.org/v1/sessions?meeting_key=%d" % meeting_code
    response = urlopen(url)
    data1 = json.loads(response.read().decode('utf-8'))
    
    session_ITEMS=[]
    session_MAPPING = {}

    for datapoint in data1:
        session_ITEMS.append(datapoint["session_name"])
        session_MAPPING[datapoint["session_name"]] = datapoint["session_key"]
    
    session.config(values = session_ITEMS)
    session.set(session_ITEMS[0])
    session.bind('<<ComboboxSelected>>', onSessionSelect)
    session.place(x=100,y=40)
  
def create_graph(laptime_63,laptime_44):
    global plot_widget,clearbtn, plt 
    try:
        clearGraph()
    except:
        pass
    ypoints = np.array(laptime_63)
    
    fig = plt.figure(1)

    plt.subplot(1, 2, 1)

    plt.title("Car 63 laptime")
    plt.xlabel("lap count")
    plt.ylabel("time")

    plt.plot(ypoints,label = session.get())
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_yticks))
    plt.legend(loc="upper left")
    
    plt.subplots_adjust(left=0.1,bottom=0.11,right=0.95,top=0.88,wspace=0.25,hspace=0.2)
    
    plt.subplot(1, 2, 2)
    
    ypoints = np.array(laptime_44)

    plt.plot(ypoints,label = session.get())
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_yticks))

    plt.legend(loc="upper left")

    plt.title("Car 44 laptime")
    plt.xlabel("lap count")
    plt.ylabel("time")
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    plot_widget = canvas.get_tk_widget()
    plot_widget.place(x=20,y=100)
    clearbtn.place(x=590,y=70)

def clearGraph():
    plt.clf()
    plot_widget.destroy()

#Country combobox
meeting = ttk.Combobox(window, values=ITEMS,width = 100)
meeting.set(ITEMS[0])
meeting.bind('<<ComboboxSelected>>', onSelect)
meeting.place(x=100,y=10)

#Session picking combobox
session = ttk.Combobox(window, values=session_ITEMS)

#Get graph button   
btn1 = tkinter.Button(window, command =lambda:create_graph(laptime_63,laptime_44), text = "Compare Laptimes")

clearbtn = tkinter.Button(window, text = "Clear Graphs",command = clearGraph)

sector1Btn = tkinter.Button(window,text = "Compare Sector 1 Times",command = lambda:create_graph(section1_63,section1_44))
sector2Btn = tkinter.Button(window,text = "Compare Sector 2 Times",command = lambda:create_graph(section2_63,section2_44))
sector3Btn = tkinter.Button(window,text = "Compare Sector 3 Times",command = lambda:create_graph(section3_63,section3_44))

window.geometry("1000x1000")
window.config(bg="white")
window.mainloop()
