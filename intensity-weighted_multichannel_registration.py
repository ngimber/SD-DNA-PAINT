import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import scipy.spatial
import scipy.stats
import scipy.signal
plt.style.use(['seaborn-white', 'seaborn-deep'])
from scipy.interpolate import interp1d
import csv
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter import *
from tkinter import IntVar
from os import path
from os import makedirs
from csv import writer
from csv import reader
from tkinter import ttk




################global variables
global files
global path
global binning
global reconstructionChannel
global newPath
global fileTmp

###############get Files
root = Tk()


PathList = askopenfilenames(filetypes=(
("SD_filtered", "*filter_out*"),
("All files", "*.*")
))

root.destroy()


files=[]
for thisfile in PathList:
    folder, file = path.split(thisfile)
    files=files+[file]

folder=folder+"/"

path=folder
###############



##############variables TK box
doCorrection=True
binning =10
doOverlay=True
reconstructionChannel="weighted"

##################


###############get Parameters
def getParameters():




    def show_entry_fields():



        global doCorrection
        doCorrection=v.get()
        global binning
        binning=e2.get()
        global doOverlay
        doOverlay=v3.get()
        global reconstructionChannel
        reconstructionChannel=e4.get()


        master.destroy()



    def gogogo():
        global addChannel
        addChannel=False
        show_entry_fields()





    master = Tk()
    master.title("Multicchannel-Registration for Spectral Demixing")
    Label(master, text="                                       ").grid(row=0, column=0,sticky=W)
    Label(master, text="Correct for chromatic errors:          ").grid(row=1, column=0,sticky=W)
    Label(master, text="Bin size for chromatic correction [nm]:").grid(row=2, column=0,sticky=W)
    Label(master, text="                                       ").grid(row=3, column=0,sticky=W)
    Label(master, text="Merge multichannels:                   ").grid(row=6, column=0,sticky=W)
    Label(master, text="Source of localizations:               ").grid(row=7, column=0,sticky=W)
    Label(master, text="                                       ").grid(row=8, column=0,sticky=W)
    Label(master, text="                                       ").grid(row=9, column=0,sticky=W)
    Label(master, text="Methodical details: https://doi.org/10.1101/2021.11.19.469218").grid(row=10, column=0,sticky=W)
    Label(master, text="niclas.gimber@charite.de ").grid(row=10, column=4,sticky=E)




    v = StringVar()
    v.set(True)

    Checkbutton(master, variable=v).grid(row=1, column=2, sticky=W)


    v2 = IntVar()
    e2 = Entry(master, text=v2, width=45)
    e2.grid(row=2, column=2, sticky=W)
    v2.set(10)

    v3 = IntVar()
    v3.set(True)
    Checkbutton(master, variable=v3).grid(row=6, column=2, sticky=W)





    v4 = IntVar()
    e4 = ttk.Combobox(master,values=[
                                        "1: Weight both channels by intensity",
                                    "2: Use short wavelength channel localizations","3: Use long wavelength channel localizations","4: Use brightest localization (decide pairwise)","5: Use brightest channel (decide imagewise)",],text=v4, width=42)


    e4.grid(row=7, column=2,sticky=W)
    v4.set("1: Weighted both channels by intensity")




    Button(master, text='Start Processing',fg="green",bg="gray83", command=gogogo).grid(row=9, column=4,columnspan=1000)
    master.attributes("-topmost", True)


    mainloop()

getParameters()



reconstructionChannel=["weighted","short","long","brightest","brightestchannel"][int(reconstructionChannel[0])-1]
doCorrection=bool(doCorrection)
doOverlay=bool(doOverlay)
binning=int(binning)

print(doCorrection)
print(binning)
print(doOverlay)
print(reconstructionChannel)

#################



