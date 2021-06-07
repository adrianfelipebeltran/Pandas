from scipy import optimize
import tkinter as tk
from tkinter import *
import tkFileDialog as filedialog
from tkinter import ttk
from tkFileDialog import askopenfilename
import pandas as pd
import matplotlib as pit
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import glob
import os
import functools
import math


filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Open file okay?",
                                          filetypes= (("excel file","*.xlsx"),
                                         ("all files","*.*")))

window = tk.Tk()
window.title("First line input depth to which line should be ")
window.geometry('500x500')

df = pd.read_excel(filepath, sheetname = '1')
print(df)
def interp():
    
    GWT = float(e2.get())
    test = float(e1.get())
    
    print(test)
    print("depth of overburden")
    print(GWT)
    print("GWT")
    global df
    df = pd.read_excel(filepath, sheetname = '1')
    #make column of values that depend on global water table height input\
    df.drop('gamma', axis=1, inplace=True)
    df.drop('sigma_t', axis=1, inplace=True)
    df.drop('sigma_eff', axis=1, inplace=True)
    global x
    x = len(df['depth'])
    #print(x)
    #print(df)
    z=0
    overburden = 0
    depthlast = 0
    addedinterp = 0
    zz = 1
    global zzz
    zzz = 0
    
    while zz < x-1:
        if GWT>=df.iloc[zz]['depth'] and GWT<=df.iloc[zz-1]['depth'] and zzz==0: 
            if df.iloc[zz-1]['depth']>=df.iloc[zz]['depth']:
                print('we found the ground water table to be in between the following two depths')
                print(df.iloc[zz-1]['depth'])
                print(df.iloc[zz]['depth'])
                print(df.iloc[zz]['unit weight']-62.5)
                
                this = df.iloc[zz-1]['unit weight']
                print(this)
                thisis= df.iloc[zz]['unit weight']-62.5
                print(thisis)
                
                line = pd.DataFrame({"depth": GWT, "unit weight": this}, index=[zz])
                line2 = pd.DataFrame({"depth": GWT, "unit weight": thisis}, index=[zz])
                #line3 = pd.DataFrame({"depth": GWT, "unit weight": thisisnext}, index=[zz])
                global df2
                df2 = pd.concat([df.iloc[:zz], line2, df.iloc[zz:]]).reset_index(drop=True)
                global zy
                zy = zz
                
                df2 = pd.concat([df2.iloc[:zy], line2, df2.iloc[zy:]]).reset_index(drop=True)
                
                df2 = pd.concat([df2.iloc[:zy], line, df2.iloc[zy:]]).reset_index(drop=True)
                             
                zzz = zz+3
                xx = len(df2['depth'])
                while zzz < xx:
                    print('at this depth below:')
                    print(df2.iloc[zzz]['depth'])
                    print('we adjust the unit weight by 62.5')
                    thisone = df2.iloc[zzz]['unit weight'] - 62.5
                    df2.at[zzz, 'unit weight'] = thisone
                    zzz=zzz+1
                    
        if zzz>zz:
            zz = zzz-5
        
        print('depth of iteration')
        zz = zz+1
        print(df.iloc[zz]['depth'])
    print('the GWT adjusted unit weight table can be found below')
    # in case the water table doesn't affect anything we need to create df2
    print(x)
    #print(df)
    z=0
    overburden = 0
    depthlast = 0
    addedinterp = 0
    zz = 0 
    x = len(df2['depth'])
    while z+1 < x:
        depth = df2.iloc[z]['depth']
        depthlast = df2.iloc[z-1]['depth']
        z = z+1
        if test<df2.iloc[z-1]['depth']:
            if depth < depthlast:
                print('your input is this much from the previous depth')
                deltadepth = depthlast - depth
                print(deltadepth)
                unit = df2.iloc[z-1]['unit weight']
                additional = deltadepth*unit
                overburden = deltadepth*unit + overburden
                print('this iteration has yielded the following overburden')
                print(overburden)
        if test>=df2.iloc[z]['depth'] and addedinterp==0:
            if df2.iloc[z-2]['depth']<df2.iloc[z]['depth']:
                print('false alarm')
            print('interpolation time baby')
            depth = df2.iloc[z+1]['depth']
            depthlastlast = df2.iloc[z-2]['depth']
            print('depth is below')
            print(depth)
            print('depth z-2 is below')
            print(depthlastlast)
            u1 = df2.iloc[z]['unit weight']
            deep = test-depthlast
            unitweight = u1
            print('unitweight is')
            print(unitweight)
            print('your input is this much from the previous depth')
            print(deep)
            addedinterp = unitweight*deep
            print(addedinterp)
            print('below is the overburden before interpolation')
            print(overburden)
            overburden = overburden - addedinterp
            print('below is the overburden after interpolation')
            print(overburden)
    
    print('overburden is below')
    print(overburden)
    print(df2)
            
def plotmeplz():
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    xseries = df['depth']
    yseries = df['unit weight']
    ax.set_title('Design Line Interpolation')
    ax.set_ylabel('unitweight')
    ax.set_xlabel('depth')
    xxseries = df2['depth']
    yyseries = df2['unit weight']
    plt.plot(xseries,yseries)
    plt.plot(xxseries, yyseries)
    plt.show()
    

def save():
    text = os.path.basename(filepath)
    one = 'C:\\New\\temp\\'
    two = '_output.csv'
    name = one + text + two
    df.to_csv (name, index = False, header=True)
    print(df)
    
w = tk.Label(window, text="Enter the depth (including negative sign) of overburden to calc")
w.pack()
z = tk.Label(window, text="Enter the depth (including negative sign) of GWT")
e1 = Entry(window)
e1.pack()
z.pack()
e2 = Entry(window)
e2.pack()
b4 = tk.Button(window, text="DO NOT PUSH THIS BUTTON", width = 25, height = 2, command=interp)
b4.pack()
b5 = tk.Button(window, text = "Unit Weight v Depth Plot Plz", width =25, height=2, command = plotmeplz)
b5.pack()
b8 = tk.Button(window, text='Save', width=15, height=2, command=save)
b8.pack()

window.mainloop()
#y = df['unit weight']
#ax.set_title('Design Line Interpolation')
#ax.set_ylabel('unitweight')
#ax.set_xlabel('depth')
#plt.plot(x,y)
#global f
#f = interp1d(x, y)

    
#yy = f(x)
#print(f(-38))
#plt.plot(x, yy)
#plt.show(
