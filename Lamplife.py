import glob
import numpy as np

import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
from PIL import ImageTk, Image

from datetime import date
import tkinter as tk
import tkinter.font as font


def get_POD_file_names():
    return glob.glob("/Volumes/Operations/0.POD/POD qPCR/POD EXPORTS/QS_details/*_details.txt")

def get_small_file_names():
    return glob.glob("/Volumes/0.Covid-19/QTP/Export/*_details.txt")

def make_data_arrays(filenames,names,hours):
    for x in range(0,len(filenames)):
        instrument = get_instrument_name(filenames[x])
        usage = get_lamp_hours(filenames, x)
        
        names.append(instrument)
        hours = np.append(hours,int(usage))
      
       
    return hours

def get_instrument_name(textpath):
    splitpath = textpath.split("/") 
    splitname = splitpath[len(splitpath)-1].split("_")
    return splitname[0]

def get_lamp_hours(filenames,filenumber):

 
    string_to_search = "Lamp Life"
    with open(filenames[filenumber], 'r') as read_obj:
    
        for line in read_obj:
            
            if string_to_search in line:
                tokenize = line.split(bytes.fromhex("09").decode('utf-8'))
                tokenize1 = tokenize[3].split(" ")         
   
    return tokenize1[0]

def make_POD_bar_graph(names,hours,title):
    
    threshold = 1500
    
    today = date.today()
    day = today.strftime("%m/%d/%Y")
    
    title_date = title + day 
    
    
    above_threshold = np.maximum(hours - threshold, 0)
    below_threshold = np.minimum(hours, threshold)
    
    parameters = {'xtick.labelsize': 15, 'ytick.labelsize':20,}
    plt.rcParams.update(parameters)

    
    PODfig, ax = plt.subplots(figsize=(35,12))
    ax.grid()
    ax.bar(names, below_threshold, color="g", label="Instrument within spec")
    ax.bar(names, above_threshold, color="r", bottom = below_threshold, label = "Bulb Overuse")
    plt.axhline(y=1500, color='black', label="NEW BULB NEEDED")

    ax.set_ylabel('Lamp Hours', fontsize=25)
    ax.set_xlabel('QS7 Name',fontsize=25)
    ax.set_title(title_date,fontsize=30, fontweight='bold')
    ax.legend(fontsize=25)
    ax.set(ylim=(0, 2000))

    
    for tick in ax.get_xticklabels():
        tick.set_rotation(40)
        
    plt.gcf().subplots_adjust(bottom=0.12)
    PODfig.show()
    
    return PODfig

def make_small_bar_graph(names,hours,title):
    
    threshold = 1500
    
    today = date.today()
    day = today.strftime("%m/%d/%Y")
    
    title_date = title + day 
    
    
    above_threshold = np.maximum(hours - threshold, 0)
    below_threshold = np.minimum(hours, threshold)
    
    parameters = {'xtick.labelsize': 25, 'ytick.labelsize':20,}
    plt.rcParams.update(parameters)

    
    smallfig, ax = plt.subplots(figsize=(18,12))
    ax.grid()
    ax.bar(names, below_threshold, color="g", label="Instrument within spec")
    ax.bar(names, above_threshold, color="r", bottom = below_threshold, label = "Bulb Overuse")
    plt.axhline(y=1500, color='black', label="NEW BULB NEEDED")

    ax.set_ylabel('Lamp Hours', fontsize=25)
    ax.set_xlabel('QS7 Name',fontsize=25)
    ax.set_title(title_date,fontsize=30, fontweight='bold')
    ax.legend(fontsize=25)
    ax.set(ylim=(0, 2000))
    
    
    
    for tick in ax.get_xticklabels():
        tick.set_rotation(40)
    plt.gcf().subplots_adjust(bottom=0.18)
    smallfig.show()
    
    return smallfig

def GUI():
    
    
    root = tk.Tk()
    root.title("Broad Institute QS7 Lamp Life Tracker")
    root.geometry("800x600")
    
    img = ImageTk.PhotoImage(Image.open("/Users/rluisfue/Downloads/download.png"))
    
    panel = tk.Label(root, image = img, borderwidth = 25)
    panel.pack(side = "top", fill = "both", expand = "no")

                                        
    startbutton = tk.Button(root, text='Check Lamp Life', width=20, height=3, command=lambda: generate_data(root))

    myFont = font.Font(size=30)

    startbutton['font'] = myFont
    
    startbutton.pack()
    
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    
 
    
def show_save(podfigure,smallfigure,root):
    
    podbutton = tk.Button(root, text='Save POD Data', width=20, height=3, command= lambda: save_figure(podfigure,"/Users/rluisfue/Desktop/LampLife/POD/"))
    smallbutton = tk.Button(root, text='Save Small Covid Data', width=20, height=3, command= lambda: save_figure(smallfigure,"/Users/rluisfue/Desktop/LampLife/Small Covid/"))
    myFont = font.Font(size=30)
    podbutton['font'] = myFont
    smallbutton['font'] = myFont
    
    smallbutton.pack()
    podbutton.pack()
    

def save_figure(figure,path):
    
    today = date.today()
    day = today.strftime("%m_%d_%Y")
    report = day + " Report"    
    
    filename = path + report
    
    figure.savefig(filename)
    
firsttime = 0 
    
def generate_data(root):

    global firsttime
    
    if(firsttime == 0):
    
        podfilenames = get_POD_file_names()
        podfilenames.sort()
        
        podnames = []
        podhours = np.array([])
    
        podhours = make_data_arrays(podfilenames,podnames,podhours)
        
        smallfilenames = get_small_file_names()
        smallfilenames.sort()
        
        smallnames = []
        smallhours = np.array([])
        
        smallhours = make_data_arrays(smallfilenames, smallnames, smallhours)
    
        
        podfig = make_POD_bar_graph(podnames,podhours,"POD Quant Studio Bulb Life as of ")
        smallfig = make_small_bar_graph(smallnames, smallhours, "Small Covid Quant Studio Bulb Life as of ")
        
        show_save(podfig, smallfig,root)
        
        firsttime = 1
    
def main():
    
    
    GUI()
    

if __name__ == "__main__":
    main()
    