def correction(table):

    if(len(table.columns)==7):
        table["8"]=[99]*len(table)
    headers=["x short [nm]","y short [nm]", "I short", "frame","x long [nm]","y long [nm]", "I long","ch"]
    table.columns=headers


    table["dX"]=table["x long [nm]"]-table["x short [nm]"].values
    table["dY"]=table["y long [nm]"]-table["y short [nm]"].values

    dX=table["x long [nm]"]-table["x short [nm]"].values
    dY=table["y long [nm]"]-table["y short [nm]"].values

    x=np.round(table["x short [nm]"].values)
    y=np.round(table["y short [nm]"].values)

    y=np.round(table["y short [nm]"].values)
    dX=table["dX"]
    dY=table["dY"]
    dXMatrix=scipy.stats.binned_statistic_2d(x,y,dX,"median",bins=[((x.max()-x.min())/binning),((y.max()-y.min())/binning)])[0]
    dYMatrix=scipy.stats.binned_statistic_2d(x,y,dY,"median",bins=[((x.max()-x.min())/binning),((y.max()-y.min())/binning)])[0]


    def NNinterpolate(matrix):
        mask = np.isnan(matrix)
        matrix[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), matrix[~mask])
        return matrix


    dXMatrixInterpolate=NNinterpolate(dXMatrix)
    dYMatrixInterpolate=NNinterpolate(dYMatrix)


    dXMatrix_smooth=(scipy.ndimage.gaussian_filter((dXMatrixInterpolate),50))
    dYMatrix_smooth=(scipy.ndimage.gaussian_filter((dYMatrixInterpolate),50))

    newXlong=[]
    newYlong=[]
    xmin=x.min()
    ymin=y.min()

    xlong=table["x long [nm]"].values
    ylong=table["y long [nm]"].values
    for k in range(0,len(x)):
        x_=x[k]
        y_=y[k]
        xlong_=xlong[k]
        ylong_=ylong[k]
        newXlong+=[xlong_-dXMatrix_smooth[int(math.floor((x_-xmin)/binning))-1,int(math.floor((y_-ymin)/binning))-1]]
        newYlong+=[ylong_-dYMatrix_smooth[int(math.floor((x_-xmin)/binning))-1,int(math.floor((y_-ymin)/binning))-1]]


    table_corr=table[:]
    table["x long [nm]"]=newXlong
    table["y long [nm]"]=newYlong

    output=table_corr[table.columns[0:8]]

    with open(path+files[i], newline='') as f:
        reader = csv.reader(f)
        row1 = next(reader)  # gets the first line
    row1

    np.savetxt(newPath+files[i][:files[i].find(".txt")]+"_corr.txt",output.values,comments="" ,header=row1[0],fmt='%f')
    return(output)



#############################################
def overlayChannels(table):

    #if("filter_out_" in fileTmp):
    if(len(table.columns==8)):
        headers=["x short [nm]","y short [nm]", "I short", "frame","x long [nm]","y long [nm]", "I long","ch"]
    else:
        headers=["x short [nm]","y short [nm]", "I short", "frame","x long [nm]","y long [nm]", "I long"]

    table.columns=headers

    global saveMe

    if (reconstructionChannel)=="short":
        print("reconstruct short")
        if("filter" in fileTmp):
            saveMe=table[["frame","x short [nm]","y short [nm]","I short","ch"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame", "x [nm]", "y [nm]","intensity_photon","ch"]
        else:
            saveMe=table[["frame","x short [nm]","y short [nm]","I short"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame", "x [nm]", "y [nm]","intensity_photon"]

        pd.options.mode.chained_assignment = None  # default='warn'

        if("ch" in table.columns):
            tmp=table[table["ch"]>0]
        else:
            tmp=table

        xoffset=(tmp["x short [nm]"]-tmp["x long [nm]"]).median()
        xshort=table["x short [nm]"]
        xlong=table["x long [nm]"]+xoffset

        yoffset=(tmp["y short [nm]"]-tmp["y long [nm]"]).median()
        yshort=table["y short [nm]"]
        ylong=table["y long [nm]"]+yoffset


    if (reconstructionChannel)=="long":
        print("reconstruct long")
        if("filter" in fileTmp):
            saveMe=table[["frame","x long [nm]","y long [nm]","I long","ch"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame", "x [nm]", "y [nm]","intensity_photon","ch"]
        else:
            saveMe=table[["frame","x long [nm]","y long [nm]","I long"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame", "x [nm]", "y [nm]","intensity_photon"]

        pd.options.mode.chained_assignment = None  # default='warn'

        if("ch" in table.columns):
            tmp=table[table["ch"]>0]
        else:
            tmp=table

        xoffset=(tmp["x short [nm]"]-tmp["x long [nm]"]).median()
        xshort=table["x short [nm]"]
        xlong=table["x long [nm]"]+xoffset

        yoffset=(tmp["y short [nm]"]-tmp["y long [nm]"]).median()
        yshort=table["y short [nm]"]
        ylong=table["y long [nm]"]+yoffset



    if (reconstructionChannel)=="weighted":
        print("reconstruct weighted")
        if("filter" in fileTmp):
            saveMe=table[["frame","I long","ch"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame","intensity_photon","ch"]

        else:
            saveMe=table[["frame","I long"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame","intensity_photon"]

        pd.options.mode.chained_assignment = None  # default='warn'

        if("ch" in table.columns):
            tmp=table[table["ch"]>0]
        else:
            tmp=table

        xoffset=(tmp["x short [nm]"]-tmp["x long [nm]"]).median()
        xshort=table["x short [nm]"]
        xlong=table["x long [nm]"]+xoffset

        yoffset=(tmp["y short [nm]"]-tmp["y long [nm]"]).median()
        yshort=table["y short [nm]"]
        ylong=table["y long [nm]"]+yoffset



        saveMe["x [nm]"]=((table["x long [nm]"]-table["x long [nm]"].mean())*table["I long"]   +   (table["x short [nm]"]-table["x short [nm]"].mean())*table["I short"])    /     (table["I long"]+table["I short"])
        saveMe["y [nm]"]=((table["y long [nm]"]-table["y long [nm]"].mean())*table["I long"]   +   (table["y short [nm]"]-table["y short [nm]"].mean())*table["I short"])    /     (table["I long"]+table["I short"])




    if (reconstructionChannel)=="brightest":
        print("reconstruct brightest")
        if("filter" in fileTmp):
            saveMe=table[["frame","I long","ch"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame","intensity_photon","ch"]
        else:
            saveMe=table[["frame","I long"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame","intensity_photon"]

        pd.options.mode.chained_assignment = None  # default='warn'

        if("ch" in table.columns):
            tmp=table[table["ch"]>0]
        else:
            tmp=table

        xoffset=(tmp["x short [nm]"]-tmp["x long [nm]"]).median()
        xshort=table["x short [nm]"]
        xlong=table["x long [nm]"]+xoffset

        yoffset=(tmp["y short [nm]"]-tmp["y long [nm]"]).median()
        yshort=table["y short [nm]"]
        ylong=table["y long [nm]"]+yoffset

        condition=((table["I short"]/table["I long"])>1).tolist()

        saveMe["x [nm]"]=np.where(condition,xshort,xlong)
        saveMe["y [nm]"]=np.where(condition,yshort,ylong)





    if (reconstructionChannel)=="brightestchannel":
        print("reconstruct brightestchannel")
        if("filter" in fileTmp):
            saveMe=table[["frame","I long","ch"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame","intensity_photon","ch"]
        else:
            saveMe=table[["frame","I long"]]
            saveMe.reset_index(level=0, inplace=True)
            saveMe.columns=["id","frame","intensity_photon"]

        pd.options.mode.chained_assignment = None  # default='warn'

        if("ch" in table.columns):
            tmp=table[table["ch"]>0]
        else:
            tmp=table

        xoffset=(tmp["x short [nm]"]-tmp["x long [nm]"]).median()
        xshort=table["x short [nm]"]
        xlong=table["x long [nm]"]+xoffset

        yoffset=(tmp["y short [nm]"]-tmp["y long [nm]"]).median()
        yshort=table["y short [nm]"]
        ylong=table["y long [nm]"]+yoffset


        saveMe["x [nm]"]=0
        saveMe["y [nm]"]=0

        shortBylong=[]
        for ch in np.unique(table["ch"]):

            tmp=table[table["ch"]==ch]
            shortBylong=tmp["I short"].median()/tmp["I long"].median()

            condition=(saveMe["ch"]==ch).tolist()


            if shortBylong>1:




                saveMe["x [nm]"]=np.where(condition,xshort,saveMe["x [nm]"])
                saveMe["y [nm]"]=np.where(condition,yshort,saveMe["y [nm]"])

            else:
                saveMe["x [nm]"]=np.where(condition,xlong,saveMe["x [nm]"])
                saveMe["y [nm]"]=np.where(condition,ylong,saveMe["y [nm]"])







    saveMe["x [nm]"]=saveMe["x [nm]"]-saveMe["x [nm]"].min()
    saveMe["y [nm]"]=saveMe["y [nm]"]-saveMe["y [nm]"].min()







    #### save file

    name=newPath+"/Pairs2Thunder_"+fileTmp[0:-4]+".csv"

    saveMe[saveMe.columns.tolist()].to_csv(name, index=None)
    tmp=saveMe[saveMe.columns.tolist()]

    if("filter" in fileTmp):

        zero=tmp[tmp["ch"]==0]
        zero.iat[0,4]=0
        zero.iat[0,5]=0
        zero.iat[0,3]=999999
        zero.iat[1,4]=saveMe["x [nm]"].max()
        zero.iat[1,5]=saveMe["y [nm]"].max()
        zero.iat[1,3]=999999
        zero.to_csv(name[0:-4]+"_noise.csv", index=None)

        a=tmp[tmp["ch"]==1]
        a.iat[0,4]=0
        a.iat[0,5]=0
        a.iat[0,3]=999999
        a.iat[1,4]=saveMe["x [nm]"].max()
        a.iat[1,5]=saveMe["y [nm]"].max()
        a.iat[1,3]=999999
        a.to_csv(name[0:-4]+"_ch1.csv", index=None)

        b=tmp[tmp["ch"]==2]
        b.iat[0,4]=0
        b.iat[0,5]=0
        b.iat[0,3]=999999
        b.iat[1,4]=saveMe["x [nm]"].max()
        b.iat[1,5]=saveMe["y [nm]"].max()
        b.iat[1,3]=999999
        b.to_csv(name[0:-4]+"_ch2.csv", index=None)

        if(len(tmp[tmp["ch"]==3])>0):
            c=tmp[tmp["ch"]==3]
            c.iat[0,4]=0
            c.iat[0,5]=0
            c.iat[0,3]=999999
            c.iat[1,4]=saveMe["x [nm]"].max()
            c.iat[1,5]=saveMe["y [nm]"].max()
            c.iat[1,3]=999999
            c.to_csv(name[0:-4]+"_ch3.csv", index=None)








for i in range (0,len(files)):
    fileTmp=files[i]
    print(fileTmp)
    table=pd.read_table(path+fileTmp,header=None, skiprows=1,sep=" ")



    if (doCorrection==True):

        newPath=path+"cor_\\"
        if (os.path.exists(newPath)==False):
            os.makedirs(newPath)

        table=correction(table)
        fileTmp=fileTmp.replace(".","_corr.")
    else:
        newPath=path


    if(doOverlay==True):
        table=pd.read_table(newPath+files[i][:files[i].find(".txt")]+"_corr.txt",header=None, skiprows=1,sep=" ")
        if (doCorrection==True):
            newPath=newPath+reconstructionChannel+"\\"
        else:
            newPath=path+reconstructionChannel+"\\"

        if (os.path.exists(newPath)==False):
            os.makedirs(newPath)

        overlayChannels(table)
